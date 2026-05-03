import subprocess
import os

def test_ffmpeg():
    print("Testing FFmpeg...")
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        print(f"FFmpeg found: {result.stdout.splitlines()[0]}")
    except FileNotFoundError:
        print("❌ FFmpeg NOT FOUND in PATH.")
    except Exception as e:
        print(f"❌ FFmpeg error: {e}")

if __name__ == "__main__":
    test_ffmpeg()
