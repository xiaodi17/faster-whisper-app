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
    
    # Model settings
    model_size: str = "base"
    device: str = "cpu"
    compute_type: str = "int8"
    
    # Audio settings
    sample_rate: int = 16000
    channels: int = 1
    
    # Web interface
    web_host: str = "localhost"
    web_port: int = 8000
    
    # Global hotkey
    hotkey: str = "ctrl+space"
    
    # Logging
    log_level: str = "INFO"


def load_config() -> Config:
    """Load configuration from environment variables."""
    return Config(
        model_size=os.getenv("FASTER_WHISPER_MODEL_SIZE", "base"),
        device=os.getenv("FASTER_WHISPER_DEVICE", "cpu"),
        compute_type=os.getenv("FASTER_WHISPER_COMPUTE_TYPE", "int8"),
        sample_rate=int(os.getenv("AUDIO_SAMPLE_RATE", "16000")),
        channels=int(os.getenv("AUDIO_CHANNELS", "1")),
        web_host=os.getenv("WEB_HOST", "localhost"),
        web_port=int(os.getenv("WEB_PORT", "8000")),
        hotkey=os.getenv("HOTKEY", "ctrl+space"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )


# Global config instance
config = load_config()