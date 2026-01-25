#!/usr/bin/env python3
import subprocess
import sys
import os

def run_script(script_path):
    print(f"\n>>> Executing {script_path}...")
    try:
        # Ensure we run from the project root context if needed, 
        # but for simplicity, we assume this is run from root or we adjust paths.
        # If running from root, script is scripts/build.py
        cmd = [sys.executable, script_path]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
        sys.exit(1)

def main():
    print("=== HEADY GOLDEN MASTER ACTUATOR ===")
    
    # 1. Build
    run_script(os.path.join("scripts", "build.py"))
    
    # 2. Release
    run_script(os.path.join("scripts", "release.py"))
    
    print("\n=== ACTUATION COMPLETE ===")
    print("Please check DELIVERY_MANIFEST.md and the generated zip file.")

if __name__ == "__main__":
    main()
