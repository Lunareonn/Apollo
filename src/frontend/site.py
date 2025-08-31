from flask import Flask, render_template, Response, jsonify, stream_with_context, request
import logging
from backend.downloader import start_download
from backend.logger import log_queue, queue
from backend.util import default_directory

app = Flask(__name__, static_folder="assets", template_folder="html")


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json(silent=True) or {}
    start_download(query=data.get("query"))
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
    return render_template("index.html", path=default_directory())
