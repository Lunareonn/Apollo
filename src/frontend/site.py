from flask import Flask, render_template, jsonify, request
from backend.downloader import start_download
from backend.util import default_directory, save_config, fetch_config
from frontend.extensions import socketio
import sys
import os

if getattr(sys, "frozen", False):
    template_folder = os.path.join(sys._MEIPASS, "html")
    static_folder = os.path.join(sys._MEIPASS, "assets")
else:
    template_folder = "html"
    static_folder = "assets"

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
socketio.init_app(app, async_mode="threading")

@socketio.on("download")
def handle_download(query):
    start_download(query=query)

@app.route("/save-settings", methods=["POST"])
def save_settings():
    try:
        save_config(request.get_json())
        return jsonify({"status": "Saved successfully"})
    except Exception:
        return jsonify({"status": "An error occured"})

@app.route("/get-settings", methods=["GET"])
def get_settings():
    config = fetch_config()
    return config

@app.route("/")
def index():
    return render_template("index.html", path=default_directory())
