#!/usr/bin/env python3
import json
import os

def run():
    print("--- Executing Iteration 1: Foundation ---")
    os.makedirs("heady_project/config", exist_ok=True)
    config = {
        "version": "1.0.0",
        "stage": "foundation",
        "components": ["fs_structure", "basic_config"]
    }
    with open("heady_project/config/it1_manifest.json", "w") as f:
        json.dump(config, f, indent=2)
    print("Foundation manifest created.")

if __name__ == "__main__":
    run()
