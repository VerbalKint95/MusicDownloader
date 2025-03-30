import requests
import os

CONFIG_FILE = "config/genius_token.txt"
BASE_URL = "https://api.genius.com"

def load_api_token():
    """Charge le token API Genius depuis un fichier texte."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Le fichier de configuration '{CONFIG_FILE}' est introuvable.")
    
    with open(CONFIG_FILE, "r") as f:
        return f.read().strip()

GENIUS_API_TOKEN = load_api_token()

def search_song(query):
    """Recherche une chanson sur Genius et retourne l'ID du premier résultat trouvé."""
    url = f"{BASE_URL}/search"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    params = {"q": query}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Erreur API Genius: {response.status_code}")
        return None

    data = response.json()
    hits = data.get("response", {}).get("hits", [])

    if not hits:
        print(f"Aucun résultat trouvé pour : {query}")
        return None

    return hits[0]["result"]  # Retourne le premier résultat

def get_song_details(song_id):
    """Récupère les détails d'une chanson sur Genius."""
    url = f"{BASE_URL}/songs/{song_id}"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erreur API Genius: {response.status_code}")
        return None

    return response.json().get("response", {}).get("song", {})

if __name__ == "__main__":
    song = input("Entrez le nom de la chanson : ")
    result = search_song(song)
    if result:
        song_details = get_song_details(result["id"])
        print(song_details)