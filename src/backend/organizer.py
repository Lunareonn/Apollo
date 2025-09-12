import re
import os
import json
import traceback
from pathlib import Path
from backend.logger import log
from backend.util import default_directory, fetch_config
from spotdl.utils import metadata

def sanitize(string):
    pattern = r"[\"*/:<>?\\]"
    replaced_quotes = re.sub(r'"', "'", str(string))
    sanitized = re.sub(pattern, "-", replaced_quotes)

    return Path(sanitized)

def create_folder_structure(songs):
    config = fetch_config()
    path = config["directory"]
    fallback_path = default_directory()

    for song in songs:
        if song[1] is None:
            log("A song download failed. Skipping.")
            continue
        sanitized = sanitize(song[1])
        try:
            log(f"Fetching metadata for: {sanitized}")
            song_metadata = metadata.get_file_metadata(
                sanitized, id3_separator="/")
        except AttributeError as e:
            log(f"AttributeError: {e}")
            traceback.print_exc()
            raise e
        except OSError as e:
            log(f"OSError: {e}")
            traceback.print_exc()
            raise e
        except Exception as e:
            log(f"Unexpected error while fetching metadata: {e}")
            traceback.print_exc()
            raise e

        if path is None or path == "":
            path = fallback_path

        directory = os.path.join(path, sanitize(song_metadata["album_artist"]), sanitize(song_metadata["album_name"]))
        log(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)
        log(f"Moving file {song[1]} to {directory}")
        os.rename(song[1], os.path.join(directory, song[1]))
