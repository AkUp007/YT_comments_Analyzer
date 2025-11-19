#!/usr/bin/env bash
set -o errexit

echo "⬇ Installing Chromium and Chromedriver..."

apt-get update

apt-get install -y chromium-browser chromium-chromedriver

echo "Chromium Installed Successfully!"
