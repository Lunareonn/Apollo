from flask import Flask, render_template, Response, jsonify, stream_with_context
import logging
import backend.downloader
from backend.logger import log_queue, queue

app = Flask(__name__, static_folder="assets", template_folder="html")


def log_message(msg):
    logger = logging.getLogger()
    logger.info("hi")


@app.route("/download", methods=["POST"])
def download():
    backend.downloader.song_downloader()
    return jsonify({'status': 'success', 'message': "Downloading, this might take a while."})


@app.route("/logs")
def logs():
    def event_stream():
        while True:
            try:
                message = log_queue.get(timeout=1)
                yield f"data: {message}\n\n"
            except queue.Empty:
                pass
    return Response(stream_with_context(event_stream()), headers={
        "Content-Type": "text/event-stream",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    })


@app.route("/")
def index():
    return render_template("index.html")
