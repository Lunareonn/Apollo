from flask import Flask, render_template, Response
import time
import queue
import threading
import logging

app = Flask(__name__, static_folder="assets", template_folder="html")


def generate_logs():
    while True:
        time.sleep(0.3)
        # Format NEEDS to have "data: " before the message
        # and "\n\n" after the message.
        yield "data: test log\n\n"


@app.route("/logs")
def logs():
    return Response(generate_logs(), content_type="text/event-stream")


@app.route("/")
def index():
    return render_template("index.html")
