# Faster-Whisper Global Hotkey Speech-to-Text App

A simple speech-to-text application using SYSTRAN's faster-whisper that responds to global hotkeys and types transcriptions directly into active applications.

## Features

- 🎙️ **Global Hotkey**: Press `F1` to start/stop recording from anywhere
- ⚡ **Fast Processing**: Uses optimized faster-whisper with int8 compute for speed
- 🌍 **Multi-language**: Automatic language detection
- ⌨️ **Direct Typing**: Types transcribed text into any active application
- 🎯 **Simple Setup**: One command installation with uv

## 🚀 Quick Setup

**Modern setup with uv (recommended):**

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/xiaodi17/faster-whisper-app
cd faster-whisper-app

# Install everything (Python 3.11 + dependencies)
uv sync

# Run the application
uv run faster-whisper-app
```

**Alternative (traditional pip):**

```bash
pip install -e .
faster-whisper-app
```

## 🎮 Usage

1. **Press `F1`** → Start recording
2. **Speak clearly** → Audio is captured
3. **Press `F1` again** → Stop recording and transcribe
4. **View results** → See transcription in terminal + typed into active app

## ⚙️ Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key settings:

- `FASTER_WHISPER_MODEL_SIZE`: tiny, base, small, medium, large (default: small)
- `FASTER_WHISPER_DEVICE`: cpu, cuda (default: cpu)
- `HOTKEY`: Global hotkey combination (default: f1)

## 🛠️ Development

```bash
# Format code
make format

# Run tests
make test

# Start app
make start
```

## Requirements

- Python 3.11+
- Microphone access
- ~300MB disk space (for small model)

## License

MIT License - see LICENSE file for details.
