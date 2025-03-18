# Edition Manager

Edition Manager is a powerful utility that enhances your Plex movie library by automatically generating and updating rich "Edition" metadata based on technical and content specifications of your movie files.

In Plex, there are two concepts of "version": "[Edition](https://support.plex.tv/articles/multiple-editions/)" and "[Version](https://support.plex.tv/articles/200381043-multi-version-movies/)", but their uses are quite different.
Edition Manager
Edition Manager is a powerful tool designed to enhance your Plex media library by leveraging the Edition feature to display rich, customizable metadata for your movies.

# Key Features:
- **Metadata Enhancement**: Extracts and displays crucial information such as resolution, audio codecs, content ratings, and more
- **Customizable Module System**: Allows users to choose which information to display and in what order
- **User-Friendly GUI**: Easy-to-use interface with progress tracking and status updates
- **Performance Optimized**: Utilizes caching, multi-threading, and batch processing
- **Backup & Restore**: Provides options to backup and restore metadata, ensuring you can always revert changes
- **Plex Integration**: Seamlessly integrates with your Plex server, updating movie information directly in the Plex interface

This tool is perfect for movie enthusiasts who want more detailed information about their digital collection at a glance, right within their Plex interface. It turns your Plex server into a comprehensive movie database, enhancing your browsing and selection experience.

# User-Friendly Operations:

Simply run the GUI version
```
python edition-manager-gui.py
```
or on Windows, double-click on `edition-manager-gui.bat`

## Command Line Usage

Edition Manager can be used via command line:

Add all selected Edition information
```
python edition-manager.py --all
```
Remove all Edition information
```
python edition-manager.py --reset
```
Easy backup of current Edition information
```
python edition-manager.py --backup
```
Easy restore of Edition information that was backed up
```
python edition-manager.py --restore
```

Edition Manager transforms your Plex library, offering a more informative and customizable viewing experience. Whether you're distinguishing between cut versions, highlighting technical specifications, or simply enriching your movie displays, this tool provides the means to curate your library exactly as you envision it.

## Available Modules

Edition Manager uses a modular system where each component extracts specific information:

| Module | Description | Example Output |
|--------|-------------|----------------|
| AudioChannels | Audio channel layout | 5.1, 7.1 |
| AudioCodec | Audio format | Dolby TrueHD, DTS-HD MA |
| Bitrate | Video bitrate | 24.5 Mbps |
| ContentRating | Age rating | PG-13, R |
| Country | Production country | USA, France |
| Cut | Special cuts | Director's Cut, Extended |
| Director | Film director | Spielberg |
| Duration | Movie length | 120 MIN |
| DynamicRange | HDR information | HDR, Dolby Vision |
| FrameRate | Frame rate | 24P, 60P |
| Genre | Primary genre | Drama, Sci-Fi |
| Language | Audio language | German, Japanese |
| Rating | IMDB/RT rating | 8.5, 92% |
| Release | Special releases | Anniversary Edition |
| Resolution | Video resolution | 1080P, 4K |
| Size | File size | 58.2 GB |
| Source | Media source | REMUX, WEB-DL |
| SpecialFeatures | Has bonus content | Special Features |
| Studio | Production studio | Warner Bros. |
| VideoCodec | Video format | HEVC, AVC |

[Full Overview of Modules](https://github.com/Entree3k/edition-manager/blob/main/Edition%20Manager%20Modules.md)

## Demo
Configuration `order = Cut;Release` looks like this:

![Cut Release](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/28047dfe-a058-4cf3-8a32-ca8882edae15)

Configuration `order = Rating;Country` looks like this:

![Rating Country](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/05214007-f2ed-423e-82a3-188712933446)

Configuration `order = FrameRate;Bitrate` looks like this:

![FrameRate Bitrate](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/b843c042-b9cb-43d8-92c0-8d74c7847ffa)

Configuration `order = Resolution;AudioCodec` looks like this:

![Resolution AudioCodec](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/97606ea4-e5e0-45e4-8633-08f77181ef96)

Configuration `order = Source;DynamicRange` looks like this:

![Source DynamicRange](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/a0d845cd-39e8-45b1-bb4f-3950c51b65e1)

Configuration `order = ContentRating;Duration` looks like this:

![ContentRating Duration](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/15805123-de56-4e68-871a-cccd6bf09f9d)

Configuration `order = Release;Source;Resolution;DynamicRange;VideoCodec;FrameRate;AudioCodec;Bitrate;Size;Country` looks like this:

![Multi-module](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/11ca5070-1757-4790-a896-5da97ce976a9)

## Configuration

Edit `config/config.ini` to customize your setup:

### Server Settings
- `address`: Your Plex server URL (e.g., http://localhost:32400)
- `token`: Your Plex authentication token
- `skip_libraries`: Semi-colon separated list of libraries to skip

### Module Settings
- `order`: Control which modules are used and in what order. Use semi-colon to separated list

### Language Settings
- `excluded_languages`: Languages to exclude from detection
- `skip_multiple_audio_tracks`: Skip language tag if multiple audio tracks exist

### Performance Settings
- `max_workers`: Number of concurrent threads (4-12 recommended)
- `batch_size`: Movies to process in each batch (10-30 recommended)
- `cache_ttl`: Time to live for cache entries in seconds

Since Edition Manager only processes libraries of movie type, specify libraries of movie type to skip when needed. There is no limit to the number of modules for writing editions, so you can choose and configure them according to your needs.


#### Requirements
- Python 3.0 or higher installed.
- Necessary third-party libraries installed using the command `pip install -r requirements.txt`.

## Troubleshooting

### Common Issues

1. **Connection Errors**:
   - Verify your Plex server is running
   - Check your server address and token in config.ini
   - Ensure your network allows connections to the Plex server

2. **No Metadata Appearing**:
   - Check which modules are enabled in settings
   - Verify file naming follows expected patterns
   - Check logs for specific errors with modules

3. **Performance Issues**:
   - Adjust max_workers in settings (lower for less powerful systems)
   - Reduce batch_size for better responsiveness
   - Use the clear-cache option if cached data becomes stale

4. **Language Module Issues**:
   - Ensure the audio track is named with the proper language
   - Use a program like [mkvtoolnix](https://mkvtoolnix.download/) to rename audio tracks

## Contributing

Contributions are welcome! Feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the MIT License

## Acknowledgement

All respect to [x1ao4](https://github.com/x1ao4) for the original

## Support

If you found this helpful, consider giving it a ⭐️. Thanks for your support!
