import re
import getpass
import sys
from backend.logger import log

def example_directory():
    username = getpass.getuser()
    if sys.platform == "win32":
        path = f"C:\\Users\\{username}\\Downloads"
        return path
    elif sys.platform == "linux":
        path = f"/home/{username}/Downloads"
        return path
    elif sys.platform == "darwin":
        path = f"/Users/{username}/Downloads"
        return path

def validate_link(query):
    pattern = r"https://open\.spotify\.com/(album|track|artist|playlist)/[a-zA-Z0-9]{22}"
    if re.match(pattern, query):
        return True
    else:
        return False