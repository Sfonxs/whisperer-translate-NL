# Step-by-Step Guide for Creating the Whisperer Executable on macOS

Here's a detailed guide for creating a Mac-compatible version of Whisperer:

## Prerequisites
- macOS operating system
- Internet connection
- An OpenAI API key

## Step 1: Install Python (if not already installed)
1. Open Terminal (you can find it in Applications > Utilities or search using Spotlight)
2. Check if Python is installed by running:
   ```bash
   python3 --version
   ```
3. If not installed, download and install from [python.org](https://www.python.org/downloads/macos/)

## Step 2: Set Up the Project
1. Create a new folder for the project
   ```bash
   mkdir ~/WhispererApp
   cd ~/WhispererApp
   ```
2. Download the source files I sent you and place them in this folder
3. Create a text file named `openai_api_key.txt` and paste YOUR OpenAI API key into it
   ```bash
   echo "your-api-key-goes-here" > openai_api_key.txt
   ```

## Step 3: Set Up a Python Virtual Environment
1. Open Terminal and navigate to your project folder:
   ```bash
   cd ~/WhispererApp
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
   (Your terminal prompt should change to show "(venv)" at the beginning)

## Step 4: Install Required Libraries
1. With the virtual environment active, install all required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure PyInstaller is installed:
   ```bash
   pip install pyinstaller
   ```

## Step 5: Create the Executable
1. Run PyInstaller to create the macOS executable:
   ```bash
   pyinstaller --onefile --add-data "openai_api_key.txt:." whisperer.py
   ```
   Note: This creates a command-line executable

2. For a more Mac-like application (with an icon in the dock), use:
   ```bash
   pyinstaller --onefile --windowed --add-data "openai_api_key.txt:." whisperer.py
   ```

3. Wait for PyInstaller to finish - this may take a few minutes

## Step 6: Find and Run Your Executable
1. Once complete, your executable will be in the `dist` folder
   ```bash
   cd dist
   ```
2. Run the executable:
   ```bash
   ./whisperer
   ```
   Or for the windowed version, find it in Finder and double-click it

3. The first time you run the application:
   - Right-click on the executable and select "Open"
   - You'll likely see a security warning - click "Open" again
   - macOS will ask for permission to access your microphone - allow this

## Troubleshooting Tips
- If you get a "not trusted" warning, go to System Preferences > Security & Privacy and click "Open Anyway"
- If the microphone isn't working, check that permission is granted in System Preferences > Security & Privacy > Microphone
- If you have issues with PyInstaller, try running in debug mode:
  ```bash
  pyinstaller --onefile --add-data "openai_api_key.txt:." --debug all whisperer.py
  ```

## Additional Notes
- The keyboard shortcuts might feel different on Mac - the app uses Right CTRL to record, which on Mac keyboards would be the Control key on the right side
- If there are any Mac-specific issues, let me know and I can help troubleshoot

This should get you up and running with your own Mac-compatible version of Whisperer!