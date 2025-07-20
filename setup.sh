#!/bin/bash
# Quick setup script for faster-whisper-app

echo "🚀 Setting up faster-whisper-app..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
echo "📋 Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Test installation
echo "🧪 Testing installation..."
python -c "from faster_whisper import WhisperModel; print('✅ faster-whisper works')" || echo "❌ faster-whisper failed"
python -c "import pyaudio; print('✅ PyAudio works')" || echo "❌ PyAudio failed - you may need to install portaudio"
python -c "import keyboard; print('✅ keyboard works')" || echo "❌ keyboard failed"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start using the app:"
echo "  source venv/bin/activate"
echo "  python -m faster_whisper_app"
echo ""
echo "If PyAudio failed:"
echo "  macOS: brew install portaudio"
echo "  Ubuntu: sudo apt install portaudio19-dev"
echo "  Windows: pip install pipwin && pipwin install pyaudio"