import asyncio
import threading
from spotdl import Spotdl
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

spotdl = Spotdl(client_id=client_id, client_secret=client_secret)


def start_download():
    asyncio.run(song_download())


async def song_download():
    songs = spotdl.search(['joji - test drive'])
    spotdl.download_songs(songs)
