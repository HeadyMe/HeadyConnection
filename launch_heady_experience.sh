#!/bin/bash
# launch_heady_experience.sh
# Sets up dependencies and launches the HeadyLens TUI

echo "Installing dependencies..."
pip install rich > /dev/null 2>&1

echo "Launching HeadyLens..."
python3 HeadyLens_Installer.py
