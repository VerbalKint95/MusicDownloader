# config.py

import yaml
import os
from pathlib import Path

# Chemin vers le fichier config.yaml
CURRENT_PATH = Path(__file__).resolve().parents[1]
CONFIG_FILE = CURRENT_PATH / 'config' / 'config.yaml'

# Fonction utilitaire pour convertir un chemin relatif
def _relative_path(path_str):
    path = Path(path_str)
    if not path.is_absolute():
        return (CURRENT_PATH / path).resolve()
    return path

# Charger le fichier YAML
if not CONFIG_FILE.exists():
    raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    _config_data = yaml.safe_load(f)

# Raccourcis pour les différentes sections
_paths = _config_data["config"]["paths"]
_tag_config = _config_data["config"]["tag_config"]

# Variables de chemin, résolues proprement

INPUT_FILE = _relative_path(_paths["input_file"])
NOTFOUND_FILE = _relative_path(_paths["notfound_file"])
LIBRARY_FOLDER = _relative_path(_paths["library_folder"])
GENIUS_TOKEN_FILE = _relative_path(_paths["genius_token_file"])

TEMP_FOLDER = _relative_path(_paths["temp_folder"])

#temp sub-folder
DOWNLOAD_FOLDER = TEMP_FOLDER / "download"
TAGGED_FOLDER = TEMP_FOLDER / "tagged"
THUMBNAIL_FOLDER = TEMP_FOLDER / "thumbnail"
MANUAL_TAGGING_FOLDER = TEMP_FOLDER / "manual_tagging"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(TAGGED_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)
os.makedirs(MANUAL_TAGGING_FOLDER, exist_ok=True)

# Chargement du token Genius
if not GENIUS_TOKEN_FILE.exists():
    raise FileNotFoundError(f"Genius token file not found: {GENIUS_TOKEN_FILE}")

with open(GENIUS_TOKEN_FILE, "r", encoding="utf-8") as f:
    GENIUS_TOKEN = f.read().strip()

# Variables pour le tagging
ARTIST_SEPARATOR = str(_tag_config["artist_separator"])
FILE_FORMAT = _tag_config["file_format"]
FILE_TREE_FORMAT = _tag_config["file_tree_format"]
