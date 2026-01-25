#!/usr/bin/env python3
import argparse, os, sys, tarfile, zipfile, subprocess
from pathlib import Path

def extract_archive(archive_path, output_dir):
    if not archive_path.is_file(): raise ValueError(f"Archive {archive_path} missing")
    output_dir.mkdir(parents=True, exist_ok=True)
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, "r") as z: z.extractall(output_dir)
    elif tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path, "r:*") as t: t.extractall(output_dir)
    else: raise ValueError("Unsupported format")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_path", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--init-cmd", type=str)
    args = parser.parse_args()
    out = args.output or Path.cwd() / args.archive_path.stem
    print(f"Extracting {args.archive_path} to {out}...")
    extract_archive(args.archive_path, out)
    if args.init_cmd:
        subprocess.run(args.init_cmd.format(extracted_dir=str(out.resolve())), shell=True)

if __name__ == "__main__": main()
