from downloader import process_links
from tagger import process_all_mp3
from config import TEMP_FOLDER
from MP3TagEditor import MP3TagEditor 
from pathlib import Path

file_path = Path(TEMP_FOLDER / "Tengo John, Di-Meh, Cinco - MTM (feat. Di-Meh & Cinco).mp3")

file = MP3TagEditor(file_path)

print(file.get_empty_tags())

print(file.get_tag("artist"))


