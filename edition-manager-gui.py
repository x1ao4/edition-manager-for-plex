import tkinter as tk
from tkinter import messagebox
import subprocess

def run_command(command):
    try:
        subprocess.run(["python", "edition-manager.py", command], check=True)
        messagebox.showinfo("Success", f"Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while executing '{command}': {str(e)}")

def create_gui():
    root = tk.Tk()
    root.title("Edition Manager for Plex")
    root.geometry("300x250")

    tk.Label(root, text="Edition Manager for Plex", font=("Helvetica", 16)).pack(pady=10)

    buttons = [
        ("Process All Movies", "--all"),
        ("Reset All Movies", "--reset"),
        ("Backup Metadata", "--backup"),
        ("Restore Metadata", "--restore")
    ]

    for button_text, command in buttons:
        tk.Button(root, text=button_text, command=lambda cmd=command: run_command(cmd)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()