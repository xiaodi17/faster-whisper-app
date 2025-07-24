"""Basic setup tests to verify installation."""

import pytest


def test_faster_whisper_import():
    """Test that faster-whisper can be imported."""
    try:
        from faster_whisper import WhisperModel

        assert WhisperModel is not None
    except ImportError:
        pytest.fail("faster-whisper not installed properly")


def test_pyaudio_import():
    """Test that PyAudio can be imported."""
    try:
        import pyaudio

        assert pyaudio.PyAudio is not None
    except ImportError:
        pytest.fail("PyAudio not installed properly")


def test_keyboard_import():
    """Test that keyboard module can be imported."""
    try:
        import keyboard

        assert keyboard is not None
    except ImportError:
        pytest.fail("keyboard module not installed properly")


def test_core_imports():
    """Test that our core modules can be imported."""
    from faster_whisper_app.config import config
    from faster_whisper_app.core import AudioRecorder, FasterWhisperTranscriber

    assert FasterWhisperTranscriber is not None
    assert AudioRecorder is not None
    assert config is not None


def test_config_loading():
    """Test configuration loading."""
    from faster_whisper_app.config import load_config

    cfg = load_config()
    assert cfg.model_size in ["tiny", "base", "small", "medium", "large", "large-v3"]
    assert cfg.device in ["cpu", "cuda", "auto"]
    assert cfg.sample_rate > 0
    assert cfg.channels > 0
