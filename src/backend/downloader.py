import logging
import threading
import queue as _queue
from spotdl import Spotdl
from backend.utils import validate_link
from dotenv import load_dotenv
from backend.logger import log
import os

load_dotenv()
logger = logging.getLogger("downloader")

_task_queue = _queue.Queue()
_worker_thread = None
_worker_lock = threading.Lock()
_worker_started = False

def start_download(query=None):
    global _worker_thread, _worker_started
    with _worker_lock:
        if not _worker_started:
            _worker_thread = threading.Thread(target=_worker_loop, daemon=True)
            _worker_thread.start()
            _worker_started = True
    _task_queue.put(query)

def _worker_loop():
    try:
        spotdl = Spotdl(client_id=os.getenv("SPOTIFY_CLIENT_ID"), client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"), downloader_settings={
            "output": "{artists} ({album}) - {title}.{output-ext}",
            "bitrate": "128k"
        })
    except Exception as e:
        log(f"Failed to initialize Spotdl: {e}")
        return
    
    log("Worker thread started.")

    while True:
        task = _task_queue.get()
        try:
            if task is None:
                log("Worker received shutdown signal.")
                break

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

            if isinstance(query, list):
                query_list = [query]
            elif isinstance(query, (list, tuple)):
                query_list = list(query)
            else:
                query_list = [str(query)]

            log(f"Starting download for query: {query_list}")
            try:
                songs = spotdl.search(query_list)
                spotdl.download_songs(songs)
                msg = "Download completed successfully."
                log(msg)
            except Exception as e:
                msg = f"An error occurred during download: {e}"
                log(msg)

        finally:
            _task_queue.task_done()

def stop_worker(wait=True):
    global _worker_started
    if _worker_started:
        _task_queue.put(None)
        if wait and _worker_thread is not None:
            _worker_thread.join()
        _worker_started = False
