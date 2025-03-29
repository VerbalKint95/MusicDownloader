from pytube import YouTube
import os

DOWNLOAD_FOLDER = "temp"  # Dossier temporaire pour stocker les fichiers téléchargés

def download_audio(youtube_url):
    """Télécharge l'audio d'une vidéo YouTube en MP3 et retourne le chemin du fichier."""
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        if not audio_stream:
            print(f"Aucun flux audio trouvé pour {youtube_url}")
            return None

        print(f"Téléchargement en cours : {yt.title}...")

        # Téléchargement
        output_path = audio_stream.download(output_path=DOWNLOAD_FOLDER)

        # Renommage en .mp3
        base, _ = os.path.splitext(output_path)
        new_file = base + ".mp3"
        os.rename(output_path, new_file)

        print(f"Téléchargement terminé : {new_file}")
        return new_file

    except Exception as e:
        print(f"Erreur lors du téléchargement de {youtube_url} : {e}")
        return None

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    download_audio(test_url)
