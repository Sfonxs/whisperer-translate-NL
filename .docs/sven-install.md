# Ubuntu Installation Commands

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-tk xclip portaudio19-dev python3-dev

# Create and activate virtual environment
cd /home/sven/projects/whisperer-translate-NL
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Create API key file
nano openai_api_key.txt
# (paste your OpenAI API key, save and exit)

# Run the app
python3 whisperer.py
```

## Usage

```bash
# To run in the future
cd /home/sven/projects/whisperer-translate-NL
source venv/bin/activate
python3 whisperer-NL-CR-SB-PG.py
```

