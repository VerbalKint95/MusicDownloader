from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, USLT
from mutagen.mp3 import MP3
from config import ARTIST_SEPARATOR

class MP3TagEditor:
    def __init__(self, filepath):
        self.filepath = filepath
        try:
            self.audio = EasyID3(filepath)
        except Exception:
            # Si pas de tags existants, on les crée
            self.audio = MP3(filepath)
            self.audio.add_tags()
            self.audio = EasyID3(filepath)
        self.full_audio = MP3(filepath, ID3=ID3)  # Pour manipuler les images

    # ========== Méthodes spécifiques ==========

    def set_track(self, track_number, total_tracks):
        self.audio["tracknumber"] = f"{track_number}/{total_tracks}"
        self.audio.save()

    def set_disk(self, disk_number, total_disks):
        self.audio["discnumber"] = f"{disk_number}/{total_disks}"
        self.audio.save()

    def set_title(self, title):
        self.audio["title"] = title
        self.audio.save()

    #artist
    def set_artist(self, artist):
        self.audio["artist"] = artist
        self.audio.save()

    def set_artists(self, artists):
        if isinstance(artists, list):
            artist_str = ARTIST_SEPARATOR.join([i for i in artists if i])
            self.set_artist(artist_str)
        else:
            raise TypeError("artists should be a list.")
    
    def add_artist(self, artist):
        self.set_artists([self.get_artist(), artist])
    
    #composer
    def set_composer(self, composer):
        self.audio["composer"] = composer
        self.audio.save()

    def set_composers(self, composers):
        if isinstance(composers, list):
            composer_str = ARTIST_SEPARATOR.join([i for i in composers if i])
            self.set_composer(composer_str)
        else:
            raise TypeError("composers should be a list.")
    
    def add_composer(self, composer):
        self.set_composers([self.get_composer(), composer])


    def set_album(self, album):
        self.audio["album"] = album
        self.audio.save()

    def set_genre(self, genre):
        self.audio["genre"] = genre
        self.audio.save()

    def set_comment(self, comment):
        self.audio["comment"] = comment
        self.audio.save()

    def set_url(self, url):
        self.audio["website"] = url
        self.audio.save()

    def set_album_artist(self, album_artist):
        self.audio["albumartist"] = album_artist
        self.audio.save()

    def set_copyright(self, copyright_text):
        self.audio["copyright"] = copyright_text
        self.audio.save()

    def set_publisher(self, publisher):
        self.audio["publisher"] = publisher
        self.audio.save()

    def set_conductor(self, conductor):
        self.audio["conductor"] = conductor
        self.audio.save()

    def set_encoded_by(self, encoded_by):
        self.audio["encodedby"] = encoded_by
        self.audio.save()

    
        
    

    def set_bpm(self, bpm):
        self.audio["bpm"] = str(bpm)
        self.audio.save()

    #not ID3
    def set_cover(self, image_path, mime_type="image/jpeg"):
        """Ajoute une cover au MP3 (par défaut jpeg)."""
        with open(image_path, "rb") as img:
            self.full_audio.tags.add(
                APIC(
                    encoding=3,  # 3 = UTF-8
                    mime=mime_type,
                    type=3,  # 3 = Cover (front)
                    desc="Cover",
                    data=img.read()
                )
            )
        self.full_audio.save()

    #not ID3
    def set_lyrics(self, lyrics, lang='eng'):
        """Ajoute des paroles (lyrics) au fichier MP3."""
        # Supprimer d'abord les anciennes paroles si existantes
        self.full_audio.tags.delall('USLT')
        self.full_audio.tags.add(
            USLT(encoding=3, lang=lang, desc='', text=lyrics)
        )
        self.full_audio.save()

    # ========== Méthodes utilitaires ==========

    def get_tags(self):
        """Retourne tous les tags existants."""
        return dict(self.audio)

    def get_tag(self, tag_name):
        """Retourne la valeur d'un tag spécifique."""
        return self.audio.get(tag_name, None)[0]
    
    def get_album_artist(self):
        return self.audio.get("albumartist", None)[0]
    
    def get_artist(self):
        return self.audio.get("artist", None)[0]
    
    def get_title(self):
        return self.audio.get("title", None)[0]
    
    def get_composer(self):
        return self.audio.get("composer", None)[0]
    
    def get_track(self):
        return self.audio.get("tracknumber")[0]

    def delete_tag(self, tag_name):
        """Supprime un tag."""
        if tag_name in self.audio:
            del self.audio[tag_name]
            self.audio.save()

    def get_empty_tags(self):
        """Retourne la liste des tags supportés qui sont vides (non définis)."""
        expected_tags = [
            "tracknumber", "discnumber", "title", "artist", "album", "genre",
            "comment", "website", "albumartist", "copyright",
            "publisher", "conductor", "encodedby", "bpm", "cover"
        ]

        empty_tags = []

        for tag in expected_tags:
            if tag == "cover":
                # Vérification spéciale pour la cover (APIC)
                if not any(key.startswith("APIC") for key in self.full_audio.tags.keys()):
                    empty_tags.append("cover")
            elif tag == "lyrics":
                if not any(key.startswith("USLT") for key in self.full_audio.tags.keys()):
                    empty_tags.append("lyrics")
            else:
                if tag not in self.audio or not self.audio[tag]:
                    empty_tags.append(tag)

        return empty_tags

# Exemple d'utilisation
if __name__ == "__main__":
    editor = MP3TagEditor("ton_fichier.mp3")

    # Exemple : changer le titre
    editor.set_title("Nouveau Titre")

    # Exemple : ajouter une cover
    editor.set_cover("chemin/vers/image.jpg")

    # Voir les tags vides
    print(editor.list_empty_tags())
