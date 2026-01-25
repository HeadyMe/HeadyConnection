#!/usr/bin/env python3
import os
import shutil
import datetime
import hashlib
import stat
import zipfile

class ReleaseManager:
    def __init__(self, base_dir="releases"):
        self.base_dir = base_dir
        self.current_dir = os.path.join(base_dir, "current")
        self.previous_dir = os.path.join(base_dir, "previous")
        self.artifacts = [
            "Heady_v13_Gold_Master.zip",
            "apply_heady_golden_master.sh",
            "DELIVERY_MANIFEST.md",
            "actuator.py",
            "Heady_it1_v_1_0_0.py",
            "Heady_it2_v_1_0_0.py",
            "Heady_it3_v_1_0_0.py",
            "Heady_it4_v_1_0_0.py"
        ]

    def setup_directories(self):
        if not os.path.exists(self.previous_dir):
            os.makedirs(self.previous_dir)
        if not os.path.exists(self.current_dir):
            os.makedirs(self.current_dir)

    def archive_current(self):
        # If current is not empty, zip it and move to previous
        if os.path.exists(self.current_dir) and os.listdir(self.current_dir):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"release_{timestamp}"
            archive_path = os.path.join(self.previous_dir, archive_name)
            print(f"Archiving existing current release to {archive_path}.zip...")
            
            # Create zip of current contents
            shutil.make_archive(archive_path, 'zip', self.current_dir)
            
            # Clean current (unlock first to ensure deletion)
            self._unlock_directory(self.current_dir)
            for item in os.listdir(self.current_dir):
                item_path = os.path.join(self.current_dir, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

    def _unlock_directory(self, directory):
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                os.chmod(os.path.join(root, d), stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
            for f in files:
                os.chmod(os.path.join(root, f), stat.S_IWRITE | stat.S_IREAD)

    def package_current(self):
        print("Packaging artifacts to releases/current...")
        for artifact in self.artifacts:
            if os.path.exists(artifact):
                shutil.copy2(artifact, self.current_dir)
                print(f"  Copied {artifact}")
            else:
                print(f"  Warning: Artifact {artifact} not found.")

    def generate_audit_manifest(self):
        print("Generating AUDIT_MANIFEST.sha256...")
        manifest_path = os.path.join(self.current_dir, "AUDIT_MANIFEST.sha256")
        with open(manifest_path, "w") as manifest:
            manifest.write(f"# Auditable Build Manifest - Generated {datetime.datetime.now().isoformat()}\n")
            for root, _, files in os.walk(self.current_dir):
                for file in files:
                    if file == "AUDIT_MANIFEST.sha256": continue
                    filepath = os.path.join(root, file)
                    sha256 = self._get_checksum(filepath)
                    relpath = os.path.relpath(filepath, self.current_dir)
                    manifest.write(f"{sha256}  {relpath}\n")
        return manifest_path

    def _get_checksum(self, filepath):
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def lock_release(self):
        print("Locking releases/current (Read-Only Mode)...")
        # Make files read-only (chmod 444 or 555)
        for root, dirs, files in os.walk(self.current_dir):
            for f in files:
                p = os.path.join(root, f)
                os.chmod(p, stat.S_IREAD) 
            for d in dirs:
                p = os.path.join(root, d)
                os.chmod(p, stat.S_IREAD | stat.S_IEXEC) 

    def execute(self):
        print("=== Heady Release Manager ===")
        self.setup_directories()
        self.archive_current()
        self.package_current()
        self.generate_audit_manifest()
        self.lock_release()
        print("\n\u2705 Release Process Complete.")
        print(f"   Current Location: {os.path.abspath(self.current_dir)}")
        print(f"   Archive Location: {os.path.abspath(self.previous_dir)}")

if __name__ == "__main__":
    ReleaseManager().execute()
