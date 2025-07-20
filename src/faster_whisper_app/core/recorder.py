"""Audio recording utilities using PyAudio."""

import logging
import threading
import time
from typing import Optional, List

import pyaudio
import numpy as np

from .exceptions import AudioRecordingError, DeviceError

logger = logging.getLogger(__name__)


class AudioRecorder:
    """Simple audio recorder for speech-to-text."""
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        audio_format: int = pyaudio.paInt16
    ) -> None:
        """Initialize audio recorder.
        
        Args:
            sample_rate: Audio sample rate (16kHz optimal for Whisper)
            channels: Number of channels (1 = mono)
            chunk_size: Frames per buffer
            audio_format: Audio format (16-bit signed integer)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio_format = audio_format
        
        self.audio: Optional[pyaudio.PyAudio] = None
        self.stream: Optional[pyaudio.Stream] = None
        self.is_recording = False
        self.audio_frames: List[bytes] = []
        self.recording_thread: Optional[threading.Thread] = None
        
        logger.info(f"AudioRecorder initialized: {sample_rate}Hz, {channels}ch")
    
    def list_audio_devices(self) -> List[dict]:
        """List available audio input devices."""
        if not self.audio:
            self.audio = pyaudio.PyAudio()
        
        devices = []
        try:
            for i in range(self.audio.get_device_count()):
                device_info = self.audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:  # Input device
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels'],
                        'sample_rate': int(device_info['defaultSampleRate'])
                    })
        except Exception as e:
            logger.error(f"Error listing audio devices: {e}")
        
        return devices
    
    def get_default_input_device(self) -> dict:
        """Get default audio input device info."""
        if not self.audio:
            self.audio = pyaudio.PyAudio()
        
        try:
            device_info = self.audio.get_default_input_device_info()
            return {
                'index': device_info['index'],
                'name': device_info['name'],
                'channels': device_info['maxInputChannels'],
                'sample_rate': int(device_info['defaultSampleRate'])
            }
        except OSError as e:
            raise DeviceError(f"No default input device found: {e}")
    
    def start_recording(self, device_index: Optional[int] = None) -> bool:
        """Start audio recording.
        
        Args:
            device_index: Specific device to use (None for default)
            
        Returns:
            True if recording started successfully
        """
        if self.is_recording:
            logger.warning("Already recording")
            return False
        
        try:
            if not self.audio:
                self.audio = pyaudio.PyAudio()
            
            # Reset audio frames
            self.audio_frames.clear()
            
            # Validate device if specified
            if device_index is not None:
                device_info = self.audio.get_device_info_by_index(device_index)
                if device_info['maxInputChannels'] == 0:
                    raise DeviceError(f"Device {device_index} is not an input device")
                logger.info(f"Using device: {device_info['name']}")
            
            # Start recording in separate thread
            self.is_recording = True
            self.recording_thread = threading.Thread(
                target=self._recording_worker,
                args=(device_index,),
                daemon=True
            )
            self.recording_thread.start()
            
            logger.info("🎙️ Recording started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self.is_recording = False
            raise AudioRecordingError(f"Failed to start recording: {e}")
    
    def stop_recording(self) -> Optional[bytes]:
        """Stop recording and return audio data.
        
        Returns:
            Audio data as bytes, or None if no recording
        """
        if not self.is_recording:
            logger.warning("Not currently recording")
            return None
        
        # Stop recording
        self.is_recording = False
        
        # Wait for recording thread to finish
        if self.recording_thread:
            self.recording_thread.join(timeout=2.0)
        
        # Combine audio frames
        if self.audio_frames:
            audio_data = b''.join(self.audio_frames)
            logger.info(f"⏹️ Recording stopped: {len(audio_data)} bytes")
            return audio_data
        
        return None
    
    def _recording_worker(self, device_index: Optional[int]) -> None:
        """Worker thread for audio recording."""
        try:
            # Open audio stream
            stream_params = {
                'format': self.audio_format,
                'channels': self.channels,
                'rate': self.sample_rate,
                'input': True,
                'frames_per_buffer': self.chunk_size
            }
            
            if device_index is not None:
                stream_params['input_device_index'] = device_index
            
            self.stream = self.audio.open(**stream_params)
            
            # Record audio chunks
            while self.is_recording:
                try:
                    chunk = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    self.audio_frames.append(chunk)
                except OSError as e:
                    logger.warning(f"Audio read error: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"Recording worker error: {e}")
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
    
    def get_audio_level(self, audio_chunk: bytes) -> float:
        """Get audio level for volume indication.
        
        Args:
            audio_chunk: Raw audio chunk
            
        Returns:
            Audio level from 0.0 to 1.0
        """
        try:
            if not audio_chunk:
                return 0.0
            
            # Convert to numpy array
            audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
            
            if len(audio_array) == 0:
                return 0.0
            
            # Calculate RMS level
            rms = np.sqrt(np.mean(audio_array.astype(np.float64) ** 2))
            
            # Normalize to 0-1 range
            level = min(rms / 10000.0, 1.0)
            return max(0.0, level)
            
        except Exception:
            return 0.0
    
    def cleanup(self) -> None:
        """Clean up audio resources."""
        if self.is_recording:
            self.stop_recording()
        
        if self.stream:
            self.stream.close()
        
        if self.audio:
            self.audio.terminate()
            self.audio = None
        
        logger.info("Audio recorder cleaned up")


def test_audio_recording():
    """Test audio recording functionality."""
    try:
        recorder = AudioRecorder()
        
        # List devices
        devices = recorder.list_audio_devices()
        print(f"📱 Found {len(devices)} audio input devices:")
        for device in devices[:3]:  # Show first 3
            print(f"  {device['index']}: {device['name']}")
        
        # Test default device
        default_device = recorder.get_default_input_device()
        print(f"🎤 Default device: {default_device['name']}")
        
        print("✅ Audio recording test passed")
        
        recorder.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Audio recording test failed: {e}")
        return False


if __name__ == "__main__":
    test_audio_recording()