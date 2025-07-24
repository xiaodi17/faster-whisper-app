# Faster-Whisper Global Hotkey Speech-to-Text App

A simple speech-to-text application using SYSTRAN's faster-whisper that responds to global hotkeys and outputs transcriptions to both terminal and browser simultaneously.

## Features

- 🎙️ **Global Hotkey**: Press `F1` to start/stop recording from anywhere
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
git clone https://github.com/xiaodi17/faster-whisper-app
cd faster-whisper-app

# Install Python 3.11 + all dependencies
uv sync

# Run the application
uv run python -m faster_whisper_app
```

That's it! uv automatically:

- ✅ Installs Python 3.11 if needed
- ✅ Creates virtual environment
- ✅ Installs all dependencies

## 📦 Alternative Setup (Traditional)

**Using pip and virtual environments:**

```bash
# Clone repository
git clone https://github.com/xiaodi17/faster-whisper-app
cd faster-whisper-app

# Ensure Python 3.11+ is installed
python --version  # Should be 3.11+

# Install the project
pip install -e .

# Run the application
faster-whisper-app
```

## 🎮 Usage

### **Method 1: Modern Way (with uv)**

```bash
# After running uv sync, start the app
uv run python -m faster_whisper_app

# Alternative: if CLI is installed globally
uv run faster-whisper-app
```

### **Method 2: Traditional Way (after pip install)**

```bash
# After pip install -e ., run the global command
faster-whisper-app

# Or use the short alias
fwa

# Or use module syntax
python -m faster_whisper_app

# With CLI options
faster-whisper-app --model-size base --device cpu
```

### **Method 3: Using Makefile (any setup)**

```bash
make start    # Automatically detects your setup and runs the app
make help     # Show all available commands
```

### **Method 4: Direct Python (for development)**

```bash
# If you have venv activated
python -m faster_whisper_app

# With specific options
python -m faster_whisper_app --model-size base --device cpu
```

## 🛠️ Development Commands

### **Code Quality:**

```bash
# Format code
black src/ tests/
isort src/ tests/
ruff format src/ tests/

# Lint code
ruff check src/ tests/
mypy src/

# Run tests
pytest tests/ -v
```

### **Available Commands:**

```bash
faster-whisper-app run          # Start the app
faster-whisper-app transcribe   # Transcribe audio file
faster-whisper-app test         # Test installation
faster-whisper-app config       # Show configuration
```

## How It Works

1. **Press `F1`** → Start recording
2. **Speak clearly** → Audio is captured
3. **Press `F1` again** → Stop recording and transcribe
4. **View results** → See transcription in terminal AND browser

## Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Available settings:

- `FASTER_WHISPER_MODEL_SIZE`: tiny, base, small, medium, large (default: base)
- `FASTER_WHISPER_DEVICE`: cpu, cuda (default: cpu)
- `HOTKEY`: Global hotkey combination (default: f1)
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

## License

MIT License - see LICENSE file for details.
