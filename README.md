# Speech-to-Text App

**Press F1, speak, and watch your words instantly appear in any app.**

Transform your voice into text across your entire system. Press F1 from anywhere - whether you're in a text editor, browser, or chat app - speak naturally, and your words will be typed directly where your cursor is. No copy-pasting, no switching windows.

## How It Works

1. **Press F1** → Start recording (works from any application)
2. **Speak naturally** → Your voice is captured
3. **Press F1 again** → Voice converts to text and types automatically
4. **Done!** → Text appears wherever your cursor was

## Why You'll Love It

- 🎙️ **Works everywhere** - Email, documents, chat, code editors, web forms
- ⚡ **Lightning fast** - Optimized AI transcription in under 2 seconds
- 🌍 **Speaks your language** - Automatically detects 100+ languages
- ⌨️ **No interruptions** - Text appears directly where you're typing
- 🎯 **Easy setup** - Install and run in 30 seconds

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
