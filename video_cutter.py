from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
from threading import Thread


HASHTAGS = ["#tiktok", "#foryou", "#foryoupage", "#fyp", "#viral", "#tiktokindia", 
            "#trending", "#tiktokfrance", "#comedy", "#funny"]
STR_TAGS = ' '.join(HASHTAGS)

def make_part_thread(source, targ, start, end, index):
    part = VideoFileClip(source).subclip(start, end)
    text = TextClip(f"Part{index}", 
                     fontsize=60, color="black",
                     bg_color="white", 
                     font="Arial").set_position(("center", "center")).set_duration(4)
                     
    part = CompositeVideoClip([part, text])
    text.close()
    part.write_videofile(targ)
    part.close()


def video_cutter(videoindex, start, end, nbpart):
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
    video_cutter(0, 0, 120, 4)
    input("--- Press Enter To delete test ---")
    clean_parts(0)