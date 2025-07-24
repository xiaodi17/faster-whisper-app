#!/usr/bin/env python3
"""Build script for creating standalone executables with PyInstaller."""

import os
import platform
import subprocess
import sys
from pathlib import Path


def get_platform_name():
    """Get platform-specific name for the executable."""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    # Normalize architecture names
    if arch in ('x86_64', 'amd64'):
        arch = 'x64'
    elif arch in ('arm64', 'aarch64'):
        arch = 'arm64'
    elif arch in ('i386', 'i686'):
        arch = 'x86'
    
    return f"{system}-{arch}"


def build_executable():
    """Build the executable using PyInstaller."""
    print("🔨 Building Voice-to-Text executable...")
    
    # Get platform info
    platform_name = get_platform_name()
    print(f"📋 Platform: {platform_name}")
    
    # Define paths
    src_path = Path("src/faster_whisper_app/__main__.py")
    if not src_path.exists():
        print(f"❌ Source file not found: {src_path}")
        sys.exit(1)
    
    # Build executable name
    exe_name = f"Voice-to-Text-{platform_name}"
    if platform.system() == "Windows":
        exe_name += ".exe"
    
    print(f"📦 Building: {exe_name}")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single file
        "--windowed",                   # No console window
        "--name", exe_name,             # Executable name
        "--distpath", "dist",           # Output directory
        "--workpath", "build",          # Temp build directory
        "--specpath", ".",              # .spec file location
        "--clean",                      # Clean previous builds
        "--noconfirm",                  # Overwrite without asking
        str(src_path)                   # Source file
    ]
    
    try:
        print("⚙️  Running PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Check if executable was created
        exe_path = Path("dist") / exe_name
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / 1024 / 1024
            print(f"✅ Success! Built executable: {exe_path}")
            print(f"📏 File size: {size_mb:.1f} MB")
            print(f"🚀 Users can now run: ./{exe_name}")
        else:
            print("❌ Build completed but executable not found")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        sys.exit(1)


def clean_build():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    import shutil
    
    # Directories to clean
    clean_dirs = ["build", "dist", "__pycache__"]
    
    for dir_name in clean_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"🗑️  Removed: {dir_path}")
    
    # .spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"🗑️  Removed: {spec_file}")
    
    print("✅ Clean completed")


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_build()
    else:
        build_executable()


if __name__ == "__main__":
    main()