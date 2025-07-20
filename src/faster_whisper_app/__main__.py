"""Main entry point for faster-whisper-app."""

import logging
import sys
import signal
from typing import Optional

from .core.transcriber import FasterWhisperTranscriber
from .core.recorder import AudioRecorder
from .core.exceptions import TranscriptionError, AudioRecordingError, ModelLoadError
from .interfaces.hotkey_handler import AlternativeHotkeyHandler
from .interfaces.terminal_interface import TerminalInterface
from .config import load_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SpeechToTextApp:
    """Main application class combining all components."""
    
    def __init__(self):
        """Initialize the application."""
        self.config = load_config()
        self.terminal = TerminalInterface()
        self.transcriber: Optional[FasterWhisperTranscriber] = None
        self.recorder: Optional[AudioRecorder] = None
        self.hotkey_handler: Optional[AlternativeHotkeyHandler] = None
        self.is_recording = False
        self.is_running = False
        
        logger.info("Speech-to-text app initialized")
    
    def initialize_components(self) -> bool:
        """Initialize all app components.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.terminal.show_status("Initializing components...")
            
            # Initialize transcriber
            self.terminal.show_status("Loading speech recognition model...")
            self.transcriber = FasterWhisperTranscriber(
                model_size=self.config.model_size,
                device=self.config.device,
                compute_type=self.config.compute_type
            )
            
            # Show model info
            model_info = self.transcriber.get_model_info()
            self.terminal.show_model_info(model_info)
            
            # Initialize audio recorder
            self.terminal.show_status("Setting up audio recorder...")
            self.recorder = AudioRecorder(
                sample_rate=self.config.sample_rate,
                channels=self.config.channels
            )
            
            # Show device info
            try:
                if self.config.audio_device_index is not None:
                    # Show configured device - need to initialize PyAudio first
                    devices = self.recorder.list_audio_devices()
                    configured_device = None
                    for device in devices:
                        if device['index'] == self.config.audio_device_index:
                            configured_device = device
                            break
                    
                    if configured_device:
                        self.terminal.show_device_info(configured_device)
                        print(f"🎤 Configured to use device {self.config.audio_device_index}: {configured_device['name']}")
                    else:
                        self.terminal.show_error(f"Configured device {self.config.audio_device_index} not found!")
                        device_info = self.recorder.get_default_input_device()
                        self.terminal.show_device_info(device_info)
                else:
                    # Show default device
                    device_info = self.recorder.get_default_input_device()
                    self.terminal.show_device_info(device_info)
                    print(f"🎤 Using default device: {device_info['name']}")
            except Exception as e:
                self.terminal.show_error(f"Audio device warning: {e}")
            
            # Initialize hotkey handler with F1 (simpler key, less permission issues)
            self.hotkey_handler = AlternativeHotkeyHandler(
                callback=self.toggle_recording,
                hotkey="f1"
            )
            
            self.terminal.show_status("✅ All components initialized successfully!", "green")
            return True
            
        except ModelLoadError as e:
            self.terminal.show_error(f"Failed to load model: {e}")
            return False
        except Exception as e:
            self.terminal.show_error(f"Initialization failed: {e}")
            return False
    
    def toggle_recording(self) -> None:
        """Toggle recording state (start/stop)."""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self) -> None:
        """Start audio recording."""
        if self.is_recording:
            return
        
        if not self.recorder:
            self.terminal.show_error("Audio recorder not initialized")
            return
        
        try:
            self.terminal.show_recording_start()
            success = self.recorder.start_recording(device_index=self.config.audio_device_index)
            
            if success:
                self.is_recording = True
            else:
                self.terminal.show_error("Failed to start recording")
                
        except AudioRecordingError as e:
            self.terminal.show_error(f"Recording failed: {e}")
    
    def stop_recording(self) -> None:
        """Stop recording and transcribe."""
        if not self.is_recording:
            return
        
        if not self.recorder or not self.transcriber:
            self.terminal.show_error("Components not initialized")
            return
        
        try:
            self.terminal.show_recording_stop()
            audio_data = self.recorder.stop_recording()
            self.is_recording = False
            
            if audio_data:
                # Show processing message
                self.terminal.show_status("🤖 Processing audio...", "yellow")
                
                result = self.transcriber.transcribe_audio_data(
                    audio_data,
                    sample_rate=self.config.sample_rate
                )
                
                # Show result
                self.terminal.show_transcription_result(result)
                
            else:
                self.terminal.show_error("No audio data captured")
                
        except TranscriptionError as e:
            self.terminal.show_error(f"Transcription failed: {e}")
        except Exception as e:
            self.terminal.show_error(f"Processing failed: {e}")
        
        # Show ready message
        self.terminal.show_waiting_for_input()
    
    def run(self) -> None:
        """Run the main application."""
        try:
            # Show startup banner
            self.terminal.show_startup_banner()
            
            # Initialize components
            if not self.initialize_components():
                self.terminal.show_error("Failed to initialize. Exiting.")
                return
            
            # Setup signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # Start hotkey listener
            if self.hotkey_handler:
                self.hotkey_handler.start_listening()
                self.is_running = True
                
                self.terminal.show_waiting_for_input()
                
                # Keep running until interrupted
                try:
                    while self.is_running:
                        import time
                        time.sleep(0.1)
                except KeyboardInterrupt:
                    pass
            else:
                self.terminal.show_error("Failed to start hotkey listener")
                
        except Exception as e:
            self.terminal.show_error(f"Application error: {e}")
            logger.exception("Application error")
        finally:
            self.shutdown()
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.terminal.show_status("\n🛑 Shutting down...")
        self.is_running = False
    
    def shutdown(self) -> None:
        """Clean up resources."""
        try:
            self.is_running = False
            
            # Stop recording if in progress
            if self.is_recording and self.recorder:
                self.recorder.stop_recording()
            
            # Stop hotkey listener
            if self.hotkey_handler:
                self.hotkey_handler.stop_listening()
            
            # Clean up recorder
            if self.recorder:
                self.recorder.cleanup()
            
            self.terminal.show_status("👋 Goodbye!", "cyan")
            
        except Exception as e:
            logger.error(f"Shutdown error: {e}")


def main():
    """Main entry point."""
    try:
        app = SpeechToTextApp()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()