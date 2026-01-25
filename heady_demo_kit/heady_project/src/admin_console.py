#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class AdminConsole:
    def __init__(self):
        self.builder = os.path.join(current_dir, "consolidated_builder.py")
        self.api = os.path.join(current_dir, "api_server.py")
        self.fleet = os.path.join(os.getcwd(), "heady-fleet")

    def run_build(self):
        print(f"Executing Builder: {self.builder}")
        subprocess.run([sys.executable, self.builder], check=True)  # nosec

    def serve_api(self):
        print(f"Launching API: {self.api}")
        subprocess.run([sys.executable, self.api], check=True)  # nosec

    def run_audit(self):
        print("--- Starting Audit ---")
        targets = {"auth-service": "Identity_Root", "guardian-gateway": "Active"}
        for s, v in targets.items():
            p = os.path.join(self.fleet, s, "heady-manifest.json")
            if not os.path.exists(p):
                print(f"\u274c Missing {s}")
                sys.exit(1)
            print(f"\u2705 Verified {s}")
        print("\u2728 Audit Passed")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--action')
    a = p.parse_args()
    c = AdminConsole()
    if a.action == 'builder_build':
        c.run_build()
    elif a.action == 'full_audit':
        c.run_audit()
    elif a.action == 'serve_api':
        c.serve_api()

if __name__ == '__main__':
    main()
