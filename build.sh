#!/bin/bash
set -o errexit

# Install Python packages
pip install -r requirements.txt

# Install Chromium and ChromeDriver
apt-get update
apt-get install -y chromium chromium-driver

# (Optional) For NLTK if needed
# python -m nltk.downloader stopwords vader_lexicon

echo "Build completed."
