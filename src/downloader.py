import os
import spotDL
#import ytDL
from config import INPUT_FILE, NOTFOUND_FILE

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

    for url in urls:
        if "spotify" in url:
            spotDL.download(url)
        #elif "youtube" in url:
        #    not_found_urls.append(ytDL.download(url))
        else:
            not_found_urls.append(url)

    # Ajouter les URL échouées à notfound.txt
    if not_found_urls:
        os.makedirs(os.path.dirname(NOTFOUND_FILE), exist_ok=True)
        with open(NOTFOUND_FILE, "a") as f:
            for url in not_found_urls:
                f.write(url + "\n")

if __name__ == "__main__":
    process_links()