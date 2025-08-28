import logging
import threading
from spotdl import Spotdl
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

try:
    from backend.logger import log_queue
except Exception as e:
    print(e)
    log_queue = None

print(log_queue)
logger = logging.getLogger(__name__)

def start_download(query=None):
    t = threading.Thread(target=_download_thread, args=(query,), daemon=True)
    t.start()

def _download_thread(query):
    try:
        spotdl = Spotdl(client_id=client_id, client_secret=client_secret)

        if query == "" or query is None:
            msg = "No link provided."
            logger.info(msg)
            if log_queue:
                try:
                    log_queue.put(msg)
                except Exception:
                    pass
            return

        songs = spotdl.search([query])
        spotdl.download_songs(songs)

        msg = "Download completed successfully."
        logger.info(msg)
        log_queue.put(msg)
    except Exception as e:
        msg = f"An error occurred during download: {e}"
        logger.info(msg)
        log_queue.put(msg)
