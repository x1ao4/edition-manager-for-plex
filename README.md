# Edition Manager

In Plex, there are two concepts of "version": "[Edition](https://support.plex.tv/articles/multiple-editions/)" and "[Version](https://support.plex.tv/articles/200381043-multi-version-movies/)", but their uses are quite different.
Edition Manager
Edition Manager is a powerful tool designed to enhance your Plex media library by leveraging the Edition feature to display rich, customizable metadata for your movies.
Key Features:

Automated Metadata Extraction: Automatically retrieves and writes specified information into the Edition field, including:

Cut versions (Theatrical, Director's, Extended, Unrated, etc.)
Release versions (Special Edition, Remastered, Anniversary Edition, etc.)
Technical details (Resolution, Dynamic Range, Video/Audio Codec, Frame Rate, Bitrate, Size)
Content information (Country, Content Rating, Audience Rating, Duration)


Enhanced Visibility: Display crucial information like Dolby Vision support on mobile and TV apps, where it's typically not shown.
Flexible Sorting: Overcome Plex's single-criteria sorting limitation by incorporating multiple attributes into the Edition field.
Custom Modules: Extend functionality with user-defined modules and custom sorting options.
Non-Invasive Implementation: Achieve rich metadata display without modifying filenames.
User-Friendly Operations:

One-click addition of extra display information
Easy removal of all Edition information
Experiment with different combinations freely


Plex Pass Alternative: Utilize Edition features without a Plex Pass subscription.

Edition Manager transforms your Plex library, offering a more informative and customizable viewing experience. Whether you're distinguishing between cut versions, highlighting technical specifications, or simply enriching your movie displays, this tool provides the means to curate your library exactly as you envision it.

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

## Modules
Currently, EMP offers a total of 14 modules for selection. These include Cut, Release, Source, Resolution, DynamicRange, VideoCodec, FrameRate, AudioCodec, Bitrate, Size, Country, ContentRating, Rating, and Duration. You can choose any number of modules and arrange them in any order. If certain modules cannot retrieve information, the others will still display correctly. Customize as needed.

### Cut
The Cut module currently supports 13 types of cut versions. This module prioritizes matching cut version information based on the movie's filename. If multiple video files exist, it will use the largest file by size for matching. If cut version information cannot be found through filename, it will attempt to match using embedded video titles within the file. If cut version information still cannot be found, it will not write cut version information. The supported cut versions are:

- **Theatrical Cut**: This version is shown in theaters and is typically the most widely recognized version. It undergoes final review by producers and distributors for large-scale release.
- **Director's Cut**: This version is considered by the director to best reflect their creative intent. It may include deleted scenes or have a different narrative structure, often released after the theatrical run.
- **Producer's Cut**: Edited under the supervision of producers, this version may differ from the director's intent. Producer's cuts sometimes modify the film for commercial reasons.
- **Extended Cut**: Includes scenes cut from the theatrical release or extends certain segments. Extended editions are usually released in home video formats to provide more content to viewers.
- **Unrated Cut**: A version not reviewed by film rating boards, often containing more intense or controversial content. Unrated versions are generally released in the home entertainment market.
- **Final Cut**: This is the definitive version of the film, incorporating input from all creative teams. Final cuts may be released to commemorate important anniversaries of the film.
- **Television Cut**: Specifically edited for television broadcast, often removing or modifying content unsuitable for television audiences to comply with broadcasting standards.
- **International Cut**: Adjusted for international markets, which may include subtitles or dubbing, and modifications to address significant cultural differences.
- **Home Video Cut**: Released for home viewing, including formats like VHS, DVD, Blu-ray, etc. Home video versions may include additional content or special features not present in theatrical releases.
- **Rough Cut**: A preliminary version of the film before final editing, containing all filmed material. Rough cuts are typically for internal use, facilitating later modifications.
- **Workprint Cut**: A near-final version used for internal review or test screenings. Workprints may not yet have finalized sound, music, and visual effects.
- **Fan Edit**: A version re-edited by fans based on original film material, possibly featuring different storylines, deleted scenes, or added content to cater to specific fan preferences.
- **Redux**: A version of the film that typically extends or revises the original by restoring scenes, altering edits, or adding content to offer a different viewing experience from the original release.

### Release
The Release module currently supports 14 types of release versions. This module prioritizes matching release version information based on the movie's filename. If multiple video files exist, it will use the largest file by size for matching. If release version information cannot be found through filename, it will attempt to match using embedded video titles within the file. If multiple release versions are matched, they will be sequentially written into the release version information. If release version information still cannot be found, it will not write release version information. The supported release versions are:

- **Special Edition**: Includes additional content not present in the theatrical version, such as behind-the-scenes footage, deleted scenes, or featurettes. Special editions typically offer more viewing content for fans.
- **Restored Edition**: A version of old films digitally restored to modern visual and audio standards. This version is often used for re-releasing classic films.
- **3D Edition**: Version processed using 3D technology to provide a stereoscopic visual experience. Viewers need to wear 3D glasses for an immersive experience.
- **IMAX Edition**: Optimized for IMAX theater format, offering enhanced picture and sound quality with larger, clearer screen displays for a more impactful viewing experience.
- **Collector's Edition**: Typically includes deluxe packaging and exclusive additional content such as art books, models, or other collectibles, designed for movie enthusiasts and collectors.
- **Anniversary Edition**: A special version released to celebrate significant anniversaries of the film's release, often containing extra content and commemorative items.
- **Ultimate Edition**: The most comprehensive and complete version, containing all possible additional content such as director's commentaries, behind-the-scenes footage, deleted scenes, etc., offering the richest viewing experience.
- **Blu-ray Edition**: Released in Blu-ray disc format, providing high-definition video and audio quality, often including extra content and special features.
- **DVD Edition**: Released in DVD format, suitable for home playback devices. DVD editions typically include additional content and bonus features.
- **Limited Edition**: Released in limited quantities with unique packaging and additional content, designed for specific markets or collectors.
- **Commemorative Edition**: Released to commemorate a specific event or anniversary, featuring specially designed packaging and commemorative additional content.
- **Deluxe Edition**: Includes extensive additional content and deluxe packaging, usually offering more featurettes and behind-the-scenes footage than standard editions.
- **Director's Signature Edition**: Endorsed and personally signed by the director, often including exclusive director's commentaries and special features, with high collectible value.
- **Criterion Collection**: Distributed by Criterion Collection, focusing on high-quality film restoration and special additional content, targeting film enthusiasts and collectors.

### Source
The Source module currently supports 25 types of source versions. This module prioritizes matching source version information based on the movie's filename. If multiple video files exist, it will use the largest file by size for matching. If source version information cannot be found through filename, it will attempt to match using embedded video titles within the file. If source version information still cannot be found, it will not write source version information. The supported source versions are:

- **REMUX**: Lossless version extracted from a Blu-ray disc, without compression, maintaining the original video and audio quality.
- **BD**: Version extracted from a Blu-ray disc, with some compression applied, but offering very good video and audio quality.
- **BDRIP**: Compressed version derived from a Blu-ray disc, smaller in size but slightly lower quality compared to the Blu-ray version.
- **WEB-DL**: Version downloaded from online streaming services, offering good video and audio quality.
- **VODRIP**: Version recorded from video-on-demand services, with good video and audio quality similar to WEB-DL.
- **WEBRIP**: Version recorded from online streaming services, with lower video and audio quality compared to WEB-DL.
- **HDRIP**: Compressed version extracted from a high-definition source, offering good video and audio quality.
- **HR-HDTV**: High-resolution HDTV version, with some compression applied, better quality than regular HDTV.
- **HDTV**: High-definition version recorded from television broadcasts, good video quality but may include station watermarks and advertisements.
- **PDTV**: Version recorded from digital television broadcasts, better quality than SDTV and similar to HDTV.
- **DVD**: Version extracted from a DVD disc, offering good video and audio quality.
- **DVDRIP**: Compressed version derived from a DVD disc, with lower video and audio quality compared to DVD.
- **DVDSCR**: Version distributed to award judges or critics, relatively good video and audio quality but may include watermarks and copyright information.
- **R5**: DVD version released in Russia, good video quality but slightly inferior audio quality.
- **LDRIP**: Version extracted from LaserDisc, good video and audio quality but slightly lower than DVD.
- **PPVRIP**: Version recorded from pay-per-view services, generally good quality.
- **SDTV**: Standard-definition version recorded from television broadcasts, lower resolution but moderate quality.
- **TVRIP**: Version recorded from television broadcasts, average quality, may include station watermarks and advertisements.
- **VHSRIP**: Version extracted from VHS tapes, slightly lower video and audio quality.
- **HDTC**: High-definition version recorded from a movie theater film print, may include background noise from the theater.
- **TC**: Standard-definition version recorded from a movie theater film print, relatively lower video and audio quality.
- **HDCAM**: Version recorded using high-definition cameras in a movie theater, quality between HDTC and regular CAM.
- **HQCAM**: Version recorded using high-definition cameras in a movie theater, lower video and audio quality.
- **TS**: Version recorded using professional cameras in a movie theater, relatively good audio quality but lower video quality.
- **CAM**: Version recorded using standard cameras in a movie theater, very poor video and audio quality.

### Resolution
The Resolution module supports all resolutions recognized by Plex. This module retrieves video resolution information from the media metadata. If multiple video files exist, it retrieves resolution information from the largest file by size. If resolution information cannot be found, it will not write any resolution information. Supported resolutions include but are not limited to:

- **8K**: Including 7680 x 4320 (8K UHD) and 8192 x 4320 (8K DCI), among others.
- **4K**: Including 3840 x 2160 (4K UHD), 3996 x 2160, 4096 x 1716, and 4096 x 2160 (4K DCI), among others.
- **2.7K**: Including 2704 x 1520 and 3440 x 1440, among others.
- **2K**: Including 1998 x 1080, 2048 x 858, and 2048 x 1080 (2K DCI), among others.
- **1080P**: Including 1920 x 800, 1920 x 818, 1920 x 1034, and 1920 x 1080 (FHD), among others.
- **720P**: Including 1280 x 540, 1280 x 640, 1280 x 692, and 1280 x 720 (HD), among others.
- **576P**: Including 720 x 576 (PAL), 768 x 576, 960 x 576, and 1024 x 576, among others.
- **480P**: Including 640 x 480 (NTSC), 848 x 480, and 854 x 480, among others.
- **SD**: Including resolutions below 480P, such as 360 x 240, 426 x 240, 480 x 360, and 640 x 360, among others.

### DynamicRange
The DynamicRange module supports all dynamic ranges recognized by Plex. It retrieves dynamic range information from the movie's media metadata. When multiple video files are present, it retrieves information from the largest file by size. If dynamic range information cannot be found, it will not include any dynamic range details. Supported dynamic ranges include but are not limited to:

- **DV P8**: Dolby Vision Profile 8 offers efficient color encoding for streaming, compatible with HDR10 for broad device support, but with slightly less color performance than P5.
- **DV P7**: Dolby Vision Profile 7 is a dual-layer format designed for Blu-ray discs, providing excellent color depth and detail, requiring hardware support for playback.
- **DV P5**: Dolby Vision Profile 5 is a single-layer format optimized for streaming, offering superior color encoding compared to P8, ideal for showcasing intricate colors in Dolby Vision-native content.
- **HDR**: High Dynamic Range enhances brightness and color range of display devices, making images richer and more lifelike, enhancing immersion in viewing.
- **SDR**: Standard Dynamic Range is the traditional video format, offering limited brightness and color range but widely compatible with various devices.

Note: HDR10, HDR10+, HLG, and similar high dynamic range technologies are categorized under HDR. If a video file supports both HDR and DV, both will be included in the Edition.

### VideoCodec
The VideoCodec module supports all video codecs recognized by Plex. This module retrieves video codec information from the media metadata. If multiple video files exist, it retrieves codec information from the largest file by size. If codec information cannot be found, it will not write any codec information. Supported video codecs include but are not limited to:

- **AV1**: AOMedia Video 1, an open-source codec developed by the Alliance for Open Media, known for high compression efficiency and excellent video quality.
- **HEVC**: Also known as H.265, High Efficiency Video Coding, providing high compression efficiency and good video quality.
- **VP9**: Developed by Google, an open-source codec with high compression efficiency, commonly used on platforms like YouTube.
- **H264**: Also known as H.264 or AVC, a common codec for high-definition video encoding, with high compression efficiency widely used in streaming and video storage.
- **VC1**: Also known as SMPTE 421M, a video codec developed by Microsoft, offering good compression efficiency, commonly used in Blu-ray discs and online video.
- **MPEG4**: MPEG-4 Part 2, widely used for video streaming and discs, providing good compression efficiency.
- **SVQ3**: Sorenson Video 3, an early video compression format known for lower compression efficiency.
- **WMV3**: Also known as Windows Media Video 9, Microsoft's video codec with moderate compression efficiency.
- **WMV2**: Also known as Windows Media Video 8, an earlier Microsoft video codec with lower compression efficiency.
- **WMV1**: Also known as Windows Media Video 7, the earliest Microsoft video codec with lower compression efficiency.
- **MPEG2**: Also known as H.262, a standard codec for DVDs and some TV broadcasts, known for lower compression efficiency.
- **MPEG1**: An early video compression format, commonly used for VCDs, known for very low compression efficiency.
- **RV40**: RealVideo 4.0, a codec developed by RealNetworks, known for lower compression efficiency.

### FrameRate
The FrameRate module supports all frame rates recognized by Plex. This module retrieves frame rate information from the media metadata. If multiple video files exist, it retrieves frame rate information from the largest file by size. If frame rate information cannot be found, it will not write any frame rate information. Supported frame rates include but are not limited to:

- **240P**: Displays 240 frames per second, used for super slow-motion video capture to capture details of fast-moving subjects.
- **120P**: Displays 120 frames per second, used for high frame rate video capture and playback, common in high-end TVs and virtual reality content, providing an extremely smooth visual experience.
- **100P**: Displays 100 frames per second, primarily used for certain high frame rate TV broadcasts.
- **72P**: Displays 72 frames per second, uncommon but used in certain special movie screenings.
- **60P**: Displays 60 frames per second, commonly used for high-speed motion video, sports events, and video games, offering extremely smooth motion performance.
- **50P**: Displays 50 frames per second, used in European HD TV standards and some high frame rate video content.
- **48P**: Displays 48 frames per second, previously used in some movies like "The Hobbit" series, providing smoother motion than 24 frames per second.
- **30P**: Displays 30 frames per second, suitable for NTSC video standard, widely used in TV broadcasts in North America and Japan.
- **25P**: Displays 25 frames per second, suitable for PAL video standard, primarily used in Europe, China, Australia, and other PAL regions for TV and video content.
- **24P**: Displays 24 frames per second, traditional film frame rate commonly used in movie production, providing a unique cinematic feel.
- **15P**: Displays 15 frames per second, used for low-bandwidth video streaming and some webcams.
- **12P**: Displays 12 frames per second, previously used in early animations and low-bandwidth video transmissions.
- **10P**: Displays 10 frames per second, primarily used for very low-bandwidth video transmission and some surveillance cameras.
- **5P**: Displays 5 frames per second, used for extremely low-bandwidth surveillance and video transmission.

### AudioCodec
The AudioCodec module supports all audio codecs recognized by Plex. This module retrieves audio codec information from the media metadata. If multiple video files exist, it retrieves audio codec information from the largest file by size. If multiple audio streams exist, it retrieves the audio codec information from the stream with the highest bitrate (preferring multichannel streams). If audio codec information cannot be found, it will not write any audio codec information. Supported audio codecs include but are not limited to:

- **DTS-HD MA**: DTS-HD Master Audio, lossless encoding providing cinematic sound quality, commonly used in Blu-ray discs.
- **TRUEHD**: Dolby TrueHD, Dolby's lossless encoding offering high-fidelity sound quality, also common in Blu-ray discs.
- **FLAC**: Free Lossless Audio Codec, open-source lossless encoding widely used for music archiving and high-fidelity audio tracks.
- **PCM**: Pulse Code Modulation, lossless encoding offering original sound quality, commonly used in CDs and DVDs.
- **DTS-HD HRA**: DTS-HD High Resolution Audio, lossy encoding with sound quality superior to standard DTS.
- **DTS-ES**: DTS Extended Surround, an extension of DTS that adds a rear center channel.
- **EAC3**: Enhanced AC-3, also known as Dolby Digital Plus, enhanced version of Dolby Digital offering higher compression ratio and better audio quality.
- **DTS**: Digital Theater Systems, digital cinema system encoding widely used in movies and DVDs.
- **AC3**: Also known as Dolby Digital, Dolby's digital encoding format commonly used in DVDs and digital TV broadcasts.
- **HE-AAC**: High-Efficiency Advanced Audio Codec, advanced audio encoding with higher data compression rate compared to AAC, widely used in streaming.
- **AAC**: Advanced Audio Codec, successor to MP3 for high-quality audio encoding, widely used in streaming.
- **MP3**: MPEG-1 Audio Layer 3, the most common lossy audio codec widely used for music playback.
- **VORBIS**: Ogg Vorbis, open-source lossy encoding format commonly used in gaming and network audio.
- **WMAPRO**: Windows Media Audio Professional, Microsoft's lossy encoding offering higher audio quality.
- **COOK**: RealAudio COOK, RealNetworks' lossy encoding primarily used in early streaming.
- **MP2**: MPEG-1 Audio Layer 2, early lossy encoding format commonly used in broadcasting and VCD.
- **WMAV2**: Windows Media Audio Version 2, a variant of WMA offering higher audio compression rate and lower audio quality.
- **WMA**: Windows Media Audio, Microsoft's lossy encoding widely used on Windows platforms.

Note: When writing Edition, the audio codec will display the corresponding channel information of the audio stream, such as TRUEHD 7.1, AC3 5.1, AAC Stereo, etc.

### Bitrate
The Bitrate module retrieves the bitrate information of video files from the media metadata recognized by Plex. If multiple video files exist, it retrieves the bitrate information from the largest file by size. If bitrate information cannot be found, it will not write any bitrate information (bitrate units are in Kbps, Mbps).

### Size
The Size module retrieves the size information of video files from the media metadata. If multiple video files exist, it retrieves the size information from the largest file by size (size units are in B, KB, MB, GB).

### Country
The Country module retrieves the country (or region) information of movies from the movie metadata. If multiple countries exist, it sequentially writes the country information. If country information cannot be found, it will not write any country information.

### ContentRating
The ContentRating module retrieves the content rating information of movies from the movie metadata. If content rating information cannot be found, it will not write any content rating information. Supported content ratings include but are not limited to:

#### Movie Ratings (MPAA)
- **G**: General Audiences – Suitable for all ages. Contains nothing that would offend parents for viewing by children.
- **PG**: Parental Guidance Suggested – Some material may not be suitable for children. Parents are urged to give "parental guidance."
- **PG-13**: Parents Strongly Cautioned – Some material may be inappropriate for children under 13. Parents are urged to be cautious.
- **R**: Restricted – Restricted to viewers over the age of 17 or accompanied by a parent or adult guardian. Contains strong language, violence, or sexual content.
- **NC-17**: Adults Only – No one 17 and under admitted. Contains explicit sexual or violent content.
- **NR**: Not Rated – The film has not been submitted for rating to the MPAA.
- **Unrated**: A version not officially rated by organizations like the MPAA, may contain content not included in the original rating.

#### TV Show Ratings (TV Parental Guidelines)
- **TV-Y**: Television for All Children – Suitable for all children. Typically suitable for ages 2-6.
- **TV-Y7**: Directed to Older Children – Suitable for children age 7 and above. May contain mild fantasy violence or infrequent use of mild language.
- **TV-Y7-FV**: Directed to Older Children - Fantasy Violence – Suitable for children age 7 and above. Contains fantasy violence.
- **TV-G**: General Audience – Suitable for all ages. Contains little or no violence, no strong language, and little or no sexual dialogue or situations.
- **TV-PG**: Parental Guidance Suggested – Some material may not be suitable for children. Parents are urged to provide "parental guidance."
- **TV-14**: Parents Strongly Cautioned – Contains some material that many parents would find unsuitable for children under 14.
- **TV-MA**: Mature Audience Only – This program is specifically designed to be viewed by adults and may be unsuitable for children under 17. May contain crude indecent language, explicit sexual activity, or graphic violence.

#### Other Rating Standards
- **Approved**: Approved by the Motion Picture Association or other relevant authorities. Suitable for public viewing, specific content may vary depending on release era.
- **18+**: Restricted to viewers 18 years and older. Contains adult-oriented content.
- **AO**: Adults Only – Used for video game ratings, suitable only for adults.

Note: The above ratings are based on the U.S. rating system. Ratings systems in other regions may vary.

### Rating
The Rating module retrieves the audience rating information of movies from the movie metadata (using the configured rating source from the database). If rating information cannot be found, it will not write any rating information (ratings will be converted to a 10-point scale).

### Duration
The Duration module retrieves the duration information of video files from the media metadata of movies. If multiple video files exist, it retrieves the duration information from the largest file by size. If duration information cannot be found, it will not write any duration information (duration is measured in minutes).

## Features
The EMP operates in three modes: `add editions for all movies (all)`, `add editions for new movies (new)`, and `reset editions for all movies (reset)`:

- **add editions for all movies**: Based on user configuration, this mode adds editions for all movies in libraries excluding those configured to be skipped. Movies with existing editions will be skipped.
- **add editions for new movies**: This mode utilizes Webhooks to listen for server events in real-time, capturing metadata for newly added items. It then adds editions only for newly added movies (excluding those in libraries configured to be skipped).
- **reset editions for all movies**: According to user settings, this mode resets (removes) editions for all movies in libraries excluding those configured to be skipped.

Note: The `add editions for new movies` mode requires the server administrator account to be subscribed to Plex Pass in order to use.

## Config
Before using EMP, please configure `/config/config.ini` according to the following example:
```
[server]
# Address of the Plex server, formatted as http://server IP address:32400 or http(s)://domain:port
address = http://127.0.0.1:32400
# Token of the Plex server for authentication
token = xxxxxxxxxxxxxxxxxxxx
# Specify libraries to skip, format should be LibraryName1;LibraryName2;LibraryName3, leave empty if no libraries need to be skipped
skip_libraries = Cloud Movie;Concert
# Language setting, 'zh' for Chinese, 'en' for English
language = en

[modules]
# Specify modules to write and their order, format should be Module1;Module2;Module3, optional modules include Cut, Release, Source, Resolution, DynamicRange, VideoCodec, FrameRate, AudioCodec, Bitrate, Size, Country, ContentRating, Rating, Duration
order = Source;DynamicRange
```
Since EMP only processes libraries of movie type, specify libraries of movie type to skip when needed. There is no limit to the number of modules for writing editions, so you can choose and configure them according to your needs.

When running in `add editions for new movies` mode, EMP creates a Flask web server that listens on port `8089` to receive `library.new` events sent by the Plex server. This allows it to capture metadata for newly added items and process them accordingly.

If port `8089` is already occupied by another service, you may need to modify the `port=8089` on the ninth last line of `edition-manager-for-plex.py` (when running via Python script) or adjust port mapping (when running via Docker container) to change the listening port.

## How to Run
You can run EMP using Docker containers or Python scripts. Docker containerization is recommended for its ease of use and scalability. Detailed instructions for each method are provided below.

### Running via Docker Container

#### Requirements
- Docker and Docker Compose installed.

#### Docker Compose
- edition-manager-for-plex (Plex Pass subscribers)
  
   ```
   version: "2"
   services:
     emp-all:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-all
       command: python edition-manager-for-plex.py --all
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /custom/directory/edition-manager-for-plex/config:/app/config
     emp-new:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-new
       command: python edition-manager-for-plex.py --new
       ports:
         - 8089:8089
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /custom/directory/edition-manager-for-plex/config:/app/config
       restart: unless-stopped
   networks: {}
   ```
- edition-manager-for-plex（Non-Plex Pass subscribers）
  
   ```
   version: "2"
   services:
     emp-scheduler:
       image: mcuadros/ofelia:latest
       container_name: emp-scheduler
       depends_on:
         - emp-all
       command: daemon --docker -f label=com.docker.compose.project=${COMPOSE_PROJECT_NAME}
       labels:
         ofelia.job-run.emp-all.schedule: 0 30 22 * * *
         ofelia.job-run.emp-all.container: emp-all
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock:ro
       restart: unless-stopped
     emp-all:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-all
       command: python edition-manager-for-plex.py --all
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /custom/directory/edition-manager-for-plex/config:/app/config
   networks: {}
   ```
- edition-manager-for-plex-reset
  
   ```
   version: "2"
   services:
     emp-reset:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-reset
       command: python edition-manager-for-plex.py --reset
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /custom/directory/edition-manager-for-plex/config:/app/config
   networks: {}
   ```

#### Usage
With EMP, you can write edition information as well as remove it. Since Docker automatically starts all containers within the stack upon stack initialization, the functions for writing and removing need to be deployed separately. First, deploy `edition-manager-for-plex` to write edition information, then deploy `edition-manager-for-plex-reset` when needed to remove edition information (upon deployment, it will immediately execute a `reset editions for all movies` once. You can also use `docker-compose up --no-start` to deploy this container, which will not run immediately after deployment; start the container only when needed).

- edition-manager-for-plex

  1. In the Plex server settings, navigate to `Webhooks`, click on `Add Webhook`, and enter your Flask server address `http://Docker host IP address:8089` and `Save Changes`. (Non-Plex Pass subscribers do not need to fill this.)
  2. Download the `/compose/edition-manager-for-plex/compose.yaml` file from the repository (Plex Pass subscribers should delete the `emp-scheduler` section; non-Plex Pass subscribers should delete the `emp-new` section) and save it in a folder named `edition-manager-for-plex`.
  3. Open `compose.yaml` with a text editor and replace `/custom/directory/edition-manager-for-plex/config` with a directory on your host machine where configuration files will be stored. (Both `emp-all` and `emp-new` should use the same directory.)
  4. Open the terminal or command line tool, use the `cd` command to switch to the directory where `compose.yaml` is located.
  5. Use the command `docker-compose up -d` to deploy and start the edition-manager-for-plex stack.
  6. Open `/custom/directory/edition-manager-for-plex/config/config.ini` with a text editor, fill in your Plex server address (`address`) and [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) (`token`), set the modules to write edition information and their order (`order`), and optionally fill in other configuration options as needed.
  7. Restart the edition-manager-for-plex stack to start running properly.

- edition-manager-for-plex-reset

  1. Download the `/compose/edition-manager-for-plex-reset/compose.yaml` file from the repository and save it in a folder named `edition-manager-for-plex-reset`.
  2. Open `compose.yaml` with a text editor and replace `/custom/directory/edition-manager-for-plex/config` with a directory on your host machine where configuration files will be stored. (Use the same directory as `emp-all` and `emp-new`.)
  3. Open the terminal or command line tool, use the `cd` command to switch to the directory where `compose.yaml` is located.
  4. Use the command `docker-compose up -d` to deploy and start the edition-manager-for-plex-reset stack. (If `/custom/directory/edition-manager-for-plex/config/config.ini` is correctly configured, the stack will operate properly; if not configured, fill in the configuration information first, then restart the stack for proper operation.)

#### Instructions
EMP consists of four containers: `emp-all`, `emp-new`, `emp-scheduler`, and `emp-reset`, each designed to handle different tasks. Upon stack deployment, these containers will have slightly different running states.

- The `emp-all` container is used for the `add editions for all movies` task. It runs this task once after startup, processing all movies within the set scope (adding edition information), and displays the library information and processing results in the terminal or logs. It will stop running after completing the task. You can start it at any time to run the `add editions for all movies` task, and it will stop after each run. If you have configured `emp-scheduler`, `emp-all` will also run once automatically at each scheduled task time.
- The `emp-new` container is used for the `add editions for new movies` task. After startup, it will create a Flask server to listen for events from the Plex server. When there are new movies on the Plex server, it will automatically process the new movies (add edition information) and display the processing results in the terminal or logs. After processing, it will continue to listen for events from the Plex server and handle any new movies as they arrive, then resume listening.
- The `emp-scheduler` container is used to set/trigger scheduled tasks for `add editions for all movies`. After startup, it will create a scheduled task to run `emp-all` at a default setting of `0 30 22 * * *`, which means it will run once daily at 10:30 PM. You can customize the running frequency by modifying the cron expression, such as `"@every 3h"` for every 3 hours or `"@every 30m"` for every 30 minutes. It will start the `emp-all` container at the scheduled task time and synchronize the `emp-all` log information in the terminal or logs, then continue running.
- The `emp-reset` container is used for the `reset editions for all movies` task. It runs this task once after startup, processing all movies within the set scope (resetting/removing edition information), and displays the library information and processing results in the terminal or logs. It will stop running after completing the task. You can start it at any time to run the `reset editions for all movies` task, and it will stop after each run.

You can select and configure these four containers as needed. If certain functions are not required, simply delete the corresponding parts in the Compose file before deployment.

### Running via Python Script

#### Requirements
- Python 3.0 or higher installed.
- Necessary third-party libraries installed using the command `pip3 install -r requirements.txt`.

#### Usage
1. Download the latest release package from [Releases](https://github.com/x1ao4/edition-manager-for-plex/releases) and extract it to a local directory.
2. Open the `/config/config.ini` file in the directory using a text editor, fill in your Plex server address (`address`) and [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) (`token`), set the modules to write edition information and their order (`order`), and optionally fill in other configuration options as needed.
3. In the Plex server settings, navigate to `Webhooks`, click on `Add Webhook`, and enter your Flask server address `http://IP address of the device running the script:8089` and `Save Changes`. (Non-Plex Pass subscribers do not need to fill this.)
4. Open a terminal or command line tool, use the `cd` command to switch to the directory where the script is located.
5. Use the command `python3 edition-manager-for-plex.py --all` to run the `add editions for all movies` task. The script will process all movies within the configured scope (adding edition information) and display library information and processing results in the console. It will stop running after completing the task.
6. Use the command `python3 edition-manager-for-plex.py --new` to run the `add editions for new movies` task. The script will create a Flask server to listen for events from the Plex server. When there are new movies on the Plex server, the script will automatically process the new movies (adding edition information) and display the processing results in the console. After processing, it will continue to listen for events from the Plex server and handle new movies as they arrive, then resume listening.
7. Use the command `python3 edition-manager-for-plex.py --reset` to run the `reset editions for all movies` task. The script will process all movies within the configured scope (resetting/removing edition information) and display library information and processing results in the console. It will stop running after completing the task.

#### Quick Start
PC users can quickly start tasks by double-clicking the provided scripts:

- To run the `add editions for all movies` task, double-click `emp-all.bat (Win)` or `emp-all.command (Mac)`.
- To run the `add editions for new movies` task, double-click `emp-new.bat (Win)` or `emp-new.command (Mac)`.
- To run the `reset editions for all movies` task, double-click `emp-reset.bat (Win)` or `emp-reset.command (Mac)`.

#### Automation
For convenience, you can set up EMP to run automatically using crontab or other task scheduling tools.

- Add Editions for All Movies (Mac)
  
  1. Open the crontab file in the terminal with the command `crontab -e`.
  2. Press `i` to enter insert mode and add the line `30 22 * * * /path/to/emp-all.command > /dev/null 2>&1`. (Replace `/path/to/emp-all.command` with the actual path to your script.)
  3. Press `Esc` to exit insert mode, type `:wq`, and press `Enter` to save changes and exit the editor.

  This sets up a scheduled task to run the `add editions for all movies` script every day at 10:30 PM. You can customize the frequency by modifying the time expression, such as `0 */3 * * *` to run every 3 hours or `*/30 * * * *` to run every 30 minutes. (The script will run in the background.)

- Add Editions for New Movies (Mac)
  
  1. Open the `emp-new.command` file with a text editor, add `sleep 10` on the second line, save the changes, and close the file.
  2. Open the crontab file in the terminal with the command `crontab -e`.
  3. Press `i` to enter insert mode and add the line `@reboot /path/to/emp-new.command`. (Replace `/path/to/emp-new.command` with the actual path to your script.)
  4. Press `Esc` to exit insert mode, type `:wq`, and press `Enter` to save changes and exit the editor.

  This sets the `add editions for new movies` script to run on Mac startup, with a 10-second delay to ensure the Plex server starts before the script. (The script will run in the background.)

- Add Editions for All Movies (NAS)
  
  Use the built-in task scheduler to add a scheduled task for `add editions for all movies`. After adding the task, enter `python3 /path/to/edition-manager-for-plex.py --all` in the `Run Command - User-Defined Script` field, then set the desired run time. (Replace `/path/to/edition-manager-for-plex.py` with the actual path to your script.)
  
- Add Editions for New Movies (NAS)
  
  Use the built-in task scheduler to set `add editions for new movies` to run at startup. After adding the task, enter `sleep 10 && python3 /path/to/edition-manager-for-plex.py --new` in the `Run Command - User-Defined Script` field. This ensures the script runs 10 seconds after NAS startup, giving the Plex server time to start first. (Replace `/path/to/edition-manager-for-plex.py` with the actual path to your script.)

If the scripts fail to run as scheduled or on startup, you may need to replace `python3` with the full path to the Python interpreter. You can find the actual path to `python3` using the `which python3` command in the Mac terminal or NAS SSH.

## Notes
- Ensure you provide the correct Plex server address and the correct X-Plex-Token.
- Ensure you provide the correct library names and fill them in as required.
- Ensure you correctly set the language and module information as required.
- If the script cannot connect to the Plex server, check your network connection and ensure the server is accessible.
- Use the server administrator account's X-Plex-Token to run the script to ensure you have sufficient permissions for operations.
- The edition field will be locked after being added. If modifications are needed, Plex Pass subscribers can manually unlock the edition field and then modify it; non-Plex Pass subscribers do not support manual modification of the edition field. To modify the edition modules or their order for all movies, first reset the editions, then modify the configuration file, and finally rewrite the editions.
- If Windows users see no response after running the Python script, try replacing `python3` with `python` in the run command or start script.

## Support
If you found this helpful, consider buying me a coffee or giving it a ⭐️. Thanks for your support!

<img width="399" alt="Support" src="https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/be5aa968-3dc3-4dcc-91cc-506354000a6a">
<br><br>
<a href="#edition-manager-for-plex-en">Back to Top</a>
