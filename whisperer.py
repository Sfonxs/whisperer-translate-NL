# This script is a voice-to-text application that uses the OpenAI API to transcribe audio recordings.
# It imports necessary libraries for handling audio input, environment variables, and keyboard events.
# The script initializes global variables to manage the recording state, audio data, and other flags.
# The main function sets up the environment by loading variables from a .env file and defining a helper
# function to get the correct resource path for the API key file. It then prints instructions for the user
# on how to operate the application, such as holding the right CTRL key to start recording and pressing
# the right SHIFT key to enable translation to Dutch. The script also includes error handling to notify
# the user if the API key file is missing.


import sys, os
import sounddevice as sd
import numpy as np
import openai
import pyperclip
from pynput.keyboard import Listener, Controller, Key, KeyCode
import soundfile
from dotenv import load_dotenv

import tkinter as tk
import threading

# Only available on Windows by default:
try:
    import winsound
except ImportError:
    winsound = None

# Initialize global variables
recording = False
audio_data = []
stream = None
translate = False
force_clipboard = False

# We'll store references to our Tk objects here
root = None
status_label = None

def set_status(text):
    """Update the Tkinter status label (thread-safe)."""
    global root, status_label
    
    # If Tkinter is not initialized or there's no UI, just print to console
    if root is None or status_label is None:
        print(f"Status: {text}")
        return
        
    # Use `event_generate` for thread-safe UI updates
    def update_label(evt):
        status_label.config(text=text)

    try:
        root.event_generate("<<StatusUpdate>>", when="tail")
        root.bind("<<StatusUpdate>>", update_label, add="+")
    except Exception as e:
        print(f"UI update error: {str(e)}")

def play_tone(frequency=800, duration=0.1, volume=0.3):
    """Play a synthesized tone in a background thread to avoid blocking."""
    def _play():
        try:
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            # Generate a sine wave
            tone = np.sin(frequency * t * 2 * np.pi)
            # Apply volume
            tone = tone * volume
            # Play the tone
            sd.play(tone, sample_rate)
            sd.wait()
        except Exception as e:
            # Silently ignore audio playback errors
            pass
    
    # Play in a background thread to avoid blocking
    threading.Thread(target=_play, daemon=True).start()

def init_ui():
    """Initialize the Tkinter UI if needed"""
    global root, status_label
    
    try:
        # Create Tkinter window
        root = tk.Tk()
        root.title("Whisperer")
        root.geometry("300x100")
        
        # Create status label
        status_label = tk.Label(root, text="Idle", font=("Arial", 14))
        status_label.pack(pady=20)
        
        # Update UI in background thread
        def update_ui():
            try:
                root.mainloop()
            except Exception as e:
                print(f"UI error: {str(e)}")
                
        ui_thread = threading.Thread(target=update_ui, daemon=True)
        ui_thread.start()
        return True
    except Exception as e:
        print(f"Could not initialize UI: {str(e)}")
        root = None
        status_label = None
        return False

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize UI (optional)
        # Comment out the next line if you don't want a UI window
        # init_ui()
        
        # Helper function to get the correct resource path
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        # Updated API key file path using the resource helper
        api_key_path = resource_path('openai_api_key.txt')

        print("=== Whisperer Voice-to-Text ===")
        print("Hold right CTRL to record")
        print("Press right SHIFT while recording to translate to Dutch")
        print("Press CTRL+C to exit")
        print("Waiting for input...")

        # Key to hold down to start recording
        record_key = Key.ctrl_r

        # Key to tap turn on translation
        translate_key = Key.shift_r

        # Print a nice message if the API key file isn't present.
        try:
            with open(api_key_path, 'r') as file:
                pass
        except FileNotFoundError:
            print(f"Please create a file called {api_key_path} and paste your OpenAI API key in it.")
            exit()

        # Read the API key from the file
        with open(api_key_path, 'r') as file:
            openai.api_key = file.read().strip()

        # Callback function to collect audio data
        def callback(indata, frames, time, status):
            global audio_data
            if recording:
                # Check if indata has the expected shape (e.g., (32,))
                if indata.shape[1] == 1:  # Check if indata is mono
                    audio_data.append(indata.copy())
                else:
                    # Resize indata or discard it
                    pass

        keyboard = Controller()

        def on_press(key):
            global recording, stream, audio_data, translate

            if key == record_key and not recording:
                recording = True
                translate = False
                set_status("Recording...")
                
                # Play start recording tone (higher pitch)
                play_tone(frequency=800, duration=0.1)

                audio_data = []
              
                # Initialize and start InputStream
                stream = sd.InputStream(callback=callback, channels=1, samplerate=16000)
                stream.start()

            # If recording and the translate key is pressed, set translate to True and throw away the keypress.
            if recording and key == translate_key:
                print("Translate key pressed.")
                translate = True
              
        def process_audio(audio_data_copy, should_translate, keyboard_controller):
            """Process audio in a background thread to avoid blocking new recordings."""
            global force_clipboard
            
            try:
                if audio_data_copy == []:
                    print("No audio data recorded.")
                    return
              
                # Concatenate all audio data into one NumPy array
                audio_data_np = np.concatenate(audio_data_copy, axis=0)

                # Get length of audio data in seconds
                audio_data_length = len(audio_data_np) / 16000

                if audio_data_length < 0.5:
                    force_clipboard = True

                if audio_data_length < 1:
                    print("Audio data is less than 1 second long.")
                    return

                # Write audio data to file
                soundfile.write('output.flac', audio_data_np, 16000, format='flac')
              
                # Save or send the audio data to OpenAI Whisper
                with open("output.flac", "rb") as file:
                    print("Sending audio data to OpenAI Whisper...")
                    client = openai.OpenAI(api_key=openai.api_key)
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=file,
                
                    )
                    transcript_text = transcript.text

                    # Replace "New paragraph." with "\n"
                    transcript_text = transcript_text.replace("New paragraph.", "\n\n")

                    print("Transcript:")
                    print(transcript_text)

                    if should_translate:
                        print("Translating transcript to Dutch...")
                        result = openai.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You translate the input text to Dutch. You only output the translated text and nothing else. Avoid using the uw form as this is old fashioned"},
                                {"role": "user", "content": transcript_text},
                            ]
                        )

                        transcript_text = result.choices[0].message.content
                        print(transcript_text)

                    # Determine if any special characters are being used that can't be
                    # typed using keyboard.type(). These are any characters that aren't in English
                    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,;:!?-\'_')
                    special_chars = set(transcript_text) - allowed_chars
                    if len(special_chars) > 0 or force_clipboard:
                        print("Special characters detected: " + str(special_chars))

                        # Copy the transcript text to the clipboard
                        pyperclip.copy(transcript_text)

                        # Simulate CTRL-V to paste the text
                        keyboard_controller.press(Key.ctrl)
                        keyboard_controller.press('v')
                        keyboard_controller.release('v')
                        keyboard_controller.release(Key.ctrl)
                        force_clipboard = False
                    else:  
                        # Since there are no accents, we can just use the standard type command.
                        keyboard_controller.type(transcript_text)
            except Exception as e:
                print(f"Error processing audio: {str(e)}")
        
        def on_release(key):
            global recording, stream, translate, force_clipboard

            if key == record_key:
                recording = False
                set_status("Idle")
                
                # Play stop recording tone (lower pitch)
                play_tone(frequency=400, duration=0.1)

                # Stop and close InputStream
                if stream is not None:
                    stream.stop()
                    stream.close()
                    stream = None

                # Create a copy of the audio data and translate flag for the background thread
                audio_data_copy = audio_data.copy()
                should_translate = translate
                
                # Reset translate flag immediately
                translate = False
                
                # Process audio in background thread to allow immediate new recordings
                processing_thread = threading.Thread(
                    target=process_audio, 
                    args=(audio_data_copy, should_translate, keyboard),
                    daemon=True
                )
                processing_thread.start()
              
        # Start listening for key events
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
            
    except FileNotFoundError:
        print("\nError: Could not find openai_api_key.txt")
        print("Please ensure the API key file is in the same directory as the executable")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nPress Enter to exit...")
        input()

if __name__ == "__main__":
    main()
