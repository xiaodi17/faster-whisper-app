#!/usr/bin/env python3
"""Simple hotkey test to debug the issue."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_hotkey():
    """Test different hotkey combinations."""
    try:
        import keyboard
        
        print("Testing different hotkey combinations...")
        print("This will help identify which keys work on macOS")
        
        def callback1():
            print("✅ ctrl+shift+space detected!")
        
        def callback2():
            print("✅ ctrl+space detected!")
            
        def callback3():
            print("✅ shift+space detected!")
            
        def callback4():
            print("✅ F1 detected!")
        
        # Test multiple combinations
        keyboard.add_hotkey('ctrl+shift+space', callback1)
        keyboard.add_hotkey('ctrl+space', callback2) 
        keyboard.add_hotkey('shift+space', callback3)
        keyboard.add_hotkey('f1', callback4)
        
        print("Hotkeys registered:")
        print("- Ctrl+Shift+Space")
        print("- Ctrl+Space") 
        print("- Shift+Space")
        print("- F1")
        print("\nTry pressing any of these combinations...")
        print("Press Ctrl+C to exit")
        
        # Keep running
        keyboard.wait('ctrl+c')
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if "Error 13" in str(e):
            print("\n🔧 SOLUTION:")
            print("1. Open System Preferences → Security & Privacy → Privacy")
            print("2. Select 'Accessibility' from the left sidebar")
            print("3. Click the lock icon and enter your password")
            print("4. Click '+' and add Terminal.app")
            print("5. Make sure Terminal is checked ✓")
            print("6. Restart Terminal and try again")

if __name__ == "__main__":
    test_hotkey()