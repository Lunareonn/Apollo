import re
import getpass
import sys
import os
import json
from backend.logger import log, log_queue

def check_config():
    home_folder = os.path.join(os.path.expanduser("~"))
    if sys.platform == "linux":
        if os.path.isfile(os.path.join(home_folder, ".config", "apollo", "config.json")):
            return True
        else:
            return False
    elif sys.platform == "win32":
        if os.path.isfile(os.path.join(home_folder, "AppData", "Local", "Apollo", "config.json")):
            return True
        else:
            return False
    elif sys.platform == "darwin":
        pass
        # same with this

def generate_config():
    if check_config():
        return
    else:
        home_folder = os.path.join(os.path.expanduser("~"))
        dconfig = {
            "directory": default_directory(),
            "client_id": "",
            "client_secret": ""
        }
        if sys.platform == "linux":
            if not os.path.isdir(os.path.join(home_folder, ".config", "apollo")):
                os.makedirs(os.path.join(home_folder, ".config", "apollo"))

            config = json.dumps(dconfig, indent=4)

            with open(os.path.join(home_folder, ".config", "apollo", "config.json"), "w") as f:
                f.write(config)
        if sys.platform == "win32":
            if not os.path.isdir(os.path.join(home_folder, "AppData", "Local", "Apollo")):
                os.makedirs(os.path.join(home_folder, "AppData", "Local", "Apollo"))

            config = json.dumps(dconfig, indent=4)

            with open(os.path.join(home_folder, "AppData", "Local", "Apollo", "config.json"), "w") as f:
                f.write(config)


def save_config(settings: dict):
    home_folder = os.path.join(os.path.expanduser("~"))
    if sys.platform == "linux":
        with open(os.path.join(home_folder, ".config", "apollo", "config.json"), "w") as f:
            json.dump(settings, f, indent=4)
    if sys.platform == "win32":
        with open(os.path.join(home_folder, "AppData", "Local", "Apollo", "config.json"), "w") as f:
            json.dump(settings, f, indent=4)

def fetch_config():
    home_folder = os.path.join(os.path.expanduser("~"))
    if sys.platform == "linux":
        with open(os.path.join(home_folder, ".config", "apollo", "config.json"), "r") as f:
            config = json.load(f)
            return config
    if sys.platform == "win32":
        with open(os.path.join(home_folder, "AppData", "Local", "Apollo", "config.json"), "r") as f:
            config = json.load(f)
            return config

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