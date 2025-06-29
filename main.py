import whisper
import pyaudio
import wave
import threading
import tempfile
import speech_recognition as sr
from rapidfuzz import fuzz
from client import OBSClient  # Make sure this client is working correctly with your OBS

import re

# Constants
WAKE_WORD = "bob"
RECORD_SECONDS = 5
SAMPLE_RATE = 16000
CHUNK = 1024
CHANNELS = 1
FORMAT = pyaudio.paInt16

# Load Whisper model
model = whisper.load_model("base")

# Audio setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Utility: clean + normalize text
def clean_text(text):
    return re.sub(r'[^\w\s]', '', text).lower().strip()

def words_to_numbers(text):
    numbers = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6", "seven": "7",
        "eight": "8", "nine": "9", "ten": "10"
    }
    for word, digit in numbers.items():
        text = text.replace(word, digit)
    return text

def normalize(text):
    return words_to_numbers(clean_text(text))

# Transcribe with Whisper
def transcribe_with_whisper(audio_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_data.get_wav_data())
        tmp_path = tmp.name
    result = model.transcribe(tmp_path, fp16=False)
    return result["text"]

# Fuzzy match spoken scene to OBS scenes
def match_and_switch_scene(obs: OBSClient, spoken_text: str):
    try:
        scenes = obs.scene.get_scene_list()
        scene_names = [scene['sceneName'] for scene in scenes]
    except Exception as e:
        print(f"[OBS Error] Could not fetch scene list: {e}")
        return False

    normalized_spoken = normalize(spoken_text)

    best_match = None
    best_score = 0

    for scene_name in scene_names:
        normalized_scene = normalize(scene_name)
        score = fuzz.token_set_ratio(normalized_spoken, normalized_scene)
        print(f"🔍 Matching '{normalized_spoken}' to '{scene_name}' - Score: {score}")
        if score > best_score:
            best_score = score
            best_match = scene_name

    if best_score > 50:
        try:
            obs.scene.set_current_scene(best_match)
            print(f"✅ Switched to scene: {best_match} (confidence: {best_score})")
            return True
        except Exception as e:
            print(f"[OBS Error] Could not switch scene: {e}")
    else:
        print(f"❌ No strong match found for: '{spoken_text}'")
    return False

# Main loop
def listen_loop(obs: OBSClient):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎙️ Listening for wake word...")

        while True:
            try:
                print("🔊 Say something...")
                audio = recognizer.listen(source, phrase_time_limit=RECORD_SECONDS)
                transcript = transcribe_with_whisper(audio)
                print(f"🗣️ You said: {transcript}")

                if WAKE_WORD in transcript.lower():
                    command_text = transcript.lower().split(WAKE_WORD, 1)[-1].strip()
                    if command_text:
                        matched = match_and_switch_scene(obs, command_text)
                        if not matched:
                            print("⚠️ Command not recognized.")
            except Exception as e:
                print(f"🎧 Error: {e}")

# Start
if __name__ == "__main__":
    try:
        obs = OBSClient()
        thread = threading.Thread(target=listen_loop, args=(obs,))
        thread.start()
    except Exception as e:
        print(f"🔥 Startup error: {e}")
