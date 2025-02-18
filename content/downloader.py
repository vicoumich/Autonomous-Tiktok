import os
import yt_dlp

def get_video(link: str, index=0) -> int:
    path = f"./Videos/Vid{index}"
    
    while os.path.isdir(path) :
        index += 1
        path = f"./Videos/Vid{index}"
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
    test = "https://youtube.com/shorts/5wmP7YZQQtk"
    get_video(test, 1)