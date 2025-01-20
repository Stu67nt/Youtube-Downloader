# Youtube-Downloader

**Intro/About**
  
This program can be used to download Youtube videos and audio through ytdlp. It can integrate thumbnails into the video as well as subtitles. Furthermore, it has support for downloading private videos as well as access to Sponsor block to identify and remove typically undesired parts of a video such as the intro, sponsored segments, ect.

# Download & Usage

**This program has only been tested and compiled for Windows 11**

<del>
To download this program:
1.  Go to the releases section of this github page and download the latest release of the program.
2.  Once downloaded locate it in your downloads folder or your browser should have a pop up which lets you view the file in file explorer.
3.  Once located extract it to your desired location.
4.  Do not move the executable or any of the other files/folders outside of the main folder. If you wish to move the directory it is in move the whole folder.
5.  Open the exe
The next steps are not required but **HIGHLY RECCOMENDED**
6.  CLick on 'Edit Config'
7.  In the empty quotation marks next to "downloadDirectory" put in the directory where you want your files to be installed. If this is not done the downloads will be placed in the temp folder.<br>
    For reference the line you are looking for will look like this:<br>
    "downloadDirectory": "C:\Users\John Smith\Videos",
8.  Enter the name of your normal browser on the "browserCookies" part. This is **ONLY** used for getting authentication details for private downloads. If you will never download private videos you noo not need to provide this information
9.  Whilst this program can be used without ffmpeg and ffprobe it is **HEAVILY** reccomended for you to install them and put the executeables in the same directory as this program as it unlocks many more functionalities. <br> Found here: https://www.ffmpeg.org/download.html<br>
10. Tinker with the other settings as you wish. Arguments for each will be provided below.
</del>

**Config Arguments:**
The config by default would look something like this.
  
         {
          "quality": 720,
          "downloadDirectory": "temp",
          "sponsorblockSkipCatagories": [],
          "validLangs": [],
          "needThumbnail": false,
          "needSubtitles": false,
          "videoFileFormat": "mp4",
          "audioFileFormat": "m4a",
          "subtitlesFileFormat": "vtt",
          "needCookies": false,
          "browserCookies": "",
          "verbose": true
        }
You should not change any of the catagory names such as "quality", "validLangs", ect. You shoud not remove any of the colons, double quote marks, curly brackets, ect.<br>
What you can modify however, is the attributes they are given. How you can modify them and what they each mean will be explained below:<br>

        quality: The preferred quality the video is downloaded at. You can change the number for any
        other common video quality. Eg: 1080p, 480p 
        Example: "quality": 720,

        downloadDirectory: The place where downloads are moved to when completed. 
        Default will place them in temp.
        Example: "downloadDirectory": 'C:/Users/John Smith/Videos',

        sponsorblockSkipCatagories: Potentially unwanted things in a video which can be cut out is 
        avaliable in database. 
        Default config cuts no portions out.
        possible options (can include any combination of choosing): 
        "interaction", "intro", "music_offtopic", "outro", "preview", "selfpromo", "sponsor", "filler"
        Examples: "sponsorblockSkipCatagories": ["interaction", "intro", "music_offtopic", "outro", 
                                                "preview", "selfpromo", "sponsor", "filler"],
                  "sponsorblockSkipCatagories": ["selfpromo",
                                                 "sponsor"],

        validLangs: Languages to download subtitles in if avaliable. NOTE: needSubtitles has to be 
        enables for subtitles to download. 
        Default config leaves this empty.
        Possible Options (as many as wanted): The 2 letter codes from this 'website' should work 
        https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt 
        Example: "validLangs": ["en", "fr", "de"],
        
        needThumbnail: Gives a thumbnail to the download so it looks pretty in file explorer if possible.
        (Requires FFmpeg to function when true)
        Default is off/false
        options (must have only one): true (requires FFmpeg), false
        Example: "needThumbnail": true,

        needSubtitles: Gives and embeds subtitles into the video if possible. 
        (Requires FFprobe to function when true)
        Default is off/false
        options (must have only one): true (requires FFprobe), false
        Example: "needSubtitles": true,

        videoFileFormat: Perferred format the video is downloaded in if possible. 
        Default is "mp4"
        options (must have only one): "avi", "flv", "mkv", "mov", "mp4", "webm"
        Example: "videoFileFormat": "webm",
        
        audioFileFormat: Perferred format the audio is downloaded in if possible. 
        Default is "m4a"
        options (must have only one): "aiff", "alac", "flac", "m4a", "mka", "mp3", "ogg", "opus", "wav"
        Example: "audioFileFormat": "wav",

        subtitlesFileFormat: Perferred format the subtitles are downloaded in if possible. 
        Default is "vtt",
        options (must have only one): "srt", "vtt", "ass", "lrc"
        Example: "subtitlesFileFormat": "vtt",
        
        needCookies: Takes cookies from your specified browser in browserCookies to 
        authenticate you in order to download private things. (Need to fill "browserCookies")
        Default is off/false
        options (must have only one): true, false
        Example: "needCookies": true,
       
        browserCookies: Tells program which browser to take cookies from.
        options (must have only one): brave, chrome, chromium, edge, firefox, opera, safari, vivaldi, whale
        Example: "browserCookies": "brave",

        verbose: Gives a more detailed logs for the download process to help debug.
        default: true
        options: true, false
        Example: "verbose": false

# Contributions
Umm idk don't? BUt feedback on how shit my code is would be very nice. If i have the time or will I might carry onworking on this
