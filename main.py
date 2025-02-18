from content.video_cutter import video_cutter, clean_parts
from tiktok.tiktok import TikTokControler
from content.downloader import get_video
from art import tprint

def main():
    # Intro
    tprint("Autonomous")
    tprint("TikTok")
    print(72 * "#")

    controler_tiktok = None
    commands = ["download", "cut", "tiktok", "full"]
    command = input(f"Commands avilable {commands} >>>").strip()
    while not(command in commands):
        print("You can only put available command")
        command = input(f"Commands available {commands} >>>").strip()
    


    if command == "full":
        url = input("\turl youtube >>>").strip()
        index = get_video(url, 0)

        # mettre des try
        i1 = int(input("\tfirst part of the interval >>>"))
        i2 = int(input("\tsecond part of the interval >>>"))
        nbpart = int(input("Number of parts >>>"))
        video_cutter(index, i1, i2, nbpart)

        controler_tiktok = TikTokControler()
        controler_tiktok.connect()
        for i in range(nbpart):
            controler_tiktok.post(i, index)
        
    if command == "tiktok":
        if controler_tiktok is None:    
            controler_tiktok = TikTokControler()
        tiktok_commands = ["post", "connection"]
        tiktok_command = None

        while not(tiktok_command in tiktok_commands):
            print("You can only put available command")
            tiktok_command = input(f"Commands available {tiktok_commands} >>>").strip()
        if tiktok_command == "post":
            video_index = int(input("\t video index >>>"))
            part_index = int(input("\t part index >>>"))
            if controler_tiktok.connected:
                controler_tiktok.post(part_index, video_index)
            else:
                controler_tiktok.connect()
                controler_tiktok.post(part_index, video_index)
        if tiktok_command == "connection":
            if controler_tiktok.connected:
                pass
            else:
                controler_tiktok.connect()

if __name__ == "__main__":
    main()
    