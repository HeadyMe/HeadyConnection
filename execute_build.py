#!/usr/bin/env python3
"""
Utility to clone a GitHub repository, extract a packaged archive, and run a build script.

This script automates the steps required to set up a local working copy of a
repository, extract an installation package (ZIP archive), and execute a
specified build script. It is designed to aid in building packages like the
Heady Golden Master builder and similar projects.

Example usage:

    python3 execute_build.py \
        --repo-url https://github.com/HeadyConnection/Heady.git \
        --zip-file /path/to/HeadySystems_package_v1_0_0.zip \
        --build-script Heady_Golden_Master_Builder_v_1_0_0.py \
        --work-dir /tmp/heady_build \
        --output-dir /tmp/heady_package

This will clone the repository into `/tmp/heady_build/Heady`, extract the contents
of the ZIP archive into `/tmp/heady_build/extracted`, and then invoke the build
script with the repository as the source directory and `/tmp/heady_package` as
the output directory.

Dependencies: git must be installed and available in your PATH.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd, cwd=None):
    """Run a command and stream its output. Raise an error on non-zero exit."""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command {' '.join(cmd)} failed with exit code {result.returncode}")


def clone_repository(repo_url: str, dest_dir: Path) -> Path:
    """Clone a git repository into the destination directory. Return the repo path."""
    repo_name = Path(repo_url).stem  # e.g. 'Heady' from .../Heady.git
    repo_path = dest_dir / repo_name
    if repo_path.exists():
        shutil.rmtree(repo_path)
    run_cmd(["git", "clone", repo_url, str(repo_path)])
    return repo_path


def extract_zip(zip_file: Path, dest_dir: Path) -> Path:
    """Extract a ZIP archive into dest_dir. Return the extraction path."""
    if not zip_file.is_file():
        raise FileNotFoundError(f"ZIP file not found: {zip_file}")
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.unpack_archive(str(zip_file), str(dest_dir))
    return dest_dir


def run_build_script(script_path: Path, source_dir: Path, output_dir: Path, version: str = "1.0.0") -> None:
    """Execute the build script with the given source and output directories."""
    if not script_path.is_file():
        raise FileNotFoundError(f"Build script not found: {script_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["python3", str(script_path), "--source-dir", str(source_dir), "--output-dir", str(output_dir), "--version", version, "--zip"]
    run_cmd(cmd)


def main():
    parser = argparse.ArgumentParser(description="Clone, extract, and run a build script.")
    parser.add_argument("--repo-url", required=True, help="URL of the Git repository to clone.")
    parser.add_argument("--zip-file", required=True, help="Path to the ZIP package to extract.")
    parser.add_argument("--build-script", required=True, help="Name of the build script to run (inside extracted or repo).")
    parser.add_argument("--work-dir", default="./work", help="Working directory to clone and extract into.")
    parser.add_argument("--output-dir", default="./build_output", help="Directory to write build output.")
    parser.add_argument("--version", default="1.0.0", help="Version identifier passed to the build script.")
    args = parser.parse_args()

    work_dir = Path(args.work_dir).resolve()
    repo_path = clone_repository(args.repo_url, work_dir)
    print(f"Cloned repository to: {repo_path}")

    extract_dir = work_dir / "extracted"
    zip_file = Path(args.zip_file).resolve()
    extract_zip(zip_file, extract_dir)
    print(f"Extracted ZIP contents to: {extract_dir}")

    # Determine build script location: check extracted dir first, then repo
    script_path = extract_dir / args.build_script
    if not script_path.exists():
        script_path = repo_path / args.build_script
        if not script_path.exists():
            raise FileNotFoundError(f"Build script {args.build_script} not found in either {extract_dir} or {repo_path}")

    output_dir = Path(args.output_dir).resolve()
    run_build_script(script_path, repo_path, output_dir, version=args.version)
    print(f"Build completed. Output in: {output_dir}")


if __name__ == "__main__":
    main()