import logging
import queue
from frontend.extensions import socketio


log_queue = queue.Queue()

class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        socketio.emit("message", log_entry)


spotdl_logger = logging.getLogger("spotdl")
spotdl_logger.setLevel(logging.INFO)

downloader_logger = logging.getLogger("downloader")
downloader_logger.setLevel(logging.INFO)

sio_handler = SocketIOHandler()
sio_handler.setFormatter(logging.Formatter("%(message)s"))
spotdl_logger.addHandler(sio_handler)
downloader_logger.addHandler(sio_handler)

def log(msg):
    downloader_logger.info(msg)
    if log_queue:
        try:
            log_queue.put(msg)
        except Exception:
            pass