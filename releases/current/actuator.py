#!/usr/bin/env python3
import subprocess
import sys
import os

ITERATIONS = [
    "Heady_it1_v_1_0_0.py",
    "Heady_it2_v_1_0_0.py",
    "Heady_it3_v_1_0_0.py",
    "Heady_it4_v_1_0_0.py"
]

def run_iteration(script_name):
    if not os.path.exists(script_name):
        print(f"Error: {script_name} not found.")
        return False
        
    print(f"\n>>> Launching {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_name], check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {script_name}: {e}")
        return False

def main():
    print("=== Heady Actuator: Starting Multi-Stage Build ===")
    
    for script in ITERATIONS:
        if not run_iteration(script):
            print("Build pipeline stopped due to error.")
            sys.exit(1)
            
    print("\n=== Heady Actuator: All Iterations Complete ===")
    # Simulate Git Sync (Local only)
    if os.path.exists(".git"):
        print("Git repository detected. Staging changes...")
        subprocess.run(["git", "add", "."], check=False)
        subprocess.run(["git", "commit", "-m", "Actuator: Completed 4-stage build"], check=False)
        print("Changes committed locally.")
    else:
        print("No git repository found. Skipping sync.")

if __name__ == "__main__":
    main()
