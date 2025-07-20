#!/usr/bin/env python3
"""List available audio devices to find the Logitech camera."""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from faster_whisper_app.core.recorder import AudioRecorder

def list_audio_devices():
    """List all available audio input devices."""
    try:
        recorder = AudioRecorder()
        devices = recorder.list_audio_devices()
        
        print("🎤 Available Audio Input Devices:")
        print("=" * 50)
        
        for device in devices:
            print(f"Index: {device['index']}")
            print(f"Name: {device['name']}")
            print(f"Channels: {device['channels']}")
            print(f"Sample Rate: {device['sample_rate']} Hz")
            print("-" * 30)
        
        # Show default device
        try:
            default = recorder.get_default_input_device()
            print(f"\nDefault Device: {default['name']} (Index: {default['index']})")
        except Exception as e:
            print(f"Default device error: {e}")
        
        recorder.cleanup()
        
    except Exception as e:
        print(f"Error listing devices: {e}")

if __name__ == "__main__":
    list_audio_devices()