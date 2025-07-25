#!/usr/bin/env bash

# Update packages
apt-get update
pip install -r requirements.txt

# Optional: Download NLTK data in build phase
python -m nltk.downloader stopwords wordnet vader_lexicon

# Install Chromium and ChromeDriver
apt-get install -y chromium-browser chromium-chromedriver

# Make sure environment variables point to the right paths (optional, safe)
export CHROME_BIN=/usr/bin/chromium-browser
export PATH=$PATH:/usr/bin
