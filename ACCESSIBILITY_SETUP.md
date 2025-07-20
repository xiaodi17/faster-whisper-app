# macOS Accessibility Setup for Global Hotkeys

## The Issue
The app needs accessibility permissions to detect the Ctrl+Shift+Space hotkey globally. Without these permissions, the hotkey won't work.

## Solution: Grant Accessibility Permissions

### Step 1: Open System Preferences
1. Click the Apple menu → System Preferences (or System Settings on newer macOS)
2. Go to "Security & Privacy" → "Privacy" tab
3. Find "Accessibility" in the left sidebar

### Step 2: Add Terminal
1. Click the lock icon to make changes (enter your password)
2. Click the "+" button to add an application
3. Navigate to Applications → Utilities → Terminal.app
4. Select Terminal and click "Open"
5. Make sure Terminal is checked in the list

### Alternative: Add Python/PyCharm/VSCode
If you're running the app from an IDE:
- For PyCharm: Add PyCharm to accessibility permissions
- For VSCode: Add Visual Studio Code to accessibility permissions  
- For direct Python: Add Python.app (usually in Applications/Python 3.x/)

### Step 3: Test the App
1. Restart Terminal (or your IDE)
2. Run the app again:
   ```bash
   source venv/bin/activate
   PYTHONPATH=src python -m faster_whisper_app
   ```
3. Try pressing Ctrl+Shift+Space

## Alternative Hotkeys
If accessibility permissions are problematic, we could switch to:
- Function key combinations (F1, F2, etc.)
- Menu bar app with click activation
- Touch Bar integration (on supported Macs)

## Verification
You should see:
```
🎹 Press ctrl+shift+space to start/stop recording
⏳ Ready - Press Ctrl+Shift+Space to start recording
```

When you press the hotkey, you should see:
```
🔧 Config audio_device_index: 2
🎤 Using device 2: C270 HD WEBCAM
🎙️ Recording...
```

## Security Note
Accessibility permissions are powerful - they allow apps to monitor all keyboard input. Only grant these to applications you trust.