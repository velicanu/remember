import hashlib
import json
import os
import subprocess
from pathlib import Path

# Imports the Google Cloud client library
from google.cloud import speech

STATE_FILE = os.path.join(os.path.dirname(__file__), "data", "state")


def get_state():
    return json.load(open(STATE_FILE)) if os.path.exists(STATE_FILE) else {}


def put_state(state):
    json.dump(state, open(STATE_FILE, "w"))


def cache(func):
    def saved(*args, **kwargs):
        file_name = kwargs["file_"]
        with open(file_name, "rb") as f:
            hash_ = hashlib.sha256(f.read()).hexdigest()
        state = get_state()

        if state.get("hash") == hash_:
            return state["transcript"]

        return func(*args, **kwargs)

    return saved


@cache
def transcribe(file_):
    if os.stat(file_).st_size == 0:
        return

    # Instantiates a client
    client = speech.SpeechClient()
    filename = Path(file_)
    wav_file = filename.with_suffix(".wav")

    subprocess.run(
        f"ffmpeg -i {file_} -vn -acodec pcm_s16le -ar 16000 -ac 2 {wav_file}".split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Loads the audio into memory
    with open(wav_file, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        audio_channel_count=2,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        with open(file_, "rb") as f:
            hash_ = hashlib.sha256(f.read()).hexdigest()

        put_state({"hash": hash_, "transcript": result.alternatives[0].transcript})

        return result.alternatives[0].transcript
