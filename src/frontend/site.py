from flask import Flask, render_template, Response, jsonify, stream_with_context, request
from flask_socketio import send, emit
from backend.downloader import start_download
from backend.util import default_directory
from frontend.extensions import socketio

app = Flask(__name__, static_folder="assets", template_folder="html")
socketio.init_app(app)

@socketio.on("download")
def handle_download(query):
    start_download(query=query)


@app.route("/")
def index():
    return render_template("index.html", path=default_directory())
