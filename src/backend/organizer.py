import os
import re
from backend.logger import log
from spotdl.utils import metadata

def sanitize(string):
    pattern = r"[\"*/:<>?\\]"
    replaced_quotes = re.sub(r'"', "'", string)
    sanitized = re.sub(pattern, "-", replaced_quotes)

    return sanitized

def create_folder_structure(songs):
    for song in songs:
        log("Sanitizing filename:", song[1])
        sanitized = sanitize(song[1])
        try:
            log("Fetching metadata for:", sanitized)
            song_metadata = metadata.get_file_metadata(
                sanitized, id3_separator=", ")
        except AttributeError as e:
            log(f"AttributeError! {e}")
            continue
        except OSError as e:
            log(f"OSError! {e}")
            continue

        # Finish later. TODO: Fetch directory for downloaded songs from config. Also fix errors
