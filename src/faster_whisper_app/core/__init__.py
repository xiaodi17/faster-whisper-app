"""Core functionality for faster-whisper transcription."""

from .transcriber import FasterWhisperTranscriber
from .recorder import AudioRecorder
from .exceptions import TranscriptionError, AudioRecordingError

__all__ = ["FasterWhisperTranscriber", "AudioRecorder", "TranscriptionError", "AudioRecordingError"]