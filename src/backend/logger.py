import logging
import queue


log_queue = queue.Queue()


class SSELogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_queue.put(log_entry)


spotdl_logger = logging.getLogger("spotdl")
spotdl_logger.setLevel(logging.INFO)

downloader_logger = logging.getLogger("downloader")
downloader_logger.setLevel(logging.INFO)

sse_handler = SSELogHandler()
sse_handler.setFormatter(logging.Formatter("%(message)s"))
spotdl_logger.addHandler(sse_handler)

def log(msg):
    downloader_logger.info(msg)
    if log_queue:
        try:
            log_queue.put(msg)
        except Exception:
            pass