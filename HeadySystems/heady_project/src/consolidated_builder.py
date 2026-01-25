#!/usr/bin/env python3
import os, sys, json, hashlib, datetime
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from heady_archive import HeadyArchive
    class VerticalTemplate:
        @staticmethod
        def get_config(v): return {"protocol": v}
except ImportError:
    pass

CONFIG_FILE = 'projects.json'

def mint_coin(d):
    return "hc_v1_" + hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]

def execute_build():
    print("Starting Consolidated Build v12.3...")
    if not os.path.exists(CONFIG_FILE):
        print(f"Config {CONFIG_FILE} not found in {os.getcwd()}")
        return

    with open(CONFIG_FILE) as f: conf = json.load(f)
    ws = conf.get('workspace', './heady-fleet')
    if not os.path.exists(ws): os.makedirs(ws)

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

        if "trust_domain" in p: m["foundation_trust_domain"] = p["trust_domain"]
        if p.get("vertical") == "security": m["security_gateway"] = "Active"
        if p.get("vertical") == "finance": m["finance_ledger"] = "Triple-Entry"
        if p.get("vertical") == "symphony": m["society_module"] = "HeadySymphony"
        if p.get("vertical") == "home": m["hardware_control"] = "Local-Only"

        m["heady_coin_pow"] = mint_coin(m)
        m = archivist.preserve(m, context_tags=[slug, "v12.3"])

        with open(os.path.join(p_dir, "heady-manifest.json"), "w") as f:
            json.dump(m, f, indent=2)

    print("Build Complete")

if __name__ == "__main__":
    execute_build()
