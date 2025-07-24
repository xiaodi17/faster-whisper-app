# Faster-Whisper Global Hotkey Speech-to-Text App

A simple speech-to-text application using SYSTRAN's faster-whisper that responds to global hotkeys and outputs transcriptions to both terminal and browser simultaneously.

## Features

- 🎙️ **Global Hotkey**: Press `Ctrl+Space` to start/stop recording from anywhere
- 🖥️ **Dual Output**: Transcriptions appear in both terminal and web browser
- ⚡ **Fast Processing**: Uses optimized faster-whisper for quick transcription
- 🌍 **Multi-language**: Automatic language detection
- 🎯 **Simple Setup**: One command installation

## 🚀 Quick Setup (Recommended - uv)

**One-command setup with uv (fastest and modern):**

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup everything
git clone https://github.com/yourusername/faster-whisper-app
cd faster-whisper-app

# Install Python 3.11 + all dependencies + run app
uv sync && uv run start
```

That's it! uv automatically:
- ✅ Installs Python 3.11 if needed
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Runs the application

## 📦 Alternative Setup (Traditional)

**Using pip and virtual environments:**

```bash
# Clone repository
git clone https://github.com/yourusername/faster-whisper-app
cd faster-whisper-app

# Ensure Python 3.11+ is installed
python --version  # Should be 3.11+

# Install the project
pip install -e .

# Run the application
faster-whisper-app
```

## 🎮 Usage

### **Modern Way (with uv):**
```bash
# Start the application
uv run start

# Run development workflow (format + lint + test + start)
uv run dev

# Run tests only
uv run test

# Format and lint code
uv run format
uv run lint

# Test individual components
uv run test-transcriber
uv run test-recorder
```

### **Traditional Way:**
```bash
# Run the application
faster-whisper-app

# Or use module syntax
python -m faster_whisper_app

# With CLI options
faster-whisper-app --model-size base --device cpu
```

### **Available Commands:**
```bash
faster-whisper-app run          # Start the app
faster-whisper-app transcribe   # Transcribe audio file
faster-whisper-app test         # Test installation
faster-whisper-app config       # Show configuration
```

## How It Works

1. **Press `Ctrl+Space`** → Start recording
2. **Speak clearly** → Audio is captured
3. **Press `Ctrl+Space` again** → Stop recording and transcribe
4. **View results** → See transcription in terminal AND browser

## Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Available settings:

- `FASTER_WHISPER_MODEL_SIZE`: tiny, base, small, medium, large (default: base)
- `FASTER_WHISPER_DEVICE`: cpu, cuda (default: cpu)
- `HOTKEY`: Global hotkey combination (default: ctrl+space)
- `WEB_PORT`: Web interface port (default: 8000)

## Troubleshooting

### PyAudio Installation Issues

**macOS:**

```bash
brew install portaudio
pip install pyaudio
```

**Ubuntu/Debian:**

```bash
sudo apt install portaudio19-dev
pip install pyaudio
```

**Windows:**

```bash
pip install pipwin
pipwin install pyaudio
```

### Permission Issues

**macOS:** Grant microphone access in System Preferences → Security & Privacy → Privacy → Microphone

**Linux:** Add user to audio group:

```bash
sudo usermod -a -G audio $USER
```

## Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/
```

## Project Structure

```
faster-whisper-app/
├── src/faster_whisper_app/
│   ├── core/                 # Core transcription engine
│   ├── interfaces/           # Terminal, web, hotkey interfaces
│   └── config.py            # Configuration management
├── tests/                   # Test suite
├── requirements.txt         # Dependencies
└── setup.sh               # Quick setup script
```

## Requirements

- Python 3.8+
- Microphone access
- ~500MB disk space (for base model)

## run in background mode

sudo bash -c "source venv/bin/activate && PYTHONPATH=src python -m faster_whisper_app"

## License

MIT License - see LICENSE file for details.
