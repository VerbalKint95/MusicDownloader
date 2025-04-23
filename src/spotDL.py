import subprocess
import logging
from config import DOWNLOAD_FOLDER

def download(url: str):
    """
    Télécharge une musique depuis une URL Spotify en utilisant SpotDL.
    """
    try:
        command = ["spotdl", url, "--output", DOWNLOAD_FOLDER]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            logging.info(f"Téléchargement réussi : {url}")
        else:
            logging.error(f"Échec du téléchargement : {url}\n{result.stderr}")
    except Exception as e:
        logging.error(f"Erreur lors du téléchargement de {url} : {str(e)}")

