"""Global hotkey handler for configurable key combinations."""

import logging
from typing import Callable

import keyboard

logger = logging.getLogger(__name__)


class HotkeyHandler:
    """Simple hotkey handler using configurable key combinations."""

    def __init__(self, callback: Callable[[], None], hotkey: str = "f1"):
        """Initialize with a hotkey combination.

        Args:
            callback: Function to call when hotkey is pressed
            hotkey: Hotkey combination (e.g., "f1", "ctrl+shift+space")
        """
        self.callback = callback
        self.hotkey = hotkey
        self.is_listening = False

        logger.info(f"Hotkey handler initialized: {hotkey}")

    def start_listening(self) -> None:
        """Start listening for the hotkey."""
        if self.is_listening:
            logger.warning("Already listening for hotkeys")
            return

        try:
            self.is_listening = True
            keyboard.add_hotkey(self.hotkey, self._safe_callback)
            logger.info(f"🎹 Started listening for {self.hotkey}")

        except Exception as e:
            logger.error(f"Failed to start hotkey listening: {e}")
            self.is_listening = False
            raise

    def stop_listening(self) -> None:
        """Stop listening for hotkeys."""
        if not self.is_listening:
            return

        try:
            self.is_listening = False
            keyboard.unhook_all()
            logger.info("⏹️ Stopped listening for hotkeys")

        except Exception as e:
            logger.error(f"Error stopping hotkey listener: {e}")

    def _safe_callback(self) -> None:
        """Safely execute the callback with error handling."""
        try:
            self.callback()
        except Exception as e:
            logger.error(f"Error in hotkey callback: {e}")


# Backward compatibility alias
AlternativeHotkeyHandler = HotkeyHandler


def test_hotkey(hotkey: str = "f1"):
    """Test the hotkey handler."""

    def test_callback():
        print(f"🎉 {hotkey.upper()} detected! This would start/stop recording.")

    try:
        handler = HotkeyHandler(test_callback, hotkey)
        handler.start_listening()

        print(f"Testing hotkey: {hotkey}")
        print(f"Try pressing {hotkey.upper()}")
        print("Press Ctrl+C to exit")

        # Keep the test running
        keyboard.wait("ctrl+c")

        handler.stop_listening()
        print("✅ Hotkey test completed")

    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    except Exception as e:
        print(f"❌ Hotkey test failed: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Test specific hotkey from command line
        test_hotkey(sys.argv[1])
    else:
        # Default test
        test_hotkey("f1")
