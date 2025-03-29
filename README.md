/MusicDownloader/
│── /config/                  # Fichiers de configuration
│   ├── settings.json          # Configuration des tags et du format
│   ├── paths.json             # Définition des dossiers d'entrée et de sortie
│
│── /input/                    # Dossier contenant le fichier texte avec les liens YouTube
│   ├── links.txt              # Liste des liens YouTube
│
│── /temp/                     # Dossier temporaire pour les fichiers téléchargés
│
│── /music/                    # Dossier final contenant les musiques organisées
│
│── /src/                      # Code source du projet
│   ├── downloader.py          # Processus de téléchargement (PyTube)
│   ├── tagger.py              # Processus de retagging (Mutagen + Genius API)
│   ├── organizer.py           # Organisation des fichiers dans l'arborescence
│   ├── utils.py               # Fonctions utilitaires
│
│── main.py                    # Point d'entrée du programme
│── requirements.txt            # Dépendances du projet (PyTube, Mutagen, Requests, etc.)
│── README.md                   # Documentation du projet
```

---

### 🔥 Explication :
- **`/config/`** : Contient les fichiers de configuration (formats de tags, chemins des dossiers...).  
- **`/input/`** : Contient le fichier `links.txt` qui est surveillé en continu.  
- **`/temp/`** : Contient les fichiers téléchargés temporairement avant leur traitement.  
- **`/music/`** : Contiendra les fichiers MP3 classés selon l’arborescence définie.  
- **`/src/`** : Contient les scripts Python :
  - `downloader.py` : Télécharge les fichiers MP3 à partir de YouTube.
  - `tagger.py` : Récupère les tags via Genius et met à jour les métadonnées.
  - `organizer.py` : Trie et déplace les fichiers dans `/music/`.
  - `utils.py` : Fonctions utilitaires (formatage de texte, logs, etc.).
- **`main.py`** : Coordonne le tout.  
- **`requirements.txt`** : Liste des dépendances pour une installation facile.  
- **`README.md`** : Explication de l’utilisation du programme.  

---
