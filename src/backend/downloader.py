import asyncio
import threading
from spotdl import Spotdl
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def start_download(query=None):
    t = threading.Thread(target=_download_thread, args=(query,), daemon=True)
    t.start()

def _download_thread(query):
    try:
        spotdl = Spotdl(client_id=client_id, client_secret=client_secret)

        if query is None:
            msg = "No link provided."
            return

        print("Query in _download_thread:", query)
        print("Searching for:", query)
        songs = spotdl.search([query])
        spotdl.download_songs(songs)

        msg = "Download completed successfully."
    except Exception as e:
        msg = f"An error occurred during download: {e}"
