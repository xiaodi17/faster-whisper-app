"""Main entry point for faster-whisper-app."""

import logging
import sys
import signal
import asyncio
import threading
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
            
            # Initialize hotkey handler with configurable hotkey from .env
            self.hotkey_handler = AlternativeHotkeyHandler(
                callback=self.toggle_recording,
                hotkey=self.config.hotkey
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
            import time
            processing_start = time.time()
            logger.info("🚀 Starting complete processing pipeline")
            
            self.terminal.show_recording_stop()
            
            # Time audio data retrieval
            audio_start = time.time()
            audio_data = self.recorder.stop_recording()
            audio_time = time.time() - audio_start
            logger.info(f"⚡ Audio data retrieval: {audio_time*1000:.1f}ms")
            
            self.is_recording = False
            
            if audio_data:
                # Show processing message
                self.terminal.show_status("🤖 Processing audio...", "yellow")
                
                # Time transcription
                transcription_start = time.time()
                result = self.transcriber.transcribe_audio_data(
                    audio_data,
                    sample_rate=self.config.sample_rate,
                    beam_size=1  # Use beam_size=1 for fastest transcription
                )
                transcription_time = time.time() - transcription_start
                
                # Time result display
                display_start = time.time()
                self.terminal.show_transcription_result(result)
                display_time = time.time() - display_start
                logger.info(f"⚡ Result display: {display_time*1000:.1f}ms")
                
                # Start text output asynchronously (timing logged in the async method)
                threading.Thread(
                    target=self._type_to_active_app_async,
                    args=(result,),
                    daemon=True
                ).start()
                
                # Log overall timing
                total_processing_time = time.time() - processing_start
                logger.info(f"🏁 Total processing pipeline: {total_processing_time*1000:.1f}ms")
                logger.info(f"📊 Breakdown - Audio: {audio_time*1000:.1f}ms, Transcription: {transcription_time*1000:.1f}ms, Display: {display_time*1000:.1f}ms")
                
                # Add timing info to terminal if available
                if 'timing' in result:
                    timing = result['timing']
                    logger.info(f"🔍 Transcription breakdown - WAV prep: {timing['wav_prep_time']*1000:.1f}ms, Model: {timing['model_time']*1000:.1f}ms, Segments: {timing['segment_time']*1000:.1f}ms")
                
            else:
                logger.warning("❌ No audio data captured")
                self.terminal.show_error("No audio data captured")
                
        except TranscriptionError as e:
            self.terminal.show_error(f"Transcription failed: {e}")
        except Exception as e:
            self.terminal.show_error(f"Processing failed: {e}")
        
        # Show ready message
        self.terminal.show_waiting_for_input(hotkey=self.config.hotkey)
    
    def _type_to_active_app_async(self, result: dict):
        """Type the transcribed text into the currently active text field asynchronously."""
        import subprocess
        import time
        
        text = result.get('text', '').strip()
        if not text:
            return
        
        try:
            typing_start = time.time()
            logger.info(f"⌨️  Starting text output: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            
            # Small delay to ensure the app is ready
            prep_start = time.time()
            time.sleep(0.05)  # Reduced delay
            
            # Escape special characters for AppleScript
            escaped_text = text.replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            prep_time = time.time() - prep_start
            
            # Use AppleScript to type the text into the active application
            applescript = f'''
            tell application "System Events"
                keystroke "{escaped_text}"
            end tell
            '''
            
            # Execute the AppleScript asynchronously
            script_start = time.time()
            subprocess.run(
                ['osascript', '-e', applescript], 
                check=True,
                timeout=2.0,  # Prevent hanging
                capture_output=True
            )
            script_time = time.time() - script_start
            total_typing_time = time.time() - typing_start
            
            logger.info(f"⚡ Text output timing - Prep: {prep_time*1000:.1f}ms, Script: {script_time*1000:.1f}ms, Total: {total_typing_time*1000:.1f}ms")
            logger.info(f"✅ Successfully typed to active app")
            
        except subprocess.TimeoutExpired:
            total_time = time.time() - typing_start
            logger.warning(f"⚠️  AppleScript execution timed out after {total_time*1000:.1f}ms")
        except Exception as e:
            total_time = time.time() - typing_start
            logger.error(f"❌ Text output failed after {total_time*1000:.1f}ms: {e}")
    
    def _type_to_active_app(self, result: dict):
        """Legacy sync method - kept for compatibility."""
        self._type_to_active_app_async(result)
    
    def run(self) -> None:
        """Run the main application."""
        try:
            # Show startup banner with configured hotkey
            self.terminal.show_startup_banner(hotkey=self.config.hotkey)
            
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
                
                self.terminal.show_waiting_for_input(hotkey=self.config.hotkey)
                
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