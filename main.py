import speech_recognition as sr
import threading
from rapidfuzz import fuzz
from client import OBSClient

#pip install SpeechRecognition pyaudio rapidfuzz


WAKE_WORD = "bob"

# Define your command functions
def start_lights(obs: OBSClient):
    obs.scene.set_current_scene("Scene 3")
    print("Lights have been turned ON.")

def stop_lights(obs: OBSClient):
    obs.scene.set_current_scene("Scene 2")
    print("Lights have been turned OFF.")

# Command map (fuzzy match target -> function)
COMMANDS = {
    "switch to main scene": start_lights,
    "switch to music scene": stop_lights,
}

# Recognizer setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

def match_command(spoken_text):
    """Fuzzy match spoken command against known commands."""
    best_match = None
    highest_score = 0

    for cmd, func in COMMANDS.items():
        score = fuzz.ratio(spoken_text.lower(), cmd.lower())
        if score > highest_score:
            best_match = func
            highest_score = score

    if highest_score > 70:  # Threshold for fuzzy match
        return best_match
    return None

def listen_loop(obs: OBSClient):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for 'Bob'...")

        while True:
            try:
                audio = recognizer.listen(source)
                speech = recognizer.recognize_google(audio)
                print(f"You said: {speech}")

                if WAKE_WORD in speech.lower():
                    # Remove wake word and try to find command
                    command_part = speech.lower().split(WAKE_WORD, 1)[-1].strip()
                    if command_part:
                        action = match_command(command_part)
                        if action:
                            print("Command recognized. Executing...")
                            action(obs)
                        else:
                            print("Sorry, command not recognized.")
            except sr.UnknownValueError:
                pass  # Could not understand
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    try:    
        obs = OBSClient()
        listener_thread = threading.Thread(target=listen_loop, args=(obs,))
        listener_thread.start()
    except Exception as e:
        print(f"Error: {e}")
        print("Exiting...")
        exit(1)