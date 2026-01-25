#!/usr/bin/env python3
import os
import json
import hashlib
import datetime
import tempfile
import shutil

class HeadyGoldenMasterBuilder:
    def __init__(self, config_path="../config/projects.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            # Fallback for relative paths depending on execution context
            alt_path = os.path.join("config", "projects.json")
            if os.path.exists(alt_path):
                self.config_path = alt_path
            elif os.path.exists("projects.json"):
                self.config_path = "projects.json"
            else:
                print(f"Warning: Config file not found at {self.config_path}")
                return {}
        
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def atomic_write(self, filepath, data):
        """Writes data to a temp file then renames it to ensure atomicity."""
        dir_name = os.path.dirname(filepath)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        fd, temp_path = tempfile.mkstemp(dir=dir_name, text=True)
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2)
        
        shutil.move(temp_path, filepath)
        print(f"Generated: {filepath}")

    def build(self):
        print("--- Starting Build ---")
        workspace = self.config.get("workspace", "./heady-fleet")
        projects = self.config.get("projects", [])

        if not os.path.exists(workspace):
            os.makedirs(workspace)

        for proj in projects:
            slug = proj.get("slug")
            if not slug:
                continue
            
            project_dir = os.path.join(workspace, slug)
            os.makedirs(project_dir, exist_ok=True)

            manifest = {
                "project": slug,
                "domain": proj.get("apex_domain"),
                "build_date": datetime.datetime.now().isoformat(),
                "configuration": proj
            }

            manifest_path = os.path.join(project_dir, "manifest.json")
            self.atomic_write(manifest_path, manifest)

        print("--- Build Complete ---")

if __name__ == "__main__":
    builder = HeadyGoldenMasterBuilder()
    builder.build()
