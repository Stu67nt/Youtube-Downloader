import os
import shutil
import time
import logging
import json
import threading
import tkinter as tk
from tkinter import ttk
from tabnanny import verbose
import yt_dlp


########################################################################################################################
"""Youtube API calls (Future Use)"""
########################################################################################################################
# (Currently diesnt work due to compiling errors with Google api module)
def currentTrending200(apiKey):
    """Returns current top 200 trending videos in a JSON format as a string."""
    # Quota Cost: 4
    apiServiceName = "youtube"
    apiVersion = "v3"
    youtube = googleapiclient.discovery.build(apiServiceName, apiVersion, developerKey=apiKey)

    nextPageToken = None
    output = ""
    while True:
        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            pageToken=nextPageToken
        )
        response = request.execute()
        output += str(response)
        try:
            nextPageToken = response["nextPageToken"]
        except KeyError:
            break

    youtube.close()
    return output

def findChannelId(apiKey, channelHandle):
    """Finds the channel id using the channels unique handle"""
    # Quota Cost: 4
    apiServiceName = "youtube"
    apiVersion = "v3"

    youtube = googleapiclient.discovery.build(apiServiceName, apiVersion, developerKey=apiKey)
    print("Finding Channel Id...")
    request = youtube.channels().list(
        part = "id",
        forHandle = channelHandle,
        maxResults = 1
    )
    response = request.execute()
    id = response["items"][0]["id"]
    youtube.close()
    print("Found Channel Id")
    return id

def channelPlaylists(apiKey, channelId):
    """Returns json on all channel's playlists for video"""
    # Quota Cost: (totalResults/resultsPerPage).ceil()
    apiServiceName = "youtube"
    apiVersion = "v3"

    youtube = googleapiclient.discovery.build(apiServiceName, apiVersion, developerKey=apiKey)
    nextPageToken = None
    output = ""
    print("Compiling Playlists")
    while True:
        request = youtube.playlists().list(
            part = "snippet, contentDetails, id",
            channelId = channelId,
            pageToken = nextPageToken
        )
        response = request.execute()
        output += str(response)
        try:
            nextPageToken = response["nextPageToken"]
        except KeyError:
            break
    youtube.close()
    return output

########################################################################################################################
"""Downloads"""
########################################################################################################################

def download(videoURL:str, directory:str, needCookies:bool, attemptCounter:int, quality:int=720,
             needSubtitles:bool=False, needThumbnail:bool=False, videoFileFormat:str="mp4",
             audioFileFormat:str="m4a", subsFileFormat:str="vtt", validLangs=None, removeSegments:set={},
             browser:str=None, verbose:bool=True, downloadStyle:str="v+a"):
    """Downloads a YouTube video specified by the URL"""
    match downloadStyle.lower():
        case "v+a":
            downloadStyle = f'bestvideo[ext={videoFileFormat}][height={quality}]+bestaudio[ext={audioFileFormat}]/best'
        case "a":
            downloadStyle = f'bestaudio[ext={audioFileFormat}]/bestaudio'
        case "v":
            downloadStyle = f'bestvideo[ext={videoFileFormat}][height={quality}]/bestvideo'
        case _:
            downloadStyle = f'bestvideo[ext={videoFileFormat}][height={quality}]+bestaudio[ext={audioFileFormat}]/best'

    tempDirectory = str(os.path.abspath(os.getcwd())) + "\\temp\\"
    if needCookies:
        dloadConfig = {
        # Configuring the filename codes https://yt-dlp.eknerd.com/docs/Basic%20Usage/output-templates
            'outtmpl': {'pl_thumbnail': '',
                        'default': f'{tempDirectory}%(title)s.%(ext)s'},
            'format': downloadStyle,
            'writesubtitles': needSubtitles,
            'subtitleslangs': validLangs,
            'subtitlesformat': subsFileFormat,
            'writethumbnail': needThumbnail,
            'cookiesfrombrowser': (browser, None, None, None),
            'extractor_args': {'youtubetab': {'skip': ['authcheck']}},
            'postprocessors': [{'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
                               {'already_have_subtitle': False, 'key': 'FFmpegEmbedSubtitle'},
                               {'api': 'https://sponsor.ajay.app',
                                'categories': removeSegments,
                                'key': 'SponsorBlock',
                                'when': 'after_filter'},
                               {'force_keyframes': False,
                                'key': 'ModifyChapters',
                                'remove_chapters_patterns': [],
                                'remove_ranges': [],
                                'remove_sponsor_segments': removeSegments,
                                'sponsorblock_chapter_title': '[SponsorBlock]: '
                                                              '%(category_names)l'}
                               ],
            'logger': logging.getLogger(__name__),
            'progress_hooks': [progressHook],
            'verbose': verbose,
            'writeautomaticsub': needSubtitles,
            'ignoreerrors': 'only_download',
        }
    else:
        dloadConfig = {
        # Configuring the filename codes https://yt-dlp.eknerd.com/docs/Basic%20Usage/output-templates
            'outtmpl': {'pl_thumbnail': '',
                        'default': f'{tempDirectory}%(title)s.%(ext)s'},
            'format': downloadStyle,
            'writesubtitles': needSubtitles,
            'subtitleslangs': validLangs,
            'subtitlesformat': subsFileFormat,
            'writethumbnail': needThumbnail,
            'postprocessors': [{'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
                               {'already_have_subtitle': False, 'key': 'FFmpegEmbedSubtitle'},
                               {'api': "https://sponsor.ajay.app",
                                'categories': removeSegments,
                                'key': 'SponsorBlock',
                                'when': 'after_filter'},
                               {'force_keyframes': False,
                                'key': 'ModifyChapters',
                                'remove_chapters_patterns': [],
                                'remove_ranges': [],
                                'remove_sponsor_segments': removeSegments,
                                'sponsorblock_chapter_title': '[SponsorBlock]: '
                                                              '%(category_names)l'}
                               ],
            'logger': logging.getLogger(__name__),
            'progress_hooks': [progressHook],
            'verbose': verbose,
            'writeautomaticsub': needSubtitles,
            'ignoreerrors': 'only_download',
        }
    try:
        print("Initalising Download")
        ydl = yt_dlp.YoutubeDL(dloadConfig)
        ydl.download(videoURL)
        print("Download Success! Moving files to correct location.")
        for item in os.listdir(path=tempDirectory):
            if item not in os.listdir(path=directory):
                print(f"Moving {item} to {directory}. ")
                moveFile(item, tempDirectory, directory)
                print(f"Moved {item} successfully!")
            else:
                print(f"Moving file {item} failed. Clashing file names found.\n"
                      f"Downloads can be manually moved from {tempDirectory}")
        return 0

    except yt_dlp.utils.DownloadError as err:
        print(f"Download Failed: {err}")
        return -3

    except yt_dlp.webvtt.ParseError as err:
        if attemptCounter <= 3:
            print("Download Failed. Attempting with default settings...")
            attemptCounter += 1
            download(videoURL, directory, True, attemptCounter, quality=quality)
        else:
            print("Download didnt work. Turn on verbose in config and figure it out lmao.")
            return -2
    except yt_dlp.utils.PostProcessingError as err:
        for item in os.listdir(path=tempDirectory):
            if item not in os.listdir(path=directory):
                print(f"Moving {item} to {directory}. ")
                moveFile(item, tempDirectory, directory)
                print(f"Moved {item} successfully!")
            else:
                print(f"Moving file {item} failed. Clashing file names found.\n"
                      f"Downloads can be manually moved from {tempDirectory}")

    except Exception as err:
        print(err)
        if attemptCounter <= 3:
            print("Download Failed. Attempting with default settings...")
            attemptCounter += 1
            download(videoURL, directory, True, attemptCounter, quality=quality)
        else:
            print("Download didnt work. Turn on verbose in config and figure it out lmao.")
        return -1

# arguments for download() are handled within the function to satisfy tkinter.
def downloadWrapper():
    """Used by tkinter to call downloader() without arguments"""
    url = urlEnt.get()
    config = configReader("config.json")
    directory = config["downloadDirectory"]
    needCookies = config["needCookies"]
    quality = config["quality"]
    needSubtitles = config["needSubtitles"]
    needThumbnail = config["needThumbnail"]
    videoFileFormat = config["videoFileFormat"]
    audioFileFormat = config["audioFileFormat"]
    subsFileFormat = config["subtitlesFileFormat"]
    validLangs = config["validLangs"]
    removeSegments = config["sponsorblockSkipCatagories"]
    browser = config["browserCookies"]
    verbose = config["verbose"]
    attemptCounter = 1  # Used for retrying downloads multiple times in case defaulting settings works
    downloadStyle = downloadMethod.get()
    successCode=download(url, directory, needCookies, attemptCounter, quality, needSubtitles, needThumbnail,
                                   videoFileFormat, audioFileFormat, subsFileFormat, validLangs, removeSegments,
                                   browser, verbose, downloadStyle)
    if successCode != 0:
        print("An error occoured check the latest download log file more information.")

########################################################################################################################
"""Downloads Utils"""
########################################################################################################################
def moveFile(fileName:str, currentDirectory:str, targetDirectory:str):
    """Moves files using shutil.move"""
    currentDirectory = currentDirectory+f"/{fileName}"
    shutil.move(currentDirectory, targetDirectory)
    return 0

def createConsoleLog():
    """Creates a file for storing logs of console. Returns the file path of the created txt file."""
    print("Creating Console Log")
    timestr = time.strftime("%Y.%m.%d-%H%M%S")
    filePath = os.path.join("ConsoleLogs/", timestr + ".txt")
    print("Created Console Log")
    return str(filePath)

def progressHook(d):
    """Used to track what percent of the downloads are complete.
    Used by downloader() which does voodoo magic shit"""
    if d['status'] == 'finished':
        progressLabel.config(text="")
        progress['value'] = 0
    elif d['status'] == 'downloading':
        progressLabel.config(text=f"Downloading {d["tmpfilename"]}")
        # Removes the non number chars from the string then converts it into a float to update progress bar
        progress['value'] = float((d["_percent_str"]).replace(" ", "").replace("%", ""))
    root.update()

# Embedded Functions used here because for config editior GUI buttons to work the functions have to be there locally.
def configEditor():
    def updateConfig():
        """Validates input is in json and writes it to config.json"""""
        text = configEnt.get(1.0, "end-1c")
        # This section exists to ensure whatever is being saved is valid json. Prevents being unable to edit it later.
        with open("configTester.txt", "w") as f:
            f.write(text)
            f.close()
        try:
            with open("configTester.txt", "r") as f:
                tester = json.load(f)
                f.close()
        except Exception:
            warningLbl.config(text="Invalid format. Only edit the variables and nothing else.")
            if os.path.exists("configTester.txt"):
                os.remove("configTester.txt")
            return 1
        with open("config.json", "w") as f:
            f.write(text)
            f.close()
        if os.path.exists("configTester.txt"):
            os.remove("configTester.txt")
        root.destroy()
        return 0

    def resetConfig():
        """Resets config.json to the default settings (taken from configBackup.json)"""
        warningLbl.config(text="")
        text = configEnt.get(1.0, "end-1c")
        with open("configBackup.json", "r") as f:
            config = json.load(f)
            config = json.dumps(config, indent=4)
            f.close()
        with open("config.json", "w") as f:
            f.write(config)
            f.close()
        configEnt.delete(1.0, "end")
        configEnt.insert(tk.END, config)
        return 0

    root = tk.Tk()
    root.resizable(False, False)
    root.title("Youtube Video Downloader")
    root.geometry("900x600")
    root.config(bg="dodger blue")

    with open("config.json", "r") as f:
        config = json.load(f)
        config = json.dumps(config, indent=4)
        f.close()

    tk.Frame(root, bg="white", width=850, height=550).place(x=25, y=25)
    configEnt = tk.Text(root, font=("Montserrat", 13), bd=5, width=53, relief="groove")
    configEnt.place(x=45, y=45)
    configEnt.insert(tk.END, config)

    cnfgSave = tk.Button(root, text="Save config", font=("Montserrat", 20), command=updateConfig, width=14)
    cnfgSave.place(x=550, y=45)
    cnfgRst = tk.Button(root, text="Reset config", font=("Montserrat", 20), command=resetConfig, width=14)
    cnfgRst.place(x=550, y=105)

    warningLbl = tk.Label(root, font=("Montserrat", 20), bg="white", wraplength=325)
    warningLbl.place(x=550,y=165)
    root.mainloop()
    return 0

def configReader(config):
    """Returns a dictonary full of all the items obtained from the config in the order listed inside it."""
    with open(config, "r") as configFile:
        config = json.load(configFile)
        # JSON doesn't have sets so we have to convert a list into a set
        catagoriesList = config["sponsorblockSkipCatagories"]
        tempSet = {None}  # Python thinks this is a dictionary if I don't include at least 1 element
        for item in catagoriesList:
            tempSet.add(item)
        config["sponsorblockSkipCatagories"] = tempSet
        tempSet.remove(None)  # None element is not needed to is removed
        configFile.close()
        return config

def moveTemptoDownloads(directory):
    tempDirectory = str(os.path.abspath(os.getcwd())) + "\\temp\\"
    for item in os.listdir(path=tempDirectory):
        if item not in os.listdir(path=directory):
            print(f"Moving {item} to {directory}. ")
            moveFile(item, tempDirectory, directory)
            print(f"Moved {item} successfully!")
        else:
            print(f"Moving file {item} failed. Clashing file names found.\n"
                  f"Downloads can be manually moved from {tempDirectory}")

if __name__ == "__main__":
    filePath = createConsoleLog()
    logging.basicConfig(level=logging.DEBUG, filename=filePath)

    root = tk.Tk()
    root.resizable(False, False)
    root.title("Youtube Video Downloader")
    root.geometry("900x350")
    root.config(bg="dodger blue")

    downloadMethod = tk.StringVar()

    tk.Frame(root, bg="white", width=850, height=300).place(x=25, y=25)
    tk.Label(root, text="Enter URL Below:", bg="white", font=("Montserrat", 20)).place(x=45, y=45)
    urlEnt = tk.Entry(root, font=("Montserrat", 20), bd=5, width=53, relief="groove")
    urlEnt.place(x=45, y=85)

    vidAud = tk.Radiobutton(root,text="Full Video",font=("Montserrat",20), bd=5, width=14, relief="groove", value="v+a",
                            variable=downloadMethod)
    audO = tk.Radiobutton(root, text="Audio Only", font=("Montserrat", 20), bd=5, relief="groove", value="a", width=14,
                          variable=downloadMethod)
    vidO = tk.Radiobutton(root, text="Video Only", font=("Montserrat", 20), bd=5, relief="groove", value="v", width=14,
                          variable=downloadMethod)
    vidAud.place(x=45, y=130)
    audO.place(x=315, y=130)
    vidO.place(x=580, y=130)

    downloadButton = tk.Button(root,text="Download Video",font=("Montserrat", 20),bd=5,command=downloadWrapper,width=15)
    downloadButton.place(x=45, y=200)

    configButton = tk.Button(root, text="Edit Config", font=("Montserrat", 20), bd=5, command=configEditor, width=15)
    configButton.place(x=580, y=200)

    progressLabel = tk.Label(root, font=("Montserrat",10), bg="white", wraplength=780)
    progressLabel.place(x=45, y=270)

    progress = tk.ttk.Progressbar(root, orient="horizontal", length=260, mode="determinate")
    progress.place(x=310, y=220)

    root.mainloop()