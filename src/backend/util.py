import re
import getpass
import sys
import os
import json
from backend.logger import log, log_queue

def check_config():
    if sys.platform == "linux":
        home_folder = os.path.join(os.path.expanduser("~"))
        if os.path.isfile(os.path.join(home_folder, ".config", "apollo", "config.json")):
            return True
        else:
            return False
    elif sys.platform == "win32":
        pass
        # write this later, im not arsed rn
    elif sys.platform == "darwin":
        pass
        # same with this

def generate_config():
    if check_config():
        return
    else:
        config = {}
        if sys.platform == "linux":
            home_folder = os.path.join(os.path.expanduser("~"))
            if not os.path.isdir(os.path.join(home_folder, ".config", "apollo")):
                os.makedirs(os.path.join(home_folder, ".config", "apollo"))

            dconfig = {
                "directory": default_directory(),
                "client_id": "",
                "client_secret": ""
            }
            config = json.dumps(dconfig, indent=4)

            with open(os.path.join(home_folder, ".config", "apollo", "config.json"), "w") as f:
                f.write(config)


def save_config(settings: dict):
    if sys.platform == "linux":
        home_folder = os.path.join(os.path.expanduser("~"))
        with open(os.path.join(home_folder, ".config", "apollo", "config.json"), "w") as f:
            json.dump(settings, f, indent=4)

def fetch_config():
    if sys.platform == "linux":
        home_folder = os.path.join(os.path.expanduser("~"))
        with open(os.path.join(home_folder, ".config", "apollo", "config.json"), "r") as f:
            config = json.load(f)
            return config

def send_warning(modal_name: str, message: str):
    payload = json.dumps({"type": "modal", "modal": modal_name, "message": message})
    try:
        log_queue.put(payload)
    except Exception as e:
        log(f"Failed to send warning modal: {e}")

def default_directory():
    username = getpass.getuser()
    if sys.platform == "win32":
        path = f"C:\\Users\\{username}\\Music"
        return path
    elif sys.platform == "linux":
        path = f"/home/{username}/Music"
        return path
    elif sys.platform == "darwin":
        path = f"/Users/{username}/Music"
        return path

def validate_link(query):
    pattern = r"https://open\.spotify\.com/(album|track|artist|playlist)/[a-zA-Z0-9]{22}"
    if re.match(pattern, query):
        return True
    else:
        return False