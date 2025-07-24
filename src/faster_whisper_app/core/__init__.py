"""Core functionality for faster-whisper transcription."""

from .exceptions import AudioRecordingError, TranscriptionError
from .recorder import AudioRecorder
from .transcriber import FasterWhisperTranscriber

__all__ = [
    "FasterWhisperTranscriber",
    "AudioRecorder",
    "TranscriptionError",
    "AudioRecordingError",
]
