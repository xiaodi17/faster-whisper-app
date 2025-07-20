#!/usr/bin/env python3
"""Quick test script for the faster-whisper app."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        print("🧪 Testing imports...")
        
        from faster_whisper_app.core.transcriber import FasterWhisperTranscriber
        from faster_whisper_app.core.recorder import AudioRecorder  
        from faster_whisper_app.interfaces.hotkey_handler import DoubleCtrlHotkeyHandler
        from faster_whisper_app.interfaces.terminal_interface import TerminalInterface
        from faster_whisper_app.config import load_config
        
        print("✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test configuration loading."""
    try:
        print("⚙️ Testing configuration...")
        
        from faster_whisper_app.config import load_config
        config = load_config()
        
        print(f"✅ Config loaded: model={config.model_size}, device={config.device}")
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_terminal_interface():
    """Test terminal interface."""
    try:
        print("🖥️ Testing terminal interface...")
        
        from faster_whisper_app.interfaces.terminal_interface import TerminalInterface
        
        terminal = TerminalInterface()
        terminal.show_status("Test message", "green")
        
        print("✅ Terminal interface working!")
        return True
        
    except Exception as e:
        print(f"❌ Terminal interface test failed: {e}")
        return False

def test_audio_devices():
    """Test audio device detection."""
    try:
        print("🎤 Testing audio devices...")
        
        from faster_whisper_app.core.recorder import AudioRecorder
        
        recorder = AudioRecorder()
        devices = recorder.list_audio_devices()
        
        print(f"✅ Found {len(devices)} audio input devices")
        
        if devices:
            print(f"   Example: {devices[0]['name']}")
        
        recorder.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Audio device test failed: {e}")
        return False

def test_dependencies():
    """Test key dependencies."""
    dependencies = [
        ('faster_whisper', 'faster-whisper'),
        ('keyboard', 'keyboard'),
        ('pyaudio', 'pyaudio'),
        ('rich', 'rich'),
        ('click', 'click'),
        ('dotenv', 'python-dotenv')
    ]
    
    print("📦 Testing dependencies...")
    
    all_good = True
    for module, package in dependencies:
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - run: pip install {package}")
            all_good = False
    
    return all_good

def main():
    """Run all tests."""
    print("🚀 Testing faster-whisper-app setup")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_imports,
        test_config,
        test_terminal_interface,
        test_audio_devices,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Ready to run:")
        print("   python -m faster_whisper_app")
        print("   or")
        print("   python src/faster_whisper_app/cli.py run")
    else:
        print("❌ Some tests failed. Check dependencies and setup.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)