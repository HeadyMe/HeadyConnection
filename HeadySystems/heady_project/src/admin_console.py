#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class AdminConsole:
    def __init__(self):
        self.builder = os.path.join(current_dir, "consolidated_builder.py")
        self.api = os.path.join(current_dir, "api_server.py")
    def run_builder(self):
        subprocess.run([sys.executable, self.builder], check=True)
    def serve_api(self):
        subprocess.run([sys.executable, self.api], check=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--action")
    args, _ = p.parse_known_args()
    c = AdminConsole()
    if args.action == "builder_build": c.run_builder()
    elif args.action == "serve_api": c.serve_api()

if __name__ == "__main__": main()
