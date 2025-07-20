"""
faster-whisper transcription engine.

Based on the SYSTRAN/faster-whisper repository example:
https://github.com/SYSTRAN/faster-whisper
"""

import logging
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

from faster_whisper import WhisperModel

from .exceptions import TranscriptionError, ModelLoadError

logger = logging.getLogger(__name__)


class FasterWhisperTranscriber:
    """Simple transcriber using faster-whisper, following their repo example."""
    
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8"
    ) -> None:
        """Initialize the transcriber.
        
        Args:
            model_size: Model size (tiny, base, small, medium, large, large-v3)
            device: Device to use ("cpu", "cuda", "auto")
            compute_type: Computation type ("int8", "float16", "float32")
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model: Optional[WhisperModel] = None
        
        logger.info(f"Initializing transcriber: {model_size} on {device}")
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the faster-whisper model."""
        try:
            # Exactly following faster-whisper repo example
            self.model = WhisperModel(
                self.model_size, 
                device=self.device, 
                compute_type=self.compute_type
            )
            logger.info(f"✅ Model loaded: {self.model_size}")
            
        except Exception as e:
            error_msg = f"Failed to load model '{self.model_size}': {e}"
            logger.error(error_msg)
            raise ModelLoadError(error_msg)
    
    def transcribe_file(self, audio_path: str, beam_size: int = 5) -> Dict[str, Any]:
        """Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            beam_size: Beam size for transcription
            
        Returns:
            Dictionary with transcription results
        """
        if not self.model:
            raise TranscriptionError("Model not loaded")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            logger.info(f"Transcribing: {audio_path}")
            
            # Following faster-whisper repo example exactly
            segments, info = self.model.transcribe(audio_path, beam_size=beam_size)
            
            # Extract language info (from their example)
            language = info.language
            language_probability = info.language_probability
            
            print(f"🔍 Debug - info type: {type(info)}")
            print(f"🔍 Debug - language type: {type(language)}, value: {repr(language)}")
            print(f"🔍 Debug - probability type: {type(language_probability)}, value: {repr(language_probability)}")
            
            logger.info(f"Detected language '{language}' with probability {language_probability:.2f}")
            
            # Collect all segments into full text
            segment_list = []
            full_text_parts = []
            
            for segment in segments:
                print(f"🔍 Debug - segment type: {type(segment)}")
                print(f"🔍 Debug - segment.text type: {type(segment.text)}, value: {repr(segment.text)}")
                
                segment_data = {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text
                }
                segment_list.append(segment_data)
                full_text_parts.append(segment.text)
                
                # Log each segment (like in their example)
                logger.debug(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
            
            full_text = " ".join(full_text_parts).strip()
            
            result = {
                "text": full_text,
                "language": language,
                "language_probability": language_probability,
                "segments": segment_list,
                "model": self.model_size
            }
            
            logger.info(f"Transcription completed: '{full_text[:100]}{'...' if len(full_text) > 100 else ''}'")
            return result
            
        except Exception as e:
            error_msg = f"Transcription failed: {e}"
            logger.error(error_msg)
            raise TranscriptionError(error_msg)
    
    def transcribe_audio_data(
        self, 
        audio_data: bytes, 
        sample_rate: int = 16000,
        beam_size: int = 5
    ) -> Dict[str, Any]:
        """Transcribe raw audio data.
        
        Args:
            audio_data: Raw audio bytes
            sample_rate: Audio sample rate
            beam_size: Beam size for transcription
            
        Returns:
            Dictionary with transcription results
        """
        import tempfile
        import wave
        
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Save audio data as WAV file
            with wave.open(temp_path, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
            
            # Transcribe the temporary file
            return self.transcribe_file(temp_path, beam_size)
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except OSError:
                pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "model_size": self.model_size,
            "device": self.device,
            "compute_type": self.compute_type,
            "is_loaded": self.model is not None
        }


# Simple test function following their example pattern
def test_transcriber():
    """Test the transcriber with a simple example."""
    try:
        # Initialize transcriber
        transcriber = FasterWhisperTranscriber("tiny")  # Use tiny for quick testing
        
        print("✅ Transcriber initialized successfully")
        print(f"Model info: {transcriber.get_model_info()}")
        
        # You would test with an actual audio file like:
        # result = transcriber.transcribe_file("test_audio.wav")
        # print(f"Transcription: {result['text']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Transcriber test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the transcriber
    test_transcriber()