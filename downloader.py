from webbrowser import get
from pytube import YouTube
import os

def get_video(link, index):
    yt = YouTube(link)
    print("Downloading...\n")
    path = f"./Videos/Vid{index}"
    
    while os.path.isdir(path) :
        index += 1
        path = f"./Videos/Vid{index}"
    os.mkdir(path)
    try:
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(path) 
    except:
        raise Exception("Cant downlaod the video")
    
    print(f"Video in {path}.\n")

    # Return the index cause it can be modified
    return index

if __name__ == '__main__':
    test = "https://www.youtube.com/watch?v=I5rlZRlZVSY"
    get_video(test, 0)