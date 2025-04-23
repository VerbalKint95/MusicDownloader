from config import TEMP_FOLDER, GENIUS_TOKEN
from lyricsgenius import Genius
from lyricsgenius.genius import Song, Artist, Album
import MP3TagEditor
import os
import shutil
import requests
from MP3TagEditor import MP3TagEditor
from genius import enhanceTag
from pathlib import Path

TAGGED_FOLDER = "data/tagged"
os.makedirs(TAGGED_FOLDER, exist_ok=True)
MANUAL_TAGGING_FOLDER = "data/manual_tagging"
genius = Genius(GENIUS_TOKEN)
genius_URL = Path("https://genius.com")


def download_image(url, save_path):
    """Télécharge une image et la sauvegarde localement."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return save_path
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")
    return None

def enhanceTag(file_path: str):
    """Affiche le nom du fichier, récupère les infos Genius et tagge le MP3."""
    file_name = os.path.basename(file_path)
    print(f"\n🎵 Traitement du fichier : {file_name}")
    mp3 = MP3TagEditor(file_path)
    title = mp3.get_title()
    artist = mp3.get_album_artist()
    if title and artist:
        song = genius.search_song(title=title, artist=artist, get_full_info=True)

        mp3.set_title(song.title)
        mp3.set_url(genius_URL/song.path)
        mp3.set_lyrics(song.lyrics)
        mp3.set_artist(song.)

        album_id = song.album.id
        album = genius.search_album(album_id=album_id)

        mp3.set_album(album.name)
        mp3.set_album_artist(album.artist)

        i=0
        for track in album.tracks:
            i=i+1
            if track.id == song.id:
                mp3.set_track(i, len(album.tracks))
        

    else:
        # Déplacement vers le dossier tagged/
        shutil.move(file_path, os.path.join(TAGGED_FOLDER, file_name))
        print(f"✅ Fichier déplacé vers {TAGGED_FOLDER}")
        

    return


'''    # Recherche sur Genius
    audio=MP3TagEditor(file_path)
    title = audio.get_title
    artist = audio.get_album_artist

    if artist and title:
        song_info = search_song(artist=artist, title=title)
    else
        song_info = search_song(os.path.splitext(file_name)[0])




    if not song_info:
        print("⚠️ Impossible de trouver les infos sur Genius. Déplacement vers manual_tagging/")
        os.makedirs(MANUAL_TAGGING_FOLDER, exist_ok=True)
        shutil.move(file_path, os.path.join(MANUAL_TAGGING_FOLDER, file_name))
        return

    song_details = get_song_details(song_info["id"])
    if not song_details:
        print("⚠️ Impossible de récupérer les détails de la chanson. Déplacement vers manual_tagging/")
        os.makedirs(MANUAL_TAGGING_FOLDER, exist_ok=True)
        shutil.move(file_path, os.path.join(MANUAL_TAGGING_FOLDER, file_name))
        return

    # Tagger le MP3
    tag_mp3(file_path, song_details)
'''

    

def process_all_mp3():
    """Boucle sur tous les fichiers MP3 dans temp/ et les traite."""
    if not os.path.exists(TEMP_FOLDER):
        print(f"⚠️ Le dossier {TEMP_FOLDER} n'existe pas.")
        return

    files = [f for f in os.listdir(TEMP_FOLDER) if f.endswith(".mp3")]

    if not files:
        print("📂 Aucun fichier MP3 trouvé.")
        return

    for file in files:
        enhanceTag(os.path.join(TEMP_FOLDER, file))

if __name__ == "__main__":
    process_all_mp3()