import os
from pytubefix import YouTube, Playlist
import subprocess
from config import INPUT_FILE, NOTFOUND_FILE, DOWNLOAD_FOLDER

def convert_to_mp3(file_path):
    """Convertit un fichier AAC/M4A en vrai MP3 si nécessaire"""
    temp_mp3 = file_path.replace(".mp3", "_fixed.mp3")
    try:
        subprocess.run([
            "ffmpeg", "-i", file_path, "-vn",
            "-acodec", "libmp3lame", "-q:a", "2", temp_mp3
        ], check=True)
        os.replace(temp_mp3, file_path)  # Remplace l'ancien fichier
        print(f"✅ Conversion réussie : {file_path}")
    except subprocess.CalledProcessError:
        print(f"❌ Erreur de conversion : {file_path}")

def pretag(file_path, url):
    if "music.youtube" in url:
        
    else

def download_audio(url):
    """Télécharge l'audio d'une vidéo YouTube en MP3 et retourne True si réussi, False sinon."""
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        if not audio_stream:
            print(f"Aucun flux audio trouvé pour {url}")
            return False

        print(f"Téléchargement en cours : {yt.title}...")
        output_path = audio_stream.download(output_path=DOWNLOAD_FOLDER)
        
        # Renommage en .mp3
        base, _ = os.path.splitext(output_path)
        new_file = base + ".mp3"
        os.rename(output_path, new_file)
        
        # Conversion en vrai MP3 si nécessaire
        convert_to_mp3(new_file)
        pretag(new_file, url)

        print(f"✅ Téléchargement terminé : {new_file}")
        return True

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de {url} : {e}")
        return False

def expand_playlist(url):
    """Si l'URL est une playlist, retourne la liste des vidéos qu'elle contient."""
    try:
        playlist = Playlist(url)
        return list(playlist.video_urls)
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse de la playlist {url} : {e}")
        return []

def download(url):
    not_found_urls = []
    if "playlist?list=" in url:
        print(f"📂 Détection d'une playlist : {url}")
        urls = expand_playlist(url)
    else:
        urls = [url]

    for url in urls:
        if not download_audio(url):
            not_found_urls.append(url)
        else
            #TODO 

    return not_found_urls
