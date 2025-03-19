# Whisperer Last UpDate:20250319

Whisperer is a Python application that records audio when a specific key is held down, and sends the audio to OpenAI's Whisper ASR system for transcription when another key is tapped. It then types the transcription into the active window.

## **Latest Version 20250319**: whisperer-NL-CR-SB_Output-PG

This is the newest and best version of Whisperer, featuring:
- Text transcription
- Dutch translation (NL)
- ChatGPT response generation (CR) 
- Search block formatting for medical databases (SB)
- Prompt generation/improvement for LLMs (PG)

## Prerequisites

- Python 3
- OpenAI API key

## Dependencies

- sounddevice
- numpy
- openai
- pynput
- scipy
- pyperclip
- pyinstaller (if you want to create an executable)
- dotenv (for environment variable management)

You can install these dependencies using pip:

```
pip install sounddevice numpy openai pynput scipy pyperclip pyinstaller dotenv
```

On Linux, also run:

```
sudo apt-get install xclip
```

## Setup

1. Clone the repository.
2. Create a file named openai_api_key.txt in the root directory of the project.
3. Paste your OpenAI API key into openai_api_key.txt.
4. Make an excutional file
5. place executional file in the same folder as the openai_api_key.tx file (i keep mine in a desk top folder)


## Building an Executable

After customizing the code, you can create a standalone executable that doesn't require Python to be installed:

### Method 1: Using the Provided Spec File

1. Make sure you have PyInstaller installed: `pip install pyinstaller`
2. After customizing `whisperer.py`, build the executable using the existing spec file (this can take several minutes to build):
   ```
   pyinstaller whisperer.spec
   ```
3. The executable will be created in the `dist` folder with the name specified in the spec file

### Method 2: Creating a New Spec File

If you want to change the executable name or other build settings:

1. Create a new spec file by running:
   ```
   pyinstaller --name your_custom_name --onefile --add-data "openai_api_key.txt;." whisperer.py
   ```
2. This will generate a `.spec` file that you can further customize if needed
3. Build the executable using your new spec file:
   ```
   pyinstaller your_custom_name.spec
   ```

### Running the Executable

1. Copy the executable file (e.g., `whisperer.exe` on Windows) to a folder
2. **IMPORTANT**: Create a file named `openai_api_key.txt` in the same folder and paste YOUR OWN OpenAI API key into it
3. Double-click the executable to run it

The executable is self-contained and includes all necessary dependencies, but it requires your own API key file in the same directory to function.

## Notes

- The audio is recorded at a sample rate of 16000 Hz and saved as output.flac.
- The application only records while the record key is held down.
- The application only translates when the translate key is tapped while recording.
- The application does not transcribe audio that is less than 1 second long.
- The application does not handle errors from the Whisper API.
