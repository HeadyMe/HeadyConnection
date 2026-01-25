#!/usr/bin/env python3
import json
import os

def run():
    print("--- Executing Iteration 2: Operations ---")
    os.makedirs("heady_project/ops", exist_ok=True)
    ops_config = {
        "docker": True,
        "ci_cd": "github_actions",
        "monitoring": "uptime_kuma"
    }
    with open("heady_project/ops/ops_config.json", "w") as f:
        json.dump(ops_config, f, indent=2)
    print("Ops configuration created.")

if __name__ == "__main__":
    run()
