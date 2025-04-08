import os
import shutil
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TYER, TCOM, TCON, COMM, APIC, TRCK
from genius_api import search_song, get_song_details

TEMP_FOLDER = "data/temp"
TAGGED_FOLDER = "data/tagged"
MANUAL_TAGGING_FOLDER = "data/manual_tagging"

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

def tag_mp3(file_path, song_details):
    """Ajoute les tags ID3 au fichier MP3."""
    audio = MP3(file_path, ID3=ID3)

    # S'assurer que le fichier a des tags
    if audio.tags is None:
        audio.add_tags()

    # Ajout des métadonnées
    audio.tags.add(TIT2(encoding=3, text=song_details.get("title", "")))  # Titre
    audio.tags.add(TPE1(encoding=3, text=song_details.get("primary_artist", {}).get("name", "")))  # Artiste
    audio.tags.add(TALB(encoding=3, text=song_details.get("album", {}).get("name", "")))  # Album
    release_year = song_details.get("release_date")
    release_year = release_year[:4] if release_year else "Unknown"
    audio.tags.add(TYER(encoding=3, text=release_year))  # Année

    writers = [writer["name"] for writer in song_details.get("writer_artists", []) if isinstance(writer, dict)]
    audio.tags.add(TCOM(encoding=3, text=", ".join(writers)))  # Compositeurs

    audio.tags.add(TCON(encoding=3, text=song_details.get("genre", "")))  # Genre musical

    # Track et Disk info
    track_number = song_details.get("track_number", "1")
    disk_number = song_details.get("disk_number", "1")
    audio.tags.add(TRCK(encoding=3, text=f"{track_number}/{disk_number}"))

    # Commentaire avec lien + description + annotations
    commentary = f"{song_details.get('url', '')}\n\n{song_details.get('description', '')}\n\nAnnotations:\n"
    annotations = song_details.get("annotations", [])
    for annotation in annotations:
        commentary += f"- {annotation}\n"
    audio.tags.add(COMM(encoding=3, text=commentary))

    # Téléchargement et ajout de la cover
    cover_url = song_details.get("cover_art_url", "")
    if cover_url:
        cover_path = download_image(cover_url, "cover.jpg")
        if cover_path:
            with open(cover_path, "rb") as cover_file:
                audio.tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=cover_file.read()))
            os.remove(cover_path)

    # Sauvegarde des tags
    audio.save()

def process_mp3(file_path):
    """Affiche le nom du fichier, récupère les infos Genius et tagge le MP3."""
    file_name = os.path.basename(file_path)
    print(f"\n🎵 Traitement du fichier : {file_name}")

    # Recherche sur Genius
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

    # Déplacement vers le dossier tagged/
    os.makedirs(TAGGED_FOLDER, exist_ok=True)
    shutil.move(file_path, os.path.join(TAGGED_FOLDER, file_name))
    print(f"✅ Fichier déplacé vers {TAGGED_FOLDER}")

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
        process_mp3(os.path.join(TEMP_FOLDER, file))

if __name__ == "__main__":
    process_all_mp3()
