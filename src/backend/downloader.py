import logging
import threading
import queue as _queue
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

_task_queue = _queue.Queue()
_worker_thread = None
_worker_lock = threading.Lock()
_worker_started = False

def _log(msg):
    logger.info(msg)
    if log_queue:
        try:
            log_queue.put(msg)
        except Exception:
            pass

def start_download(query=None):
    # t = threading.Thread(target=_download_thread, args=(query,), daemon=True)
    # t.start()
    global _worker_thread, _worker_started
    with _worker_lock:
        if not _worker_started:
            _worker_thread = threading.Thread(target=_worker_loop, daemon=True)
            _worker_thread.start()
            _worker_started = True
    _task_queue.put(query)

def _worker_loop():
    try:
        spotdl = Spotdl(client_id=client_id, client_secret=client_secret)
    except Exception as e:
        _log(f"Failed to initialize Spotdl: {e}")
        return
    
    _log("Worker thread started.")

    while True:
        task = _task_queue.get()
        try:
            if task is None:
                _log("Downloader worker received shutdown signal.")
                break

            query = task
            if query == "" or query is None:
                msg = "No link provided."
                _log(msg)
                continue

            if isinstance(query, list):
                query_list = [query]
            elif isinstance(query, (list, tuple)):
                query_list = list(query)
            else:
                query_list = [str(query)]

            _log(f"Starting download for query: {query_list}")
            try:
                songs = spotdl.search(query_list)
                spotdl.download_songs(songs)
                msg = "Download completed successfully."
                _log(msg)
            except Exception as e:
                msg = f"An error occurred during download: {e}"
                _log(msg)

        finally:
            _task_queue.task_done()

def stop_worker(wait=True):
    global _worker_started
    if _worker_started:
        _task_queue.put(None)
        if wait and _worker_thread is not None:
            _worker_thread.join()
        _worker_started = False

# def _download_thread(query):
#     try:
#         # spotdl = Spotdl(client_id=client_id, client_secret=client_secret)

#         if query == "" or query is None:
#             msg = "No link provided."
#             logger.info(msg)
#             if log_queue:
#                 try:
#                     log_queue.put(msg)
#                 except Exception:
#                     pass
#             return

#         songs = spotdl.search([query])
#         spotdl.download_songs(songs)

#         msg = "Download completed successfully."
#         logger.info(msg)
#         log_queue.put(msg)
#     except Exception as e:
#         msg = f"An error occurred during download: {e}"
#         logger.info(msg)
#         log_queue.put(msg)
