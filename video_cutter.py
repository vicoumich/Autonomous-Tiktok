from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import os
from threading import Thread


HASHTAGS = ["#tiktok", "#foryou", "#foryoupage", "#fyp", "#viral", "#tiktokindia", 
            "#trending", "#tiktokfrance", "#comedy", "#funny"]
STR_TAGS = ' '.join(HASHTAGS)

def make_part_thread(source, targ, start, end, index):
    part = VideoFileClip(source).subclipped(start, end)
    text = TextClip(text = f"Part{index}", 
                     font_size=60, color="black",
                     bg_color="white", 
                     font="Arial.ttf").with_duration(4).with_position("center")
                     
    part = CompositeVideoClip([part, text])
    text.close()
    part.write_videofile(targ)
    part.close()


def video_cutter(videoindex: int, start: int|float, end: int|float, nbpart: int):
    if end <= start:
        raise Exception("End time must be more than start")
    threads = []
    index_part = 1
    part_time = (end - start) // nbpart
    start2 = start
    end2 = start2 + part_time
    source = f"Videos/Vid{videoindex}/test.mp4"

    targ = f"Videos/Vid{videoindex}/Part_{index_part}_{STR_TAGS}.mp4"

    # If the video is already cut
    if os.path.isfile(targ):
        print(f"{source} already cut in Videos/Vid{videoindex}/")
        return

    # print("Cutting the video ", end="")
    while start2 <= end:

        # Create and start a thread
        targ = f"Videos/Vid{videoindex}/Part_{index_part}_{STR_TAGS}.mp4"
        print(f"\n --- Starting thread{index_part} --- \n")
        threads.append(Thread(target=make_part_thread, 
                              args=[source, targ, start2, end2, index_part]))
        threads[-1].start()

        # Cacul next interval
        start2 = end2 - 3
        end2 = start2 + part_time
        index_part += 1
        
    for thread in threads:
        thread.join()

def clean_parts(videoindex):
    index = 1
    targ = f"Videos/Vid{videoindex}/Part{index}.mp4"
    while os.path.isfile(targ):
        os.remove(targ)
        index += 1
        targ = f"Videos/Vid{videoindex}/Part{index}.mp4"
            
    
if __name__ == "__main__":
    video_cutter(1, 1, 58, 4)
    input("--- Press Enter To delete test ---")
    clean_parts(1)