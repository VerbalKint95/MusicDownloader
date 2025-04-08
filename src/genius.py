from config import GENIUS_TOKEN
import requests

BASE_URL = "https://api.genius.com"

def search_song(query):
    """Recherche une chanson sur Genius et retourne l'ID du premier résultat trouvé."""
    url = f"{BASE_URL}/search"
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
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
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erreur API Genius: {response.status_code}")
        return None

    return response.json().get("response", {}).get("song", {})


def enhanceTag(mp3: str):
    return
