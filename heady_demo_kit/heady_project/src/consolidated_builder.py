#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import modules with Mypy safeguards
try:
    from heady_archive import HeadyArchive
    from heady_verticals import VerticalTemplate
    from heady_foundation import DataVault, TrustDomain, LegacyBridge
    from heady_security import AISafetyGateway, RAAFabric
    from heady_hardware import HeadyHome, HeadyBare
    from heady_society import HeadySymphony
    from heady_finance import HeadyFinance
    from compute_throttle import HeadyComputeThrottle, UserRequest, TaskIntent
    from heady_reflect import HeadyReflect
except ImportError:
    # Fallback mocks for standalone execution
    class HeadyArchive:  # type: ignore
        def preserve(self, m, context_tags=None):
            return m

    class VerticalTemplate:  # type: ignore
        @staticmethod
        def get_config(v):
            return {}

    class DataVault:  # type: ignore
        def __init__(self, j):
            pass

        def store_artifact(self, n, c):
            pass

    class TrustDomain:  # type: ignore
        def __init__(self, n):
            pass

    class LegacyBridge:  # type: ignore
        def __init__(self, d):
            pass

    class AISafetyGateway:  # type: ignore
        pass

    class RAAFabric:  # type: ignore
        pass

    class HeadyHome:  # type: ignore
        pass

    class HeadyBare:  # type: ignore
        pass

    class HeadySymphony:  # type: ignore
        pass

    class HeadyFinance:  # type: ignore
        pass

    class HeadyComputeThrottle:  # type: ignore
        def calculate_allocation(self, r):
            return {"cpu": 4, "ram": 16}

    class UserRequest:  # type: ignore
        def __init__(self, u, i, s=False):
            pass

    class TaskIntent:  # type: ignore
        RENDER_BATCH = "rb"

CONFIG_FILE_NAME = 'projects.json'

def mint_coin(d):
    return "hc_v1_" + hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]

def get_config_path():
    # Check CWD
    if os.path.exists(CONFIG_FILE_NAME):
        return CONFIG_FILE_NAME
    # Check relative to script
    rel_path = os.path.join(current_dir, '..', 'config', CONFIG_FILE_NAME)
    if os.path.exists(rel_path):
        return rel_path
    return None

def execute_build():
    print("Starting Consolidated Build v12.3...")
    config_path = get_config_path()
    if not config_path:
        print(f"Config {CONFIG_FILE_NAME} not found in {os.getcwd()} or relative paths")
        return

    with open(config_path) as f:
        conf = json.load(f)
    ws = conf.get('workspace', './heady-fleet')
    if not os.path.exists(ws):
        os.makedirs(ws)

    archivist = HeadyArchive()

    for p in conf.get('projects', []):
        slug = p['slug']
        p_dir = os.path.join(ws, slug)
        os.makedirs(p_dir, exist_ok=True)
        m = {
            "project": slug,
            "domain": p.get("apex_domain"),
            "gov": "Heady v12.3"
        }

        if "trust_domain" in p:
            m["foundation_trust_domain"] = p["trust_domain"]
        if p.get("vertical") == "security":
            m["security_gateway"] = "Active"
        if p.get("vertical") == "finance":
            m["finance_ledger"] = "Triple-Entry"
        if p.get("vertical") == "symphony":
            m["society_module"] = "HeadySymphony"
        if p.get("vertical") == "home":
            m["hardware_control"] = "Local-Only"

        m["heady_coin_pow"] = mint_coin(m)
        m = archivist.preserve(m, context_tags=[slug, "v12.3"])

        with open(os.path.join(p_dir, "heady-manifest.json"), "w") as f:
            json.dump(m, f, indent=2)

    print("Build Complete")

if __name__ == "__main__":
    execute_build()
