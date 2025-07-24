"""Command line interface for faster-whisper-app."""

import click
from rich.console import Console

from .config import load_config
from .__main__ import main as run_app

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Faster-Whisper Global Hotkey Speech-to-Text App
    
    A simple speech-to-text application that responds to F1 hotkey
    and outputs transcriptions to both terminal and browser.
    """
    pass


@cli.command()
@click.option('--model-size', default='base', 
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large', 'large-v3']),
              help='Whisper model size')
@click.option('--device', default='cpu',
              type=click.Choice(['cpu', 'cuda', 'auto']),
              help='Device to run model on')
@click.option('--compute-type', default='int8',
              type=click.Choice(['int8', 'float16', 'float32']),
              help='Compute precision type')
def run(model_size, device, compute_type):
    """Run the speech-to-text application with F1 hotkey."""
    console.print(f"🚀 Starting with model: {model_size} on {device}")
    
    # Override config with CLI options
    import os
    os.environ['FASTER_WHISPER_MODEL_SIZE'] = model_size
    os.environ['FASTER_WHISPER_DEVICE'] = device
    os.environ['FASTER_WHISPER_COMPUTE_TYPE'] = compute_type
    
    # Run the main app
    run_app()


@cli.command()
@click.argument('audio_file', type=click.Path(exists=True))
@click.option('--model-size', default='base',
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large', 'large-v3']),
              help='Whisper model size')
def transcribe(audio_file, model_size):
    """Transcribe an audio file directly."""
    from .core.transcriber import FasterWhisperTranscriber
    
    console.print(f"🎵 Transcribing: {audio_file}")
    console.print(f"🤖 Using model: {model_size}")
    
    try:
        transcriber = FasterWhisperTranscriber(model_size=model_size)
        result = transcriber.transcribe_file(audio_file)
        
        console.print("\n📝 Transcription Result:", style="bold green")
        console.print(f"Language: {result['language']} ({result['language_probability']:.1%})")
        console.print(f"Text: {result['text']}")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")


@cli.command()
def test():
    """Test the installation and components."""
    console.print("🧪 Testing faster-whisper-app installation...")
    
    # Test imports
    try:
        from .core.transcriber import FasterWhisperTranscriber
        from .core.recorder import AudioRecorder
        from .interfaces.hotkey_handler import AlternativeHotkeyHandler
        console.print("✅ All imports successful")
    except ImportError as e:
        console.print(f"❌ Import error: {e}", style="red")
        return
    
    # Test audio devices
    try:
        recorder = AudioRecorder()
        devices = recorder.list_audio_devices()
        console.print(f"✅ Found {len(devices)} audio devices")
        
        default_device = recorder.get_default_input_device()
        console.print(f"✅ Default device: {default_device['name']}")
        
        recorder.cleanup()
    except Exception as e:
        console.print(f"❌ Audio test failed: {e}", style="red")
    
    # Test model loading (with tiny model for speed)
    try:
        console.print("🤖 Testing model loading (this may take a moment)...")
        transcriber = FasterWhisperTranscriber(model_size="tiny")
        model_info = transcriber.get_model_info()
        console.print(f"✅ Model loaded: {model_info}")
    except Exception as e:
        console.print(f"❌ Model test failed: {e}", style="red")
    
    console.print("\n🎉 All tests completed!")


@cli.command()
def config():
    """Show current configuration."""
    cfg = load_config()
    
    console.print("⚙️ Current Configuration:", style="bold blue")
    console.print(f"Model Size: {cfg.model_size}")
    console.print(f"Device: {cfg.device}")
    console.print(f"Compute Type: {cfg.compute_type}")
    console.print(f"Sample Rate: {cfg.sample_rate} Hz")
    console.print(f"Channels: {cfg.channels}")
    console.print(f"Hotkey: {cfg.hotkey}")
    console.print(f"Web Port: {cfg.web_port}")
    console.print(f"Log Level: {cfg.log_level}")


if __name__ == '__main__':
    cli()