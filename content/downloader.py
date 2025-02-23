import os
import yt_dlp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS_DIR = os.path.join(BASE_DIR, "Videos")

def get_video(link: str, index=0) -> int:
    path = os.path.join(VIDEOS_DIR, f"Video{index}")
    
    while os.path.isdir(path) :
        index += 1
        path = os.path.join(VIDEOS_DIR, f"Video{index}")
    os.mkdir(path)
    try:
        print("Downloading...\n")
        ydl_opts = {
            'paths':{
                'home': path,
            },
            'outtmpl': 'test.%(ext)s'
        } 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except Exception as e:
        raise e
    
    print(f"Video in {path} .\n")

    # Return the index cause it can be modified
    return index

if __name__ == '__main__':
    test = "https://youtube.com/shorts/9Z9tRR7RCqA"
    get_video(test, 1)