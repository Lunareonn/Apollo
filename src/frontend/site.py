from flask import Flask, render_template, jsonify, request
from backend.downloader import start_download
from backend.util import default_directory, save_config, fetch_config
from frontend.extensions import socketio

app = Flask(__name__, static_folder="assets", template_folder="html")
socketio.init_app(app)

@socketio.on("download")
def handle_download(query):
    start_download(query=query)

@app.route("/save-settings", methods=["POST"])
def save_settings():
    save_config(request.get_json())
    return jsonify({"status": "success"})

@app.route("/get-settings", methods=["GET"])
def get_settings():
    config = fetch_config()
    return config

@app.route("/")
def index():
    return render_template("index.html", path=default_directory())
