from pytube import Search
from pytubefix import YouTube
from pathlib import Path
import os
import json
import unicodedata
import warnings
import eyed3
import subprocess


def get_config(config_file:str = "config.json") -> dict:
    # get data
    data = json.load(open(config_file, "r", encoding="utf-8"))

    for i, j in data.items():
        print(">>", i, ":", j)

    return data

def change_metadata(path_to_mp3, song_name, data, track_num):
    artist, title = song_name.split(" - ")[:2]
    album = data["folder name"]

    audiofile = eyed3.load(path_to_mp3)
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.title = title
    audiofile.tag.track_num = track_num + 1

    audiofile.tag.save()

def convert_to_mp3(input_path: str, output_path: str):
    """Convert audio file to MP3 using ffmpeg."""
    subprocess.run([
        "ffmpeg",
        "-i", input_path,
        "-codec:a", "libmp3lame",  
        "-q:a", "2",               
        "-y",  
        output_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.remove(input_path)  # Delete the original .m4a file

def handle_songname(song_name, data, index):
    file_name = ""

    # remove invalid characters
    for char in song_name:
        if char not in r'\/:*?"<>|#':
            file_name += char

    # remove artist if wanted
    if data["song name only"] and " - " in song_name:
        itter = file_name.split(" - ")[1:]
        file_name = " - ".join(itter)

    # make filenames shorter if too long
    if len(file_name) > 100:
        file_name = file_name[-100:]

    # add indexing to song names if wanted
    if data["index names"]:
        file_name = str(index + 1).zfill(data["index digits"]) + " - " + file_name

    return file_name

def save_audio(song_name:str, save_path:str, data:dict, index):
    """Search and download a song from youtube"""
    
    s = Search(song_name)

    if len(s.results) == 0:
        print(f"> No results found for '{song_name}', skipping")
        return

    i = 0
    while True:
        try:
            video = s.results[i] 
            video_url = video.watch_url
            audio = YouTube(video_url).streams.filter(only_audio=True)[0]
            break
        except:
            i += 1
        
    # Get clean filename
    file_name = handle_songname(song_name, data=data, index=index)
    
    # Define full paths
    temp_m4a_path = os.path.join(save_path, f"{file_name}.m4a")
    final_mp3_path = os.path.join(save_path, f"{file_name}.mp3")
    
    if data["ffmpeg"]:
        # Download song as m4a
        audio.download(output_path=save_path, filename=f"{file_name}.m4a")

        # Convert to mp3
        convert_to_mp3(temp_m4a_path, final_mp3_path)

        # change metadata
        change_metadata(final_mp3_path, song_name, data, index)

    
    else:
        audio.download(output_path=save_path, file_name=f"{file_name}.mp3")

    # Return the correct path
    return final_mp3_path

def main():
    
    data = get_config()

    # get txt file with songs
    song_list_txtfile = data["songs text file"]
    # get folder name. If None (null in json file),
    # use it a generic one
    if data["folder name"] is not None:
        save_folder = data["folder name"]
    else:
        save_folder = "pytube_downloads"

    # get path where folder is / will be created.
    # If None, use std downloads path
    if data["custom download path"] is None:
        download_path = str(Path.home() / "Downloads")
    else:
        download_path = data["custom download path"]
    
    download_path = os.path.join(download_path, save_folder)

    print(f"> Songs will be downloaded to {download_path}")

    # open txt file and get list of
    # song names
    with open(song_list_txtfile, "r", encoding="utf-8") as f:
        songs = [i for i in f.read().split("\n") if (not i.startswith("#")) and i] # remove 'comments'
        f.close()

    # create save path if not exists
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    # save songs
    for i, song in enumerate(songs):
        # only downloads songs if they are not already in the given path
        if f"{handle_songname(song, data=data, index=i)}.mp3" not in os.listdir(download_path):
            song_path = save_audio(song, save_path=download_path, data=data, index=i)
    

if __name__ == "__main__":
    # stupid (me) safekeeping
    q = "> Did you remember to change config " +\
        "files for this download? (y/n)"
    if input(q).lower() == "y":
        main()
    else:
        print("> go on, change them :)")
