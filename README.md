# Basic TikTok account Manager with python selenium

## TikTok API
Write your tiktok login informations in config.py and put the file in tiktok folder.
Instance of tiktok.TikTokControler gives access to a login method and other functionalities like posting videos.

## Content
dowloader.py can download a youtube video based on a link in Videos folder, assigning an index to this video.
video_cutter.py can cut a video in n parts and add a text on each new part that mention the part index. It takes the index of the video to be cut for parameter.
youtube_scrapper.py  can get the links list of the last shorts posted on a youtube account with selenium.
