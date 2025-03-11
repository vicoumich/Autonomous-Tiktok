import yt_dlp
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS_DIR = os.path.join(BASE_DIR, "Videos")

class YouTubeManager:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'extract_flat': True,  # Extract Metadata without downloading
        }

    def get_new_index_path(self):
        index=0
        path = os.path.join(VIDEOS_DIR, f"Video{index}")
    
        while os.path.isdir(path) :
            index += 1
            path = os.path.join(VIDEOS_DIR, f"Video{index}")
        os.mkdir(path)
        return path

    def get_shorts_links(self, channel_name: str) -> list[dict]:
        """
        Récupère les liens de tous les Shorts d'une chaîne YouTube.
        
        :param channel_name: Nom de la chaîne YouTube (comme dans l'URL)
        :return: Liste des URLs des Shorts
        """
        if channel_name !='' or channel_name[0] != "@":
            channel_name = "@" + channel_name
        channel_url = f'https://www.youtube.com/{channel_name}'
        print(channel_url)
        shorts_urls = []

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(channel_url, download=False)
                videos = info_dict.get('entries', [])[1]["entries"]

                # Filtrer uniquement les Shorts (ils contiennent "/shorts/" dans l'URL)
                shorts_urls = [video for video in videos if '/shorts/' in video['url']]
            except Exception as e:
                print(f"Erreur lors de l'extraction des Shorts: {e}")

        return shorts_urls

    def download_videos(self, videos: list[dict], min_views: int = None, max_duration: int = None):
        """
        Télécharge une liste de vidéos avec des filtres optionnels.

        :param videos: list[dict] contains videos metadata
        :param min_views: Minimum view count requiered (None disable filter)
        :param max_duration: Maximum duration in seconds (None disable filter)
        """
        new_path = self.get_new_index_path()

        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
            valid_urls = []

            for video in videos:
                try:
                    title = video.get('title', 'Titre inconnu')
                    views = video.get('view_count', 0)
                    duration = video.get('duration', 0)

                    if (min_views is None or views >= min_views) and (max_duration is None or duration <= max_duration):
                        valid_urls.append(video["url"])
                        print(f"✅ '{title}' ajouté à la liste de téléchargement (Vues: {views}, Durée: {duration}s)")
                    else:
                        print(f"❌ '{title}' ignoré (Vues: {views}, Durée: {duration}s)")
                except Exception as e:
                    print(f"Erreur lors de la récupération des infos de {video['url']}: {e}")

        # Download videos with valid caracteristics
        if valid_urls:
            for url in valid_urls:
                download_opts ={
                    'quiet': False, 
                    'paths':{
                        'home': new_path,
                    },
                    'outtmpl': 'test.%(ext)s'
                } 
                new_path = self.get_new_index_path()
                # Activer la sortie pour voir le téléchargement
                with yt_dlp.YoutubeDL(download_opts) as ydl:
                    ydl.download(url)
        else:
            print("Aucune vidéo ne correspond aux critères.")

if __name__ == "__main__":
    ym = YouTubeManager()
    videos = ym.get_shorts_links(channel_name="musique-remix")
    ym.download_videos(videos=videos, min_views=1000000)