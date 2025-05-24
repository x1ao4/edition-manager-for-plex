import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import queue
import configparser
import os
from pathlib import Path
import sys

# Check if ttkthemes is available, if not, we'll use the default theme
try:
    from ttkthemes import ThemedTk, ThemedStyle
    THEMED_TK_AVAILABLE = True
except ImportError:
    THEMED_TK_AVAILABLE = False

class ModernFramedFrame(ttk.Frame):
    """A modern frame with a subtle border and background"""
    def __init__(self, master, **kwargs):
        if 'padding' not in kwargs:
            kwargs['padding'] = (10, 10)
        if 'relief' not in kwargs:
            kwargs['relief'] = 'flat'
        super().__init__(master, **kwargs)

class DragDropListbox(tk.Listbox):
    """ A Listbox with drag-and-drop reordering """
    
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.bind('<Button-1>', self.start_drag)
        self.bind('<B1-Motion>', self.during_drag)
        self.bind('<ButtonRelease-1>', self.stop_drag)
        
        self.drag_start_index = None
        self.drag_end_index = None
        self.being_dragged = False
        self.update_callback = None
        
    def start_drag(self, event):
        # Get the index of the clicked item
        self.drag_start_index = self.nearest(event.y)
        
        # Make sure we clicked on an item
        if self.drag_start_index < 0 or self.drag_start_index >= self.size():
            return
            
        # Store the item we're dragging
        self.being_dragged = True
        
    def during_drag(self, event):
        if not self.being_dragged:
            return
            
        # Get current position
        current_index = self.nearest(event.y)
        
        # Make sure we're over a valid position
        if current_index < 0 or current_index >= self.size():
            return
            
        # Save current drag position for drop
        self.drag_end_index = current_index
        
        # Visual feedback - draw a line where item will be inserted
        self.delete('insertion_line')
        y_coord = self.bbox(current_index)[1]
        if current_index > self.drag_start_index:
            # Line below item
            y_coord += self.bbox(current_index)[3]
        self.create_line(0, y_coord, self.winfo_width(), y_coord, 
                         tag='insertion_line', fill='#3498db', width=2)
        
    def stop_drag(self, event):
        if not self.being_dragged:
            return
            
        # Check if checkbox part of item was clicked
        item_x = event.x
        if item_x < 25:  # Approximately where checkbox is
            # Handle checkbox toggle instead of drag-drop
            self.toggle_checkbox(self.drag_start_index)
            self.being_dragged = False
            self.delete('insertion_line')
            return
            
        # Check if we have a valid drop position
        if self.drag_end_index is not None and self.drag_start_index != self.drag_end_index:
            # Get the item being moved
            item_text = self.get(self.drag_start_index)
            
            # Remove it from original position
            self.delete(self.drag_start_index)
            
            # Insert at new position
            if self.drag_end_index > self.drag_start_index:
                # Adjust index since we removed an item
                self.drag_end_index -= 1
            
            self.insert(self.drag_end_index, item_text)
            self.selection_set(self.drag_end_index)
        
        # Clean up
        self.being_dragged = False
        self.drag_start_index = None
        self.drag_end_index = None
        self.delete('insertion_line')
        
        # Always call the update callback after drag operations
        if self.update_callback:
            self.update_callback()
            
    def toggle_checkbox(self, index):
        """Toggle the checkbox at the given index"""
        if index < 0 or index >= self.size():
            return
            
        item_text = self.get(index)
        if item_text.startswith("[✓]"):
            # Currently checked, uncheck it
            new_text = "[ ]" + item_text[3:]
        else:
            # Currently unchecked, check it
            new_text = "[✓]" + item_text[3:]
            
        self.delete(index)
        self.insert(index, new_text)
        self.selection_set(index)
        
        # Call the update callback
        if self.update_callback:
            self.update_callback()

    def get_enabled_modules(self):
        """Get a list of enabled modules in their current order"""
        enabled_modules = []
        for i in range(self.size()):
            item_text = self.get(i)
            if item_text.startswith("[✓]"):
                # Extract module name (remove checkbox part)
                module_name = item_text[4:].strip()
                enabled_modules.append(module_name)
        return enabled_modules

class StatusUpdater:
    def __init__(self, queue):
        self.queue = queue
    
    def write(self, message):
        self.queue.put(message)
    
    def flush(self):
        pass

def run_command_with_progress(command, progress_var, status_queue, button_states):
    try:
        # Disable all buttons during processing
        for button in button_states:
            button.config(state=tk.DISABLED)
        
        progress_var.set(0)
        process = subprocess.Popen(
            ["python", "edition-manager.py", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Process output line by line
        for line in iter(process.stdout.readline, ''):
            status_queue.put(line.strip())
            
            # Update progress bar for specific operations
            if "[" in line and "]" in line:
                # We're parsing log lines like: [2023-01-01 12:34:56] Processing...
                
                # For operations that have known total counts
                if "Movie count:" in line:
                    total_movies = int(line.split("Movie count:")[1].strip())
                    # Store total_movies for progress calculation
                    status_queue.put(f"TOTAL:{total_movies}")
                elif any(movie_title in line for movie_title in [":", "Cleared", "Reset"]):
                    # This is a movie being processed - increment progress
                    status_queue.put("INCREMENT")
        
        process.wait()
        status_queue.put("DONE")
        
        if process.returncode == 0:
            status_queue.put("Command executed successfully.")
        else:
            status_queue.put(f"Error executing command (code {process.returncode}).")
            
    except Exception as e:
        status_queue.put(f"An error occurred: {str(e)}")
    finally:
        # Re-enable all buttons
        for button in button_states:
            button.config(state=tk.NORMAL)

def update_status(status_text, status_queue, progress_var, progress_bar, total_items, current_item):
    try:
        while not status_queue.empty():
            message = status_queue.get_nowait()
            
            if message == "DONE":
                progress_var.set(100)  # Ensure it shows 100% when complete
            elif message.startswith("TOTAL:"):
                total_items[0] = int(message.split(":")[1])
                current_item[0] = 0
            elif message == "INCREMENT":
                current_item[0] += 1
                if total_items[0] > 0:
                    progress_percent = min(100, int(current_item[0] / total_items[0] * 100))
                    progress_var.set(progress_percent)
                    progress_bar.update()
            else:
                status_text.configure(state=tk.NORMAL)
                status_text.insert(tk.END, message + "\n")
                status_text.see(tk.END)  # Scroll to the end
                status_text.configure(state=tk.DISABLED)
    except Exception as e:
        print(f"Error updating status: {str(e)}")
    
    # Schedule next update
    status_text.after(100, update_status, status_text, status_queue, progress_var, progress_bar, total_items, current_item)

def load_config():
    config_path = Path(__file__).parent / 'config' / 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_path)
    return config, config_path

def save_config(config, config_path):
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    messagebox.showinfo("Success", "Configuration saved successfully!")

def open_settings_window(root):
    config, config_path = load_config()
    
    # Create settings window
    settings_window = tk.Toplevel(root)
    settings_window.title("Edition Manager Settings")
    settings_window.geometry("600x480")
    settings_window.grab_set()  # Make window modal
    
    # Add icon if available
    try:
        settings_window.iconbitmap("icon.ico")
    except:
        pass  # Skip if icon not available
    
    # Apply style
    if THEMED_TK_AVAILABLE:
        style = ThemedStyle(settings_window)
        # We'll keep using the same theme as the main window
    
    # Create notebook (tabs)
    notebook = ttk.Notebook(settings_window)
    notebook.pack(fill='both', expand=True, padx=15, pady=15)
    
    # Server settings tab
    server_frame = ModernFramedFrame(notebook)
    notebook.add(server_frame, text='Server')
    
    # Module settings tab
    modules_frame = ModernFramedFrame(notebook)
    notebook.add(modules_frame, text='Modules')
    
    # Language settings tab
    language_frame = ModernFramedFrame(notebook)
    notebook.add(language_frame, text='Language')
    
    # Rating settings tab
    rating_frame = ModernFramedFrame(notebook)
    notebook.add(rating_frame, text='Rating')
    
    # Performance settings tab
    performance_frame = ModernFramedFrame(notebook)
    notebook.add(performance_frame, text='Performance')
    
    # Server settings
    ttk.Label(server_frame, text="Server Address:", font=('', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=10)
    server_address = ttk.Entry(server_frame, width=40)
    server_address.grid(row=0, column=1, sticky=tk.W, padx=5, pady=10)
    server_address.insert(0, config.get('server', 'address', fallback=''))
    
    ttk.Label(server_frame, text="Server Token:", font=('', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
    server_token = ttk.Entry(server_frame, width=40)
    server_token.grid(row=1, column=1, sticky=tk.W, padx=5, pady=10)
    server_token.insert(0, config.get('server', 'token', fallback=''))
    
    ttk.Label(server_frame, text="Skip Libraries:", font=('', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=10)
    skip_libraries = ttk.Entry(server_frame, width=40)
    skip_libraries.grid(row=2, column=1, sticky=tk.W, padx=5, pady=10)
    skip_libraries.insert(0, config.get('server', 'skip_libraries', fallback=''))
    ttk.Label(server_frame, text="Use semicolons to separate library names", 
              font=('', 8), foreground="#666").grid(row=3, column=1, sticky=tk.W, padx=5)
    
    # Module settings with drag-and-drop list
    ttk.Label(modules_frame, text="Module Order", font=('', 12, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(0, 5))
    
    # Instructions label
    info_frame = ttk.Frame(modules_frame)
    info_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
    
    instruction_label = ttk.Label(
        info_frame, 
        text="• Drag modules to change their order\n• Click the checkbox to enable/disable\n• Enabled modules are processed in order from top to bottom",
        justify="left", 
        font=('', 9)
    )
    instruction_label.pack(side=tk.LEFT, anchor=tk.W)
    
    # Frame for the listbox with a border
    module_list_frame = ttk.LabelFrame(modules_frame, text="Modules")
    module_list_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
    module_list_frame.grid_rowconfigure(0, weight=1)
    module_list_frame.grid_columnconfigure(0, weight=1)
    
    # Custom listbox with drag-and-drop
    module_listbox = DragDropListbox(
        module_list_frame,
        height=12,
        width=40,
        selectbackground='#e0e0e0',
        selectforeground='black',
        font=('Courier', 10),  # Monospace font for better checkbox alignment
        borderwidth=0,
        highlightthickness=0
    )
    module_listbox.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
    
    # Add scrollbar
    module_scrollbar = ttk.Scrollbar(module_list_frame, orient=tk.VERTICAL, command=module_listbox.yview)
    module_scrollbar.grid(row=0, column=1, sticky=tk.NS, padx=(0, 5), pady=5)
    module_listbox.config(yscrollcommand=module_scrollbar.set)
    
    # All available modules
    all_modules = ["Resolution", "Duration", "Rating", "Cut", "Release", "DynamicRange", 
                  "Country", "ContentRating", "Language", "AudioChannels", "Director", 
                  "Genre", "SpecialFeatures", "Studio", "AudioCodec", "Bitrate", 
                  "FrameRate", "Size", "Source", "VideoCodec"]
    
    # Get current module order from config
    current_modules = config.get('modules', 'order', fallback='').split(';')
    current_modules = [m for m in current_modules if m]  # Remove empty strings
    
    # Add modules to listbox
    # First add enabled modules in their order
    for module in current_modules:
        if module in all_modules:
            module_listbox.insert(tk.END, f"[✓] {module}")
            all_modules.remove(module)  # Remove from all_modules list
    
    # Then add the rest as disabled
    for module in all_modules:
        module_listbox.insert(tk.END, f"[ ] {module}")
    
    # Function to update the hidden entry when the list changes
    def update_module_order():
        # This function will be called whenever the module list changes
        # No need to update a hidden entry anymore as we'll get values directly
        pass
    
    # Set the update callback
    module_listbox.update_callback = update_module_order
    
    # Language settings
    ttk.Label(language_frame, text="Excluded Languages:", font=('', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=10)
    excluded_languages = ttk.Entry(language_frame, width=40)
    excluded_languages.grid(row=0, column=1, sticky=tk.W, padx=5, pady=10)
    excluded_languages.insert(0, config.get('language', 'excluded_languages', fallback=''))
    ttk.Label(language_frame, text="Use commas to separate languages", 
              font=('', 8), foreground="#666").grid(row=1, column=1, sticky=tk.W, padx=5)
    
    skip_multiple = tk.BooleanVar(value=config.getboolean('language', 'skip_multiple_audio_tracks', fallback=False))
    skip_checkbox = ttk.Checkbutton(language_frame, text="Skip Multiple Audio Tracks", variable=skip_multiple)
    skip_checkbox.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10)
    
    # Rating settings
    ttk.Label(rating_frame, text="Rating Source:", font=('', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=10)
    rating_source = ttk.Combobox(rating_frame, values=["imdb", "rotten_tomatoes"], state="readonly", width=15)
    rating_source.grid(row=0, column=1, sticky=tk.W, padx=5, pady=10)
    rating_source.set(config.get('rating', 'source', fallback='imdb'))
    
    ttk.Label(rating_frame, text="Rotten Tomatoes Type:", font=('', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
    rt_type = ttk.Combobox(rating_frame, values=["critic", "audience"], state="readonly", width=15)
    rt_type.grid(row=1, column=1, sticky=tk.W, padx=5, pady=10)
    rt_type.set(config.get('rating', 'rotten_tomatoes_type', fallback='critic'))
    
    ttk.Label(rating_frame, text="TMDB API Key:", font=('', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=10)
    tmdb_api_key = ttk.Entry(rating_frame, width=40)
    tmdb_api_key.grid(row=2, column=1, sticky=tk.W, padx=5, pady=10)
    tmdb_api_key.insert(0, config.get('rating', 'tmdb_api_key', fallback=''))
    
    # Performance settings (removed cache TTL section)
    ttk.Label(performance_frame, text="Worker Threads:", font=('', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=10)
    max_workers = ttk.Spinbox(performance_frame, from_=1, to=32, width=5)
    max_workers.grid(row=0, column=1, sticky=tk.W, padx=5, pady=10)
    max_workers.set(config.get('performance', 'max_workers', fallback='8'))
    ttk.Label(performance_frame, text="Number of concurrent threads (4-12 recommended)", 
              font=('', 8), foreground="#666").grid(row=1, column=1, sticky=tk.W, padx=5)
    
    ttk.Label(performance_frame, text="Batch Size:", font=('', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=10)
    batch_size = ttk.Spinbox(performance_frame, from_=1, to=100, width=5)
    batch_size.grid(row=2, column=1, sticky=tk.W, padx=5, pady=10)
    batch_size.set(config.get('performance', 'batch_size', fallback='20'))
    ttk.Label(performance_frame, text="Movies to process in each batch (10-30 recommended)", 
              font=('', 8), foreground="#666").grid(row=3, column=1, sticky=tk.W, padx=5)
    
    # Create a button frame
    button_frame = ttk.Frame(settings_window)
    button_frame.pack(fill=tk.X, padx=15, pady=15)
    
    # Save button
    def save_settings():
        # Get enabled modules directly from the listbox
        enabled_modules = module_listbox.get_enabled_modules()
        module_order_value = ';'.join(enabled_modules)
        
        # Update config object
        config['server'] = {
            'address': server_address.get(),
            'token': server_token.get(),
            'skip_libraries': skip_libraries.get()
        }
        
        config['modules'] = {
            'order': module_order_value  # Use directly retrieved value
        }
        
        config['language'] = {
            'excluded_languages': excluded_languages.get(),
            'skip_multiple_audio_tracks': 'yes' if skip_multiple.get() else 'no'
        }
        
        config['rating'] = {
            'source': rating_source.get(),
            'rotten_tomatoes_type': rt_type.get(),
            'tmdb_api_key': tmdb_api_key.get()
        }
        
        # Make sure performance section exists and update it
        if 'performance' not in config:
            config['performance'] = {}
            
        config['performance']['max_workers'] = max_workers.get()
        config['performance']['batch_size'] = batch_size.get()
        
        save_config(config, config_path)
        settings_window.destroy()
    
    ttk.Button(button_frame, text="Save", command=save_settings, style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.RIGHT, padx=5)

def create_gui():
    # Use ThemedTk if available, otherwise use regular Tk
    if THEMED_TK_AVAILABLE:
        root = ThemedTk(theme="arc")  # Arc is a clean, modern theme
    else:
        root = tk.Tk()
        
    root.title("Edition Manager for Plex")
    root.geometry("850x600")
    root.minsize(600, 400)  # Set minimum window size
    
    # Try to set icon
    try:
        root.iconbitmap("icon.ico")
    except:
        pass  # Skip if icon not available
    
    # Configure style
    if THEMED_TK_AVAILABLE:
        style = root.style
    else:
        style = ttk.Style()
    
    # Define custom styles
    style.configure('Header.TLabel', font=('', 16, 'bold'))
    style.configure('Accent.TButton', font=('', 10, 'bold'))
    style.configure('Title.TLabel', font=('', 12, 'bold'))
    
    # Create a main container frame with padding
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Configure grid weights
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(3, weight=1)  # Status frame should expand
    
    # Header with app name and version
    header_frame = ttk.Frame(main_frame)
    header_frame.grid(row=0, column=0, sticky=tk.W+tk.E, pady=(0, 15))
    
    title_label = ttk.Label(header_frame, text="Edition Manager", style='Header.TLabel')
    title_label.pack(side=tk.LEFT)
    
    version_label = ttk.Label(header_frame, text="v1.6", foreground="#666")
    version_label.pack(side=tk.LEFT, padx=(10, 0), pady=3)

    # Buttons in a modern card-like frame
    actions_frame = ModernFramedFrame(main_frame)
    actions_frame.grid(row=1, column=0, sticky=tk.W+tk.E, pady=(0, 15))
    
    # Title for actions section
    ttk.Label(actions_frame, text="Actions", style='Title.TLabel').grid(
        row=0, column=0, columnspan=5, sticky=tk.W, pady=(0, 10))
    
    button_configs = [
        ("Process All Movies", "--all"),
        ("Reset All Movies", "--reset"),
        ("Backup Editions", "--backup"),
        ("Restore Editions", "--restore"),
        ("Settings", "settings")  # Special case for settings
    ]
    
    buttons = []
    for i, (button_text, command) in enumerate(button_configs):
        button_style = 'Accent.TButton' if command == '--all' else 'TButton'
        button = ttk.Button(
            actions_frame, 
            text=button_text, 
            command=lambda cmd=command: handle_command(cmd),
            style=button_style,
            width=16
        )
        button.grid(row=1, column=i, padx=5, pady=5)
        buttons.append(button)

    # Progress section
    progress_frame = ModernFramedFrame(main_frame)
    progress_frame.grid(row=2, column=0, sticky=tk.W+tk.E, pady=(0, 15))
    
    progress_label = ttk.Label(progress_frame, text="Progress", style='Title.TLabel')
    progress_label.pack(anchor=tk.W, pady=(0, 10))
    
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(
        progress_frame, 
        variable=progress_var, 
        maximum=100,
        length=400,
        mode='determinate'
    )
    progress_bar.pack(fill=tk.X)
    
    # Percentage label next to progress bar
    percentage_label = ttk.Label(progress_frame, text="0%")
    percentage_label.pack(anchor=tk.W, pady=(5, 0))
    
    # Function to update percentage label
    def update_percentage_label():
        percentage_label.config(text=f"{progress_var.get()}%")
        root.after(100, update_percentage_label)
    
    # Start updating percentage label
    update_percentage_label()

    # Status section
    status_frame = ModernFramedFrame(main_frame)
    status_frame.grid(row=3, column=0, sticky=tk.NSEW, pady=(0, 5))
    status_frame.columnconfigure(0, weight=1)
    status_frame.rowconfigure(1, weight=1)
    
    status_label = ttk.Label(status_frame, text="Status", style='Title.TLabel')
    status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
    
    status_text_frame = ttk.Frame(status_frame)
    status_text_frame.grid(row=1, column=0, sticky=tk.NSEW)
    status_text_frame.columnconfigure(0, weight=1)
    status_text_frame.rowconfigure(0, weight=1)
    
    status_text = scrolledtext.ScrolledText(
        status_text_frame, 
        state=tk.DISABLED,
        wrap=tk.WORD,
        background="#f9f9f9",
        borderwidth=1,
        relief="solid",
        font=("Consolas", 9)
    )
    status_text.grid(row=0, column=0, sticky=tk.NSEW)

    # Clear button for status
    ttk.Button(
        status_frame, 
        text="Clear Status", 
        command=lambda: clear_status(status_text)
    ).grid(row=2, column=0, sticky=tk.E, pady=(10, 0))
    
    def clear_status(status_text):
        status_text.configure(state=tk.NORMAL)
        status_text.delete(1.0, tk.END)
        status_text.configure(state=tk.DISABLED)

    # Button commands
    status_queue = queue.Queue()
    total_items = [0]  # Wrapped in list to make it mutable
    current_item = [0]

    def handle_command(cmd):
        if cmd == "settings":
            open_settings_window(root)
        else:
            threading.Thread(
                target=run_command_with_progress,
                args=(cmd, progress_var, status_queue, buttons),
                daemon=True
            ).start()

    # Set up the status updater
    update_status(status_text, status_queue, progress_var, progress_bar, total_items, current_item)

    # Add initial status message
    status_text.configure(state=tk.NORMAL)
    status_text.insert(tk.END, "Welcome to Edition Manager\n")
    status_text.insert(tk.END, "Select an action to begin\n")
    status_text.configure(state=tk.DISABLED)
    
    # Add a footer with version info
    footer_frame = ttk.Frame(main_frame)
    footer_frame.grid(row=4, column=0, sticky=tk.E, pady=(5, 0))
    ttk.Label(
        footer_frame, 
        text="Edition Manager • Python " + ".".join(map(str, sys.version_info[:3])),
        foreground="#666",
        font=("", 8)
    ).pack(side=tk.RIGHT)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()