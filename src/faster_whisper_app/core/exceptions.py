"""Custom exceptions for faster-whisper-app."""


class FasterWhisperAppError(Exception):
    """Base exception for faster-whisper-app."""
    pass


class TranscriptionError(FasterWhisperAppError):
    """Raised when transcription fails."""
    pass


class AudioRecordingError(FasterWhisperAppError):
    """Raised when audio recording fails."""
    pass


class ModelLoadError(FasterWhisperAppError):
    """Raised when model loading fails."""
    pass


class DeviceError(FasterWhisperAppError):
    """Raised when audio device is unavailable."""
    pass