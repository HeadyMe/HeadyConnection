#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import datetime
import argparse

# Ensure we can import modules from the same directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from heady_archive import HeadyArchive
    # Mock other imports for stability if missing
    class VerticalTemplate:
        @staticmethod
        def get_config(v): return {"vertical": v}
    class DataVault:
        def __init__(self, j): pass
        def store_artifact(self, n, c): pass
    class TrustDomain:
        def __init__(self, n): pass
    class LegacyBridge:
        def __init__(self, d): pass
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

CONFIG_FILE = 'projects.json'
LOCK_FILE = 'projects.lock.json'

def calculate_file_hash(filepath):
    if not os.path.exists(filepath):
        return None
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_lockfile():
    print("Generating lockfile...")
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: {CONFIG_FILE} not found in {os.getcwd()}")
        # Try to find it
        if os.path.exists(os.path.join("heady_project", "config", CONFIG_FILE)):
             shutil.copy(os.path.join("heady_project", "config", CONFIG_FILE), CONFIG_FILE)
             print("Found and copied projects.json from config dir.")
        else:
             sys.exit(1)

    config_hash = calculate_file_hash(CONFIG_FILE)
    with open(CONFIG_FILE, 'r') as f:
        config_data = json.load(f)

    lock_data = {
        "_meta": {
            "generated_at": datetime.datetime.now().isoformat(),
            "source_config_hash": config_hash
        },
        "frozen_config": config_data
    }

    with open(LOCK_FILE, 'w') as f:
        json.dump(lock_data, f, indent=2)
    print(f"Lockfile {LOCK_FILE} created.")

def verify_integrity(bypass=False):
    if not os.path.exists(LOCK_FILE):
        if bypass:
            if os.path.exists(CONFIG_FILE):
                 with open(CONFIG_FILE, 'r') as f: return json.load(f)
            return {}
        else:
            print("Error: No lockfile found.")
            sys.exit(1)

    with open(LOCK_FILE, 'r') as f:
        lock_data = json.load(f)
    return lock_data['frozen_config']

def mint_heady_coin(manifest_data):
    return f"hc_v1_{hashlib.sha256(json.dumps(manifest_data, sort_keys=True).encode()).hexdigest()[:16]}"

def execute_build(config_data):
    print("Starting Build...")
    if not config_data or 'projects' not in config_data:
        print("Error: Invalid or empty configuration.")
        return

    workspace = config_data.get('workspace', './heady-fleet')
    if not os.path.exists(workspace): os.makedirs(workspace)
    print(f"Workspace: {workspace}")

    archivist = HeadyArchive()

    for proj in config_data.get('projects', []):
        slug = proj['slug']
        print(f"Provisioning {slug}...")
        project_path = os.path.join(workspace, slug)
        os.makedirs(project_path, exist_ok=True)

        manifest = {
            "project": slug,
            "domain": proj.get("apex_domain"),
            "built_at": datetime.datetime.now().isoformat(),
            "governance": "HeadySystems v12.1"
        }

        # Integrations
        if "trust_domain" in proj: manifest["foundation_trust_domain"] = proj["trust_domain"]
        if "vertical" in proj:
            if proj["vertical"] == "security": manifest["security_gateway"] = "Active"

        manifest["heady_coin_pow"] = mint_heady_coin(manifest)
        manifest = archivist.preserve(manifest, context_tags=[slug, "v12.1"])

        with open(os.path.join(project_path, 'heady-manifest.json'), 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"Created manifest for {slug}")

    print("Build Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--lock', action='store_true')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    if args.lock:
        generate_lockfile()
    else:
        config = verify_integrity(bypass=args.force)
        execute_build(config)
