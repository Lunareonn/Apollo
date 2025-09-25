from pydub import AudioSegment, silence
from backend.logger import log
from backend.util import fetch_config

def trim_silence(filepath):
    config = fetch_config()
    min_silence_len = config["min_silence_len"]
    silence_thresh = config["silence_thresh"]
    log(f"Trimming silence from {filepath}")
    audio = AudioSegment.from_file(filepath, format="mp3")
    silent_ranges = silence.detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh, seek_step=1)
    # Return original file is no silence is found
    if not silent_ranges:
        log("No silence detected, skipping trimming.")
        return filepath
    
    # Sort silence ranges
    silent_ranges.sort()

    # Set start trim and end trim points
    start_trim = 0
    end_trim = len(audio)

    first_start, first_end = silent_ranges[0]
    if first_start <= 0 + 10:
        start_trim = max(0, first_end - 0)

    last_start, last_end = silent_ranges[-1]
    if last_end >= len(audio) - 10:
        end_trim = min(len(audio), last_start + 0)

    if start_trim >= end_trim:
        audio.export(filepath, format="mp3")
        return
    
    trimmed = audio[start_trim:end_trim]
    trimmed.export(filepath, format="mp3")