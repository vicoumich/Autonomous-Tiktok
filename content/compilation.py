import os
from moviepy import VideoFileClip, concatenate_videoclips

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS_DIR = os.path.join(BASE_DIR, "Videos")

def compile_videos(index_list: list[int]):
    """
    Compile les vidéos correspondant aux index fournis et génère une nouvelle vidéo.
    
    :param index_list: Liste des index des vidéos à compiler.
    :return: Index de la nouvelle vidéo créée.
    """
    video_clips = []
    base_path = VIDEOS_DIR
    
    # Charger les vidéos
    for index in index_list:
        video_path = os.path.join(base_path, f"Video{index}", "test.mp4")
        if os.path.exists(video_path):
            video_clips.append(VideoFileClip(video_path))
        else:
            print(f"Video not found : {video_path}")
    
    if not video_clips:
        raise ValueError("No video to compile")
    
    # Concaténer les vidéos
    final_video = concatenate_videoclips(video_clips, method="compose")
    
    # Trouver le prochain index
    existing_indexes = [int(folder.replace("Video", "")) for folder in os.listdir(base_path) if folder.startswith("Video") and folder.replace("Video", "").isdigit()]
    new_index = max(existing_indexes) + 1 if existing_indexes else 1
    
    # Sauvegarder la vidéo compilée
    output_folder = os.path.join(base_path, f"Video{new_index}")
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "test.mp4")
    final_video.write_videofile(output_path, codec="libx264", fps=24)
    
    return new_index
