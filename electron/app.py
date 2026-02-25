import subprocess
import sys
import os

def start_controller():
    try:
        subprocess.Popen([sys.executable, "-m", "gestures.controller"])
        print("✅ Gesture controller started")
    except Exception as e:
        print(f"❌ Failed to start controller: {e}")

if __name__ == "__main__":
    start_controller()