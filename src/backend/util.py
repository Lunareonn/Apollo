import re
import getpass
import sys
import os
import toml
import json
from backend.logger import log, log_queue

def check_config():
    if sys.platform == "linux":
        home_folder = os.path.join(os.path.expanduser("~"))
        if os.path.isfile(os.path.join(home_folder, ".config", "apollo", "config.toml")):
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

            config.setdefault("downloader", {})
            config["downloader"]["directory"] = default_directory()

            config.setdefault("secrets", {})
            config["secrets"]["client_id"] = ""
            config["secrets"]["client_secret"] = ""

            with open(os.path.join(home_folder, ".config", "apollo", "config.toml"), "w") as f:
                toml.dump(config, f)

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