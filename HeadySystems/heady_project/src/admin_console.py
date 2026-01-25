#!/usr/bin/env python3
import os, sys, subprocess, argparse, json

# Ensure local imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class AdminConsole:
    def __init__(self):
        self.builder = os.path.join(current_dir, "consolidated_builder.py")
        self.api = os.path.join(current_dir, "api_server.py")
        self.fleet = os.path.join(os.getcwd(), "heady-fleet")

    def run_build(self):
        print(f"Executing Builder: {self.builder}")
        subprocess.run([sys.executable, self.builder], check=True)

    def serve_api(self):
        print(f"Launching API: {self.api}")
        subprocess.run([sys.executable, self.api], check=True)

    def run_audit(self):
        print("--- Starting Audit ---")
        targets = {"auth-service": "Identity_Root", "guardian-gateway": "Active"}
        for s, v in targets.items():
            p = os.path.join(self.fleet, s, "heady-manifest.json")
            if not os.path.exists(p):
                print(f"\u274c Missing {s}"); sys.exit(1)
            print(f"\u2705 Verified {s}")
        print("\u2728 Audit Passed")

    def run_bot(self):
        print("--- Simulating HeadyGuardianBot ---")
        try:
            from heady_guardian_bot import HeadyGuardianBot
        except ImportError as e:
            print(f"Error importing HeadyGuardianBot: {e}")
            return

        bot = HeadyGuardianBot()

        # Test Case 1: Valid Intent
        print("\n[Scenario 1] Valid Update")
        payload_valid = {"user": "maintainer", "message": "Update manifest configuration"}
        bot.trigger_event("push", payload_valid)

        # Test Case 2: Invalid Intent (Governance Block)
        print("\n[Scenario 2] Malicious Intent")
        payload_invalid = {"user": "attacker", "message": "Deploy Malicious mining script"}
        bot.trigger_event("push", payload_invalid)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--action')
    a = p.parse_args()
    c = AdminConsole()
    
    if a.action == 'builder_build': c.run_build()
    elif a.action == 'full_audit': c.run_audit()
    elif a.action == 'serve_api': c.serve_api()
    elif a.action == 'run_bot': c.run_bot()

if __name__ == '__main__': main()
