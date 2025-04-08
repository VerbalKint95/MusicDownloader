from mutagen.easyid3 import EasyID3
from config import TEMP_FOLDER
from pathlib import Path

file = Path(TEMP_FOLDER / "Youssoupha - AMOUR SUPRÊME.mp3")

audio=EasyID3(file)
print(audio.get('title', [None])[0])
print(audio.get('artist', [None])[0])