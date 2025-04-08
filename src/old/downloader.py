from pytubefix import YouTube, Playlist
import os
import subprocess

INPUT_FILE = "data/input/links.txt"
NOTFOUND_FILE = "data/output/notfound.txt"
DOWNLOAD_FOLDER = "data/temp"


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

def download_audio(youtube_url):
    """Télécharge l'audio d'une vidéo YouTube en MP3 et retourne True si réussi, False sinon."""
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        if not audio_stream:
            print(f"Aucun flux audio trouvé pour {youtube_url}")
            return False

        print(f"Téléchargement en cours : {yt.title}...")
        output_path = audio_stream.download(output_path=DOWNLOAD_FOLDER)
        
        # Renommage en .mp3
        base, _ = os.path.splitext(output_path)
        new_file = base + ".mp3"
        os.rename(output_path, new_file)
        
        # Conversion en vrai MP3 si nécessaire
        convert_to_mp3(new_file)

        print(f"✅ Téléchargement terminé : {new_file}")
        return True

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de {youtube_url} : {e}")
        return False

def expand_playlist(url):
    """Si l'URL est une playlist, retourne la liste des vidéos qu'elle contient."""
    try:
        playlist = Playlist(url)
        return list(playlist.video_urls)
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse de la playlist {url} : {e}")
        return []

def process_links():
    """Lit le fichier links.txt, télécharge les musiques et gère les erreurs."""
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Le fichier {INPUT_FILE} n'existe pas.")
        return

    with open(INPUT_FILE, "r") as f:
        urls = [line.strip() for line in f.readlines()]

    if not urls:
        print("⚠️ Aucune URL trouvée dans links.txt.")
        return

    not_found_urls = []
    remaining_urls = []

    for url in urls:
        if "playlist?list=" in url:
            print(f"📂 Détection d'une playlist : {url}")
            video_urls = expand_playlist(url)
        else:
            video_urls = [url]

        for video_url in video_urls:
            if not download_audio(video_url):
                not_found_urls.append(video_url)
                remaining_urls.append(video_url)  # On garde les URL échouées

    # Mettre à jour links.txt en ne gardant que les URL échouées
    with open(INPUT_FILE, "w") as f:
        for url in remaining_urls:
            f.write(url + "\n")

    # Ajouter les URL échouées à notfound.txt
    if not_found_urls:
        os.makedirs(os.path.dirname(NOTFOUND_FILE), exist_ok=True)
        with open(NOTFOUND_FILE, "a") as f:
            for url in not_found_urls:
                f.write(url + "\n")

    print("✅ Traitement terminé.")

if __name__ == "__main__":
    process_links()