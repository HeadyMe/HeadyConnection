#!/usr/bin/env python3
import shutil
import zipfile
import hashlib
import os
import datetime

class ReleaseManager:
    def __init__(self, project_root=".", output_name="Heady_v13_Gold_Master"):
        self.project_root = project_root
        self.output_name = output_name
        self.zip_filename = f"{output_name}.zip"

    def create_archive(self):
        print(f"--- Creating Archive: {self.zip_filename} ---")
        # Exclude patterns
        exclude_dirs = {'__pycache__', '.git', '.config', 'sample_data'}
        exclude_exts = {'.pyc', '.zip'}

        with zipfile.ZipFile(self.zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.project_root):
                # Modify dirs in-place to skip exclusions
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                
                for file in files:
                    if any(file.endswith(ext) for ext in exclude_exts):
                        continue
                    
                    file_path = os.path.join(root, file)
                    # Don't include the zip itself if it's in the root
                    if file == self.zip_filename:
                        continue
                        
                    zipf.write(file_path, os.path.relpath(file_path, self.project_root))
        print("Archive created successfully.")

    def calculate_checksum(self, filepath):
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def update_manifest(self):
        print("--- Updating Manifest ---")
        if not os.path.exists(self.zip_filename):
            print(f"Error: {self.zip_filename} not found.")
            return

        checksum = self.calculate_checksum(self.zip_filename)
        size = os.path.getsize(self.zip_filename)
        timestamp = datetime.datetime.now().isoformat()

        manifest_content = f"# Delivery Manifest\n\n"
        manifest_content += f"**Generated At:** {timestamp}\n\n"
        manifest_content += f"## Artifacts\n"
        manifest_content += f"| Filename | Size (Bytes) | SHA256 Checksum |\n"
        manifest_content += f"| :--- | :--- | :--- |\n"
        manifest_content += f"| `{self.zip_filename}` | {size} | `{checksum}` |\n"

        with open("DELIVERY_MANIFEST.md", "w") as f:
            f.write(manifest_content)
        
        print("DELIVERY_MANIFEST.md updated.")

if __name__ == "__main__":
    manager = ReleaseManager()
    manager.create_archive()
    manager.update_manifest()
