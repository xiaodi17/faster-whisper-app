# Faster-Whisper Global Hotkey Speech-to-Text App

## Project Overview
A simple speech-to-text application using faster-whisper that responds to a global hotkey and outputs transcriptions to both terminal and browser simultaneously.

## Core Concept
Press `Ctrl+Space` → Record audio → Transcribe with faster-whisper → Display in terminal AND browser

## Technology Stack
- **Speech Recognition**: faster-whisper (SYSTRAN's optimized Whisper)
- **Global Hotkey**: keyboard library
- **Audio Recording**: pyaudio
- **Terminal Output**: rich (for beautiful formatting)
- **Browser Output**: FastAPI + WebSockets
- **Frontend**: Simple HTML5 with JavaScript

## Project Structure (Following Python Best Practices)
```
faster-whisper-app/
├── README.md               # Project overview and usage
├── CLAUDE.md              # Development guide
├── pyproject.toml         # Modern Python packaging (PEP 518)
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── .gitignore            # Git ignore patterns
├── .env.example          # Environment variables template
├── src/
│   └── faster_whisper_app/
│       ├── __init__.py
│       ├── __main__.py    # Entry point for `python -m faster_whisper_app`
│       ├── cli.py         # Command line interface
│       ├── config.py      # Configuration management
│       ├── core/
│       │   ├── __init__.py
│       │   ├── transcriber.py    # faster-whisper wrapper
│       │   ├── recorder.py       # Audio recording utilities
│       │   └── exceptions.py     # Custom exceptions
│       ├── interfaces/
│       │   ├── __init__.py
│       │   ├── hotkey_handler.py # Global hotkey management
│       │   └── web_server.py     # FastAPI server
│       └── static/
│           ├── index.html        # Web interface
│           ├── style.css         # Styling
│           └── script.js         # WebSocket client
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Pytest configuration and fixtures
│   ├── test_transcriber.py
│   ├── test_recorder.py
│   └── integration/
│       └── test_end_to_end.py
├── docs/                  # Documentation
│   └── usage.md
└── scripts/              # Build and utility scripts
    ├── setup.sh
    └── test.sh
```

## Implementation Pattern

### 1. Core Transcriber (Based on faster-whisper repo example)
```python
from faster_whisper import WhisperModel

class SimpleTranscriber:
    def __init__(self, model_size="base"):
        # Use faster-whisper exactly as shown in their repo
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    def transcribe_file(self, audio_path):
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        # Combine segments into full text
        full_text = " ".join([segment.text for segment in segments])
        
        return {
            "text": full_text,
            "language": info.language,
            "confidence": info.language_probability,
            "segments": list(segments)
        }
```

### 2. Global Hotkey Handler
```python
import keyboard
import asyncio

class HotkeyHandler:
    def __init__(self, transcriber, output_handler):
        self.transcriber = transcriber
        self.output_handler = output_handler
        self.is_recording = False
        
    def setup_hotkey(self):
        keyboard.add_hotkey('ctrl+space', self.toggle_recording)
        print("🎧 Global hotkey registered: Ctrl+Space")
        
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_and_transcribe()
```

### 3. Dual Output Handler
```python
from rich.console import Console
import asyncio

class OutputHandler:
    def __init__(self):
        self.console = Console()
        self.websocket_clients = []  # Connected browser clients
        
    def output_to_terminal(self, result):
        # Beautiful terminal output with Rich
        self.console.print(f"🎙️ [{result['language']}] {result['text']}", style="green")
        
    async def output_to_browser(self, result):
        # Send to all connected WebSocket clients
        for websocket in self.websocket_clients:
            try:
                await websocket.send_json(result)
            except:
                self.websocket_clients.remove(websocket)
                
    async def output_everywhere(self, result):
        # Output to both terminal and browser
        self.output_to_terminal(result)
        await self.output_to_browser(result)
```

### 4. Simple Audio Recording
```python
import pyaudio
import wave
import tempfile

class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.frames = []
        
    def start_recording(self):
        # Simple PyAudio recording
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=1024
        )
        self.recording = True
        self.frames = []
        
    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
        # Save to temp file and return path
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        self.save_wav(temp_file.name)
        return temp_file.name
```

### 5. Simple Web Interface
```html
<!DOCTYPE html>
<html>
<head>
    <title>Speech-to-Text Live</title>
</head>
<body>
    <h1>🎙️ Live Transcription</h1>
    <div id="status">Ready - Press Ctrl+Space to start</div>
    <div id="transcriptions"></div>
    
    <script>
        const ws = new WebSocket('ws://localhost:8000/ws');
        
        ws.onmessage = function(event) {
            const result = JSON.parse(event.data);
            document.getElementById('transcriptions').innerHTML += 
                `<p><strong>[${result.language}]</strong> ${result.text}</p>`;
        };
    </script>
</body>
</html>
```

## Development Approach

### Phase 1: Core Implementation (30 minutes)
1. **Setup faster-whisper**: Follow their exact example
2. **Test transcription**: Use a sample audio file
3. **Add global hotkey**: Simple keyboard listener
4. **Terminal output**: Rich formatting

### Phase 2: Audio Recording (20 minutes)
1. **PyAudio setup**: Basic recording functionality
2. **Hotkey integration**: Start/stop recording
3. **File handling**: Temp file creation
4. **Error handling**: Basic audio errors

### Phase 3: Browser Output (30 minutes)
1. **FastAPI server**: Simple WebSocket endpoint
2. **HTML interface**: Basic real-time display
3. **WebSocket connection**: Send transcriptions to browser
4. **Dual output**: Terminal + browser simultaneously

### Phase 4: Polish (20 minutes)
1. **Error handling**: Graceful failures
2. **User feedback**: Recording status indicators
3. **Configuration**: Model size selection
4. **Documentation**: Usage instructions

## Key Features

### Global Hotkey Workflow
```
1. Press Ctrl+Space    → Start recording (show in terminal + browser)
2. Speak normally      → Audio capture continues
3. Press Ctrl+Space    → Stop recording, start transcription
4. Processing          → Show "Processing..." in both outputs
5. Result              → Display transcription in terminal + browser
```

### Dual Output Benefits
- **Terminal**: Great for developers, command-line users
- **Browser**: Great for sharing, easy access, rich formatting
- **Simultaneous**: Same transcription, same time, everywhere
- **Global Access**: Works regardless of focused application

## Configuration
```python
# config.py
MODEL_SIZE = "base"        # tiny, base, small, medium, large
DEVICE = "cpu"             # cpu or cuda
COMPUTE_TYPE = "int8"      # int8, float16, float32
HOTKEY = "ctrl+space"      # Global hotkey combination
SAMPLE_RATE = 16000        # Audio sample rate
WEB_PORT = 8000           # Browser interface port
```

## Dependencies

### pyproject.toml (Modern Python packaging)
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "faster-whisper-app"
version = "0.1.0"
description = "Global hotkey speech-to-text with dual terminal/browser output"
authors = [{name = "Your Name", email = "your.email@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "faster-whisper>=0.9.0",
    "keyboard>=0.13.5",
    "pyaudio>=0.2.11",
    "rich>=13.0.0",
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "websockets>=11.0.0",
    "click>=8.0.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
    "flake8>=6.0.0",
    "pre-commit>=3.0.0",
]

[project.scripts]
faster-whisper-app = "faster_whisper_app.cli:main"

[project.urls]
Homepage = "https://github.com/yourusername/faster-whisper-app"
Repository = "https://github.com/yourusername/faster-whisper-app"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
```

### requirements.txt (Production)
```txt
faster-whisper>=0.9.0
keyboard>=0.13.5
pyaudio>=0.2.11
rich>=13.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
websockets>=11.0.0
click>=8.0.0
python-dotenv>=1.0.0
```

### requirements-dev.txt (Development)
```txt
-r requirements.txt
pytest>=7.0.0
pytest-asyncio>=0.21.0
black>=23.0.0
isort>=5.12.0
mypy>=1.0.0
flake8>=6.0.0
pre-commit>=3.0.0
```

## Installation and Usage

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/faster-whisper-app
cd faster-whisper-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Production Installation
```bash
# Install from PyPI (when published)
pip install faster-whisper-app

# Or install from source
pip install .
```

### Usage
```bash
# Run as a module
python -m faster_whisper_app

# Or use the installed command
faster-whisper-app

# With configuration
faster-whisper-app --model-size base --device cpu

# Environment variables
export FASTER_WHISPER_MODEL_SIZE=small
export FASTER_WHISPER_DEVICE=cuda
python -m faster_whisper_app
```

## Development Commands
```bash
# Code formatting
black src/ tests/
isort src/ tests/

# Linting
flake8 src/ tests/
mypy src/

# Testing
pytest
pytest --cov=faster_whisper_app
pytest tests/integration/

# Run all quality checks
./scripts/test.sh

# Build package
python -m build

# Check dependencies
python -c "from faster_whisper import WhisperModel; print('✅ faster-whisper works')"
python -c "import pyaudio; print('✅ PyAudio works')"
python -c "import keyboard; print('✅ Keyboard works')"
```

## Error Handling Strategy
```python
def safe_transcribe(audio_file):
    try:
        return transcriber.transcribe_file(audio_file)
    except Exception as e:
        return {
            "text": f"❌ Transcription failed: {str(e)}",
            "language": "error",
            "confidence": 0.0
        }

def safe_record():
    try:
        return recorder.record_audio()
    except Exception as e:
        print(f"❌ Recording failed: {e}")
        return None
```

## Performance Notes
- **Model Selection**: Start with "base" for good speed/accuracy balance
- **Audio Quality**: 16kHz mono is optimal for Whisper models
- **Memory Usage**: Larger models require more RAM
- **Processing Time**: ~1-3 seconds for 10-second audio clips
- **Real-time Factor**: Usually faster than real-time transcription

## Security Considerations
- **Global Hotkey**: Only listens for specific key combination
- **Audio Privacy**: Audio files are temporary and cleaned up
- **Network**: WebSocket only accepts local connections by default
- **Permissions**: May require microphone access permissions

This simple approach focuses on the core functionality: global hotkey → record → transcribe → output everywhere. The implementation follows the faster-whisper repository examples directly while adding the dual-output capability.