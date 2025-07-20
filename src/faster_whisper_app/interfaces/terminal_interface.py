"""Terminal interface with Rich formatting for speech-to-text output."""

import logging
import time
from typing import Dict, Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

logger = logging.getLogger(__name__)


class TerminalInterface:
    """Beautiful terminal interface for speech-to-text using Rich."""
    
    def __init__(self):
        """Initialize the terminal interface."""
        self.console = Console()
        self.is_recording = False
        self.transcription_count = 0
        
        logger.info("Terminal interface initialized")
    
    def show_startup_banner(self) -> None:
        """Display startup banner."""
        banner = Panel(
            Text.assemble(
                ("🎙️ ", "bold red"),
                ("Faster-Whisper Speech-to-Text", "bold blue"),
                (" 🎙️", "bold red")
            ),
            title="Welcome",
            border_style="cyan",
            box=box.ROUNDED
        )
        
        self.console.print()
        self.console.print(banner)
        
        # Show instructions
        instructions = Table(show_header=False, box=None, padding=(0, 1))
        instructions.add_column(style="cyan")
        instructions.add_column(style="white")
        
        instructions.add_row("🎹", "Double-tap Ctrl to start/stop recording")
        instructions.add_row("🔊", "Speak clearly into your microphone")
        instructions.add_row("⏹️", "Double-tap Ctrl again to transcribe")
        instructions.add_row("❌", "Ctrl+C to exit")
        
        self.console.print()
        self.console.print(Panel(instructions, title="Instructions", border_style="green"))
        self.console.print()
    
    def show_recording_start(self) -> None:
        """Show recording started message."""
        self.is_recording = True
        
        recording_panel = Panel(
            Text.assemble(
                ("🔴 ", "bold red"),
                ("RECORDING", "bold white on red"),
                (" 🔴", "bold red")
            ),
            border_style="red",
            box=box.HEAVY
        )
        
        self.console.print()
        self.console.print(recording_panel)
        self.console.print("💬 Speak now...", style="yellow")
    
    def show_recording_stop(self) -> None:
        """Show recording stopped message."""
        self.is_recording = False
        
        processing_panel = Panel(
            Text.assemble(
                ("🤖 ", "bold blue"),
                ("PROCESSING", "bold white on blue"),
                (" 🤖", "bold blue")
            ),
            border_style="blue",
            box=box.HEAVY
        )
        
        self.console.print()
        self.console.print(processing_panel)
    
    def show_processing_with_spinner(self) -> Live:
        """Show processing spinner and return Live context."""
        spinner_text = Text.assemble(
            ("🤖 ", "bold blue"),
            ("Transcribing audio", "white"),
            ("...", "dim white")
        )
        
        return Live(
            Panel(
                Text.assemble(
                    (Spinner("dots", style="blue"), ""),
                    (" ", ""),
                    spinner_text
                ),
                border_style="blue"
            ),
            console=self.console,
            refresh_per_second=4
        )
    
    def show_transcription_result(self, result: Dict[str, Any]) -> None:
        """Display transcription result with beautiful formatting.
        
        Args:
            result: Transcription result dictionary
        """
        self.transcription_count += 1
        
        # Extract result data
        text = result.get("text", "").strip()
        language = result.get("language", "unknown")
        confidence = result.get("language_probability", 0.0)
        model = result.get("model", "unknown")
        
        if not text:
            self.console.print("🔇 No speech detected", style="yellow")
            return
        
        # Create result table
        result_table = Table(show_header=False, box=None, padding=(0, 1))
        result_table.add_column("Label", style="cyan", width=12)
        result_table.add_column("Value", style="white")
        
        result_table.add_row("📝 Text:", text)
        result_table.add_row("🌍 Language:", f"{language} ({confidence:.1%})")
        result_table.add_row("🤖 Model:", model)
        result_table.add_row("⏱️ Time:", time.strftime("%H:%M:%S"))
        
        # Show result in a panel
        result_panel = Panel(
            result_table,
            title=f"Transcription #{self.transcription_count}",
            border_style="green",
            box=box.ROUNDED
        )
        
        self.console.print()
        self.console.print(result_panel)
        
        # Also show just the text prominently
        text_panel = Panel(
            Text(text, style="bold white"),
            title="📋 Transcribed Text",
            border_style="bright_green",
            box=box.DOUBLE
        )
        
        self.console.print()
        self.console.print(text_panel)
        self.console.print()
    
    def show_error(self, error: str) -> None:
        """Display error message.
        
        Args:
            error: Error message to display
        """
        error_panel = Panel(
            Text.assemble(
                ("❌ ", "bold red"),
                (error, "red")
            ),
            title="Error",
            border_style="red",
            box=box.HEAVY
        )
        
        self.console.print()
        self.console.print(error_panel)
        self.console.print()
    
    def show_status(self, message: str, style: str = "white") -> None:
        """Show a status message.
        
        Args:
            message: Status message
            style: Rich style for the message
        """
        self.console.print(f"ℹ️  {message}", style=style)
    
    def show_device_info(self, device_info: Dict[str, Any]) -> None:
        """Show audio device information.
        
        Args:
            device_info: Audio device information
        """
        device_table = Table(show_header=False, box=None, padding=(0, 1))
        device_table.add_column("Property", style="cyan", width=15)
        device_table.add_column("Value", style="white")
        
        device_table.add_row("🎤 Device:", device_info.get("name", "Unknown"))
        device_table.add_row("📊 Channels:", str(device_info.get("channels", "Unknown")))
        device_table.add_row("🔊 Sample Rate:", f"{device_info.get('sample_rate', 'Unknown')} Hz")
        
        device_panel = Panel(
            device_table,
            title="Audio Device",
            border_style="blue"
        )
        
        self.console.print(device_panel)
    
    def show_model_info(self, model_info: Dict[str, Any]) -> None:
        """Show model information.
        
        Args:
            model_info: Model information dictionary
        """
        model_table = Table(show_header=False, box=None, padding=(0, 1))
        model_table.add_column("Property", style="cyan", width=15)
        model_table.add_column("Value", style="white")
        
        model_table.add_row("🤖 Model:", model_info.get("model_size", "Unknown"))
        model_table.add_row("💻 Device:", model_info.get("device", "Unknown"))
        model_table.add_row("⚡ Compute:", model_info.get("compute_type", "Unknown"))
        model_table.add_row("✅ Loaded:", "Yes" if model_info.get("is_loaded") else "No")
        
        model_panel = Panel(
            model_table,
            title="Model Information",
            border_style="magenta"
        )
        
        self.console.print(model_panel)
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        self.console.clear()
    
    def show_waiting_for_input(self) -> None:
        """Show waiting for input message."""
        waiting_text = Text.assemble(
            ("⏳ ", "yellow"),
            ("Ready - Double-tap Ctrl to start recording", "white")
        )
        
        self.console.print(waiting_text)


def test_terminal_interface():
    """Test the terminal interface."""
    interface = TerminalInterface()
    
    # Show startup
    interface.show_startup_banner()
    
    # Show device info
    device_info = {
        "name": "Built-in Microphone",
        "channels": 1,
        "sample_rate": 16000
    }
    interface.show_device_info(device_info)
    
    # Show model info
    model_info = {
        "model_size": "base",
        "device": "cpu",
        "compute_type": "int8",
        "is_loaded": True
    }
    interface.show_model_info(model_info)
    
    print()
    input("Press Enter to test recording simulation...")
    
    # Simulate recording
    interface.show_recording_start()
    time.sleep(2)
    
    interface.show_recording_stop()
    
    # Show processing with spinner
    with interface.show_processing_with_spinner():
        time.sleep(3)
    
    # Show result
    result = {
        "text": "Hello, this is a test of the speech recognition system. It works great!",
        "language": "en",
        "language_probability": 0.95,
        "model": "base"
    }
    interface.show_transcription_result(result)
    
    # Show error
    interface.show_error("This is a test error message")
    
    print("✅ Terminal interface test completed!")


if __name__ == "__main__":
    test_terminal_interface()