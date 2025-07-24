# Faster-Whisper Global Hotkey Speech-to-Text App

## Project Overview
A simple speech-to-text application using faster-whisper that responds to a global hotkey and types transcriptions directly into active applications.

## Core Concept
Press `F1` → Record audio → Transcribe with faster-whisper → Display in terminal + type to active app

## Technology Stack
- **Speech Recognition**: faster-whisper (SYSTRAN's optimized Whisper)
- **Global Hotkey**: keyboard library
- **Audio Recording**: pyaudio
- **Terminal Output**: rich (for beautiful formatting)
- **Text Output**: AppleScript integration to type into active applications

## Current Architecture

### Core Components
- `src/faster_whisper_app/core/transcriber.py` - Optimized transcriber with int8 compute
- `src/faster_whisper_app/core/recorder.py` - PyAudio recording
- `src/faster_whisper_app/interfaces/hotkey_handler.py` - Configurable hotkey handling
- `src/faster_whisper_app/interfaces/terminal_interface.py` - Rich terminal UI
- `src/faster_whisper_app/config.py` - Environment-based configuration

### Key Features
- **Modern Setup**: Uses pyproject.toml + uv package manager
- **Performance Optimized**: Small model + int8 compute for speed
- **Configurable Hotkeys**: Via .env file (default: F1)
- **Direct Typing**: AppleScript integration for typing into active apps
- **Rich Terminal Interface**: Beautiful panels and formatting

## Configuration
```python
# Default settings (optimized for speed)
MODEL_SIZE = "small"       # tiny, base, small, medium, large
DEVICE = "cpu"             # cpu or cuda
COMPUTE_TYPE = "int8"      # int8, float16, float32
HOTKEY = "f1"              # Global hotkey combination
```

## Modern Development Setup
```bash
# Primary workflow (uv)
uv sync
uv run faster-whisper-app

# Development shortcuts
make setup    # Install dependencies
make start    # Start the application
make test     # Run tests
make format   # Format code
```

## Performance Notes
- **Model Selection**: Uses "small" by default for optimal speed/accuracy balance
- **Compute Type**: int8 is much faster than float16 on CPU
- **Audio Processing**: Direct audio data processing without temp files
- **Async Text Output**: Non-blocking AppleScript execution with threading

## Error Handling Strategy
- Graceful failures with user-friendly error messages
- Timeout protection for AppleScript execution
- Comprehensive logging with timing information
- Safe cleanup of audio resources

## Key Workflow
1. Press F1 → Start recording (show status in terminal)
2. Speak normally → Audio capture continues
3. Press F1 → Stop recording, start transcription
4. Processing → Show "Processing..." with timing logs
5. Result → Display in terminal + type to active app

This implementation focuses on speed, simplicity, and direct integration with the user's workflow through global hotkeys and automatic text insertion.