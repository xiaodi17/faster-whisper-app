#!/usr/bin/env python3
"""Simple launcher script for faster-whisper-app."""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now import and run the app
from faster_whisper_app.__main__ import main

if __name__ == "__main__":
    main()