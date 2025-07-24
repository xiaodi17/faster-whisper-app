"""
Faster-Whisper Global Hotkey Speech-to-Text App

A simple speech-to-text application that responds to global hotkeys
and types transcriptions directly into active applications.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.transcriber import FasterWhisperTranscriber

__all__ = ["FasterWhisperTranscriber"]
