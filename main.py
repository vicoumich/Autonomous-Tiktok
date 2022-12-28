from video_cutter import video_cutter, clean_parts
from tiktok import TikTokControler
from downloader import get_video
from art import tprint

def main():
    # Intro
    tprint("Autonomous")
    tprint("TikTok")
    print(72 * "#")

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
        


if __name__ == "__main__":
    main()