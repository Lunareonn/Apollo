import logging
import threading
import json
import queue as _queue
from spotdl import Spotdl
from frontend.extensions import socketio
from backend.util import validate_link, fetch_config
from backend.organizer import create_folder_structure
from dotenv import load_dotenv
from backend.logger import log
import traceback
import os

load_dotenv()
logger = logging.getLogger("downloader")

_task_queue = _queue.Queue()
_worker_thread = None
_worker_lock = threading.Lock()
_worker_started = False

def start_download(query=None):
    config = fetch_config()
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    if not client_id or not client_secret:
        try:
            socketio.emit("warning", "Spotify credentials are missing. Please set them in the settings.")
            log("Spotify credentials are missing. Please set them in the settings.")
            return
        except Exception as e:
            log(f"Failed to send warning modal: {e}")
            return
    
    global _worker_thread, _worker_started
    with _worker_lock:
        if not _worker_started:
            _worker_thread = threading.Thread(target=_worker_loop, args=(client_id, client_secret), daemon=True)
            _worker_thread.start()
            _worker_started = True
    _task_queue.put(query)

def _worker_loop(client_id=None, client_secret=None):
    try:
        spotdl = Spotdl(client_id=client_id, client_secret=client_secret, downloader_settings={
            "output": "{artists} - {title} ({album}).{output-ext}",
            "bitrate": "128k",
            "lyrics_providers": ""
        })
    except Exception as e:
        log(f"Failed to initialize Spotdl: {e}")
        return
    
    log("Worker thread started.")

    while True:
        task = _task_queue.get()
        try:
            query = task
            if query == "" or query is None:
                log("No link provided.")
                continue

            is_valid_link = validate_link(query)
            if is_valid_link is False: 
                log("Invalid link. Only spotify links are supported.")
                continue
            elif is_valid_link is True:
                pass

            log(f"Starting download for query: {query}")
            try:
                songs = spotdl.search([query])
                downloaded_songs = spotdl.download_songs(songs)
                create_folder_structure(downloaded_songs)
                log("Download completed successfully.")
            except Exception as e:
                log(f"An error occurred during download: {e}")

        finally:
            _task_queue.task_done()

def stop_worker(wait=True):
    global _worker_started
    if _worker_started:
        _task_queue.put(None)
        if wait and _worker_thread is not None:
            _worker_thread.join()
        _worker_started = False
