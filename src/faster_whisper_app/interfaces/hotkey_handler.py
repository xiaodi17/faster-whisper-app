"""Global hotkey handler with double Ctrl click detection."""

import logging
import time
import threading
from typing import Callable, Optional

import keyboard

logger = logging.getLogger(__name__)


class DoubleCtrlHotkeyHandler:
    """Handles double Ctrl click for global speech-to-text activation."""
    
    def __init__(self, callback: Callable[[], None], timeout: float = 0.5):
        """Initialize the hotkey handler.
        
        Args:
            callback: Function to call on double Ctrl click
            timeout: Maximum time between clicks to register as double click (seconds)
        """
        self.callback = callback
        self.timeout = timeout
        self.last_ctrl_time: Optional[float] = None
        self.is_listening = False
        self.listener_thread: Optional[threading.Thread] = None
        
        logger.info(f"Double Ctrl hotkey handler initialized (timeout: {timeout}s)")
    
    def start_listening(self) -> None:
        """Start listening for double Ctrl clicks."""
        if self.is_listening:
            logger.warning("Already listening for hotkeys")
            return
        
        try:
            self.is_listening = True
            
            # Register Ctrl key press event
            keyboard.on_press_key('ctrl', self._on_ctrl_press)
            
            logger.info("🎹 Started listening for double Ctrl clicks")
            print("🎹 Double-tap Ctrl to start/stop recording")
            
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
            
            # Unhook the Ctrl key
            keyboard.unhook_all()
            
            logger.info("⏹️ Stopped listening for hotkeys")
            
        except Exception as e:
            logger.error(f"Error stopping hotkey listener: {e}")
    
    def _on_ctrl_press(self, event) -> None:
        """Handle Ctrl key press events."""
        if not self.is_listening:
            return
        
        current_time = time.time()
        
        if self.last_ctrl_time is None:
            # First Ctrl press
            self.last_ctrl_time = current_time
            print("🎹 First Ctrl press detected")
            logger.debug("First Ctrl press detected")
        else:
            # Check if this is within the timeout window
            time_diff = current_time - self.last_ctrl_time
            
            if time_diff <= self.timeout:
                # Double click detected!
                logger.info("🎯 Double Ctrl click detected!")
                self.last_ctrl_time = None  # Reset for next double click
                
                # Call the callback in a separate thread to avoid blocking
                threading.Thread(target=self._safe_callback, daemon=True).start()
            else:
                # Too slow, reset
                self.last_ctrl_time = current_time
                print(f"🎹 Ctrl press too slow ({time_diff:.2f}s), resetting")
                logger.debug("Ctrl press too slow, resetting")
    
    def _safe_callback(self) -> None:
        """Safely execute the callback with error handling."""
        try:
            self.callback()
        except Exception as e:
            logger.error(f"Error in hotkey callback: {e}")


class AlternativeHotkeyHandler:
    """Alternative hotkey handler using traditional key combinations."""
    
    def __init__(self, callback: Callable[[], None], hotkey: str = "ctrl+shift+space"):
        """Initialize with a traditional hotkey combination.
        
        Args:
            callback: Function to call when hotkey is pressed
            hotkey: Hotkey combination (e.g., "ctrl+shift+space")
        """
        self.callback = callback
        self.hotkey = hotkey
        self.is_listening = False
        
        logger.info(f"Alternative hotkey handler initialized: {hotkey}")
    
    def start_listening(self) -> None:
        """Start listening for the hotkey."""
        if self.is_listening:
            logger.warning("Already listening for hotkeys")
            return
        
        try:
            self.is_listening = True
            
            # Register the hotkey
            keyboard.add_hotkey(self.hotkey, self._safe_callback)
            
            logger.info(f"🎹 Started listening for {self.hotkey}")
            print(f"🎹 Press {self.hotkey} to start/stop recording")
            
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


def test_double_ctrl_hotkey():
    """Test the double Ctrl hotkey handler."""
    def test_callback():
        print("🎉 Double Ctrl detected! This would start/stop recording.")
    
    try:
        handler = DoubleCtrlHotkeyHandler(test_callback, timeout=0.5)
        handler.start_listening()
        
        print("Testing double Ctrl hotkey...")
        print("Try double-tapping the Ctrl key quickly")
        print("Press Ctrl+C to exit")
        
        # Keep the test running
        keyboard.wait('ctrl+c')
        
        handler.stop_listening()
        print("✅ Hotkey test completed")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    except Exception as e:
        print(f"❌ Hotkey test failed: {e}")


def test_alternative_hotkey():
    """Test the alternative hotkey handler."""
    def test_callback():
        print("🎉 Hotkey detected! This would start/stop recording.")
    
    try:
        handler = AlternativeHotkeyHandler(test_callback, "ctrl+shift+space")
        handler.start_listening()
        
        print("Testing alternative hotkey...")
        print("Try pressing Ctrl+Shift+Space")
        print("Press Ctrl+C to exit")
        
        # Keep the test running
        keyboard.wait('ctrl+c')
        
        handler.stop_listening()
        print("✅ Alternative hotkey test completed")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    except Exception as e:
        print(f"❌ Alternative hotkey test failed: {e}")


if __name__ == "__main__":
    print("Choose hotkey test:")
    print("1. Double Ctrl click")
    print("2. Traditional hotkey (Ctrl+Shift+Space)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_double_ctrl_hotkey()
    elif choice == "2":
        test_alternative_hotkey()
    else:
        print("❌ Invalid choice")