from config import GENIUS_TOKEN, TAGGED_FOLDER, MANUAL_TAGGING_FOLDER, DOWNLOAD_FOLDER, THUMBNAIL_FOLDER
from lyricsgenius import Genius
import MP3TagEditor
import os
import shutil
import requests
from MP3TagEditor import MP3TagEditor
from pathlib import Path
from urllib.parse import urlparse
import re

     

genius = Genius(GENIUS_TOKEN)



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
    title = re.sub(r"\s*\(feat\.?\s[^)]*\)", "", mp3.get_title())
    artist = mp3.get_album_artist()
    
    if title and artist:
        song = genius.search_song(title=title, artist=artist, get_full_info=True)

    if song:
        mp3.set_title(song.title)
        mp3.set_url(song.url)
        mp3.set_lyrics(song.lyrics)

        #cover
        cover_filename = Path(urlparse(song.song_art_image_url).path).name
        cover_uri = THUMBNAIL_FOLDER / cover_filename
        
        if not os.path.isfile(cover_uri):
            download_image(song.song_art_image_url, cover_uri)
        mp3.set_cover(cover_uri)


        mp3.set_artist("")
        for writer in song.writers:
            mp3.add_artist(writer.name)

        mp3.set_composer("")
        for composer in song.producers:
            mp3.add_composer(composer.name)
        

        mp3.set_album_artist(song.album.artist.name)
        mp3.set_album(song.album.name)

        #set track using Genius TODO not use genius because tracklist does not take in count CD and can have "false track" like thumbnail or booklet
        if not mp3.get_track():
            album_id = song.album.id
            album = genius.search_album(album_id=album_id)
            for track in album.tracks:
                if track.id == song.id:
                    mp3.set_track(track.number, len(album.tracks))
                    break
        
        # Déplacement vers le dossier tagged/
        shutil.move(file_path, os.path.join(TAGGED_FOLDER, file_name))
        print(f"✅ Fichier déplacé vers {TAGGED_FOLDER}")

    else:
        # Déplacement vers le dossier tagged/
        shutil.move(file_path, os.path.join(MANUAL_TAGGING_FOLDER, file_name))
        print(f"❌ Fichier n'a pas pu être taggé, déplacé vers {MANUAL_TAGGING_FOLDER}")
    return

    

def process_all_mp3():
    """Boucle sur tous les fichiers MP3 dans temp/ et les traite."""
    if not os.path.exists(DOWNLOAD_FOLDER):
        print(f"⚠️ Le dossier {DOWNLOAD_FOLDER} n'existe pas.")
        return

    files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith(".mp3")]

    if not files:
        print("📂 Aucun fichier MP3 trouvé.")
        return

    for file in files:
        enhanceTag(os.path.join(DOWNLOAD_FOLDER, file))

if __name__ == "__main__":
    process_all_mp3()