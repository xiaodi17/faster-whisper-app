"""Configuration management for faster-whisper-app."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Application configuration."""

    # Model settings (optimized for speed)
    model_size: str = "small"  # Changed from "base" for 2x speed improvement
    device: str = "cpu"
    compute_type: str = "int8"  # Optimized for CPU - much faster than float16 on CPU

    # Audio settings
    sample_rate: int = 16000
    channels: int = 1
    audio_device_index: Optional[int] = (
        None  # None for default, or specific device index
    )

    # Web interface
    web_host: str = "localhost"
    web_port: int = 8000

    # Global hotkey
    hotkey: str = "f1"

    # Logging
    log_level: str = "INFO"


def load_config() -> Config:
    """Load configuration from environment variables."""
    return Config(
        model_size=os.getenv(
            "FASTER_WHISPER_MODEL_SIZE", "small"
        ),  # Default to "small" for speed
        device=os.getenv("FASTER_WHISPER_DEVICE", "cpu"),
        compute_type=os.getenv(
            "FASTER_WHISPER_COMPUTE_TYPE", "int8"
        ),  # Default to "int8" for CPU
        sample_rate=int(os.getenv("AUDIO_SAMPLE_RATE", "16000")),
        channels=int(os.getenv("AUDIO_CHANNELS", "1")),
        audio_device_index=(
            int(os.getenv("AUDIO_DEVICE_INDEX"))
            if os.getenv("AUDIO_DEVICE_INDEX")
            else None
        ),
        web_host=os.getenv("WEB_HOST", "localhost"),
        web_port=int(os.getenv("WEB_PORT", "8000")),
        hotkey=os.getenv("HOTKEY", "f1"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )


# Global config instance
config = load_config()
