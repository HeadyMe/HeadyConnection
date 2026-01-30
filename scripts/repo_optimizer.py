#!/usr/bin/env python3
"""
Repository Optimizer Script

This script analyzes and optimizes git repositories by:
- Detecting duplicate files
- Finding large files that could be optimized
- Identifying stale branches
- Cleaning up unnecessary files
- Providing optimization recommendations

Features:
- File size analysis
- Duplicate detection using hash comparison
- Git history analysis
- Branch cleanup recommendations
- Automatic and manual optimization modes

Usage:
    python3 repo_optimizer.py --analyze
    python3 repo_optimizer.py --optimize --auto
    python3 repo_optimizer.py --find-duplicates
    python3 repo_optimizer.py --clean-branches --days 90
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Tuple


class RepoOptimizer:
    """Handles repository optimization operations."""
    
    def __init__(self, repo_path: Path = None, dry_run: bool = False):
        self.repo_path = repo_path or Path.cwd()
        self.dry_run = dry_run
        self.findings = {
            'duplicates': [],
            'large_files': [],
            'stale_branches': [],
            'optimization_suggestions': []
        }
    
    def run_command(self, cmd: List[str], capture_output: bool = True) -> str:
        """Execute a command and return output."""
        try:
            if self.dry_run and not capture_output:
                print(f"[DRY RUN] Would execute: {' '.join(cmd)}")
                return ""
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=capture_output,
                text=True,
                check=True
            )
            return result.stdout.strip() if capture_output else ""
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {' '.join(cmd)}")
            return ""
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            print(f"Error hashing {file_path}: {e}")
            raise
    
    def find_duplicates(self) -> Dict[str, List[Path]]:
        """Find duplicate files in the repository."""
        print("\n=== Finding Duplicate Files ===")
        
        hash_map = defaultdict(list)
        ignore_dirs = {'.git', '__pycache__', 'node_modules', 'vendor', 'dist', 'build'}
        
        for root, dirs, files in os.walk(self.repo_path):
            # Remove ignored directories from traversal
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for filename in files:
                file_path = Path(root) / filename
                if file_path.stat().st_size > 0:  # Skip empty files
                    try:
                        file_hash = self.calculate_file_hash(file_path)
                        hash_map[file_hash].append(file_path)
                    except (OSError, IOError, PermissionError) as e:
                        # Skip files that can't be read
                        print(f"Warning: Could not read {file_path}: {e}")
                        continue
        
        # Find duplicates
        duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
        
        if duplicates:
            print(f"\nFound {len(duplicates)} sets of duplicate files:")
            for file_hash, paths in duplicates.items():
                total_size = paths[0].stat().st_size
                wasted_space = total_size * (len(paths) - 1)
                print(f"\n  Hash: {file_hash[:16]}... ({len(paths)} copies, wasting {wasted_space:,} bytes)")
                for path in paths:
                    rel_path = path.relative_to(self.repo_path)
                    print(f"    - {rel_path}")
                self.findings['duplicates'].append({
                    'hash': file_hash,
                    'paths': [str(p.relative_to(self.repo_path)) for p in paths],
                    'size': total_size,
                    'wasted_space': wasted_space
                })
        else:
            print("No duplicate files found")
        
        return duplicates
    
    def find_large_files(self, threshold_mb: int = 1) -> List[Tuple[Path, int]]:
        """Find large files in the repository."""
        print(f"\n=== Finding Files Larger Than {threshold_mb}MB ===")
        
        large_files = []
        ignore_dirs = {'.git', '__pycache__', 'node_modules', 'vendor'}
        threshold_bytes = threshold_mb * 1024 * 1024
        
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for filename in files:
                file_path = Path(root) / filename
                size = file_path.stat().st_size
                if size > threshold_bytes:
                    large_files.append((file_path, size))
        
        large_files.sort(key=lambda x: x[1], reverse=True)
        
        if large_files:
            print(f"\nFound {len(large_files)} large files:")
            total_size = 0
            for path, size in large_files:
                rel_path = path.relative_to(self.repo_path)
                size_mb = size / (1024 * 1024)
                print(f"  {size_mb:>8.2f} MB - {rel_path}")
                total_size += size
                self.findings['large_files'].append({
                    'path': str(rel_path),
                    'size': size,
                    'size_mb': round(size_mb, 2)
                })
            
            print(f"\nTotal: {total_size / (1024 * 1024):.2f} MB in large files")
        else:
            print(f"No files larger than {threshold_mb}MB found")
        
        return large_files
    
    def analyze_stale_branches(self, days: int = 90) -> List[Dict]:
        """Find branches that haven't been updated recently."""
        print(f"\n=== Finding Branches Inactive for {days}+ Days ===")
        
        # Get all branches with last commit date
        output = self.run_command([
            'git', 'for-each-ref',
            '--format=%(refname:short)|%(committerdate:iso)|%(authorname)',
            'refs/heads/'
        ])
        
        if not output:
            print("No branches found or error accessing git")
            return []
        
        stale_branches = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for line in output.split('\n'):
            if not line:
                continue
            
            parts = line.split('|')
            if len(parts) < 2:
                continue
                
            branch_name = parts[0]
            date_str = parts[1]
            author = parts[2] if len(parts) > 2 else "Unknown"
            
            try:
                # Parse the date - handle ISO format with timezone
                # Example: 2026-01-30 19:05:30 -0700
                date_parts = date_str.split()
                if len(date_parts) >= 2:
                    date_time_str = f"{date_parts[0]} {date_parts[1]}"
                    last_commit = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                    
                    if last_commit < cutoff_date:
                        days_old = (datetime.now() - last_commit).days
                        stale_branches.append({
                            'name': branch_name,
                            'last_commit': date_str,
                            'days_old': days_old,
                            'author': author
                        })
            except (ValueError, IndexError) as e:
                # Skip branches with unparseable dates
                continue
        
        if stale_branches:
            print(f"\nFound {len(stale_branches)} stale branches:")
            for branch in stale_branches:
                print(f"  {branch['name']:30} - {branch['days_old']:4} days old (by {branch['author']})")
                self.findings['stale_branches'].append(branch)
        else:
            print(f"No branches inactive for {days}+ days")
        
        return stale_branches
    
    def analyze_git_objects(self):
        """Analyze git object database for optimization opportunities."""
        print("\n=== Analyzing Git Objects ===")
        
        # Count objects
        count_output = self.run_command(['git', 'count-objects', '-v'])
        print(f"\n{count_output}")
        
        # Check for loose objects
        lines = count_output.split('\n')
        for line in lines:
            if 'count:' in line:
                count = int(line.split(':')[1].strip())
                if count > 1000:
                    self.findings['optimization_suggestions'].append(
                        f"Consider running 'git gc' - {count} loose objects found"
                    )
            elif 'size-pack:' in line:
                size_kb = int(line.split(':')[1].strip())
                if size_kb > 100000:  # > 100MB
                    self.findings['optimization_suggestions'].append(
                        f"Large pack files detected ({size_kb} KB) - consider cleaning history"
                    )
    
    def check_gitignore_coverage(self):
        """Check if common generated files are properly ignored."""
        print("\n=== Checking .gitignore Coverage ===")
        
        common_patterns = {
            '__pycache__': 'Python cache directories',
            '*.pyc': 'Python compiled files',
            'node_modules': 'Node.js dependencies',
            '.DS_Store': 'macOS system files',
            '*.log': 'Log files',
            'dist': 'Distribution directories',
            'build': 'Build directories'
        }
        
        gitignore_path = self.repo_path / '.gitignore'
        if not gitignore_path.exists():
            print("No .gitignore file found")
            self.findings['optimization_suggestions'].append(
                "Create a .gitignore file to exclude generated files"
            )
            return
        
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        missing = []
        for pattern, description in common_patterns.items():
            if pattern not in gitignore_content:
                # Check if these files/dirs actually exist using pathlib
                if pattern.startswith('*.'):
                    ext = pattern[1:]
                    found = False
                    for path in self.repo_path.rglob(f'*{ext}'):
                        if path.is_file():
                            found = True
                            break
                    if found:
                        missing.append((pattern, description))
                else:
                    # Check for directory or file by name
                    found = False
                    for path in self.repo_path.rglob(pattern):
                        found = True
                        break
                    if found:
                        missing.append((pattern, description))
        
        if missing:
            print("\nSuggested additions to .gitignore:")
            for pattern, description in missing:
                print(f"  {pattern:20} # {description}")
                self.findings['optimization_suggestions'].append(
                    f"Add '{pattern}' to .gitignore ({description})"
                )
        else:
            print("✓ .gitignore appears well-configured")
    
    def generate_report(self):
        """Generate optimization report."""
        print("\n" + "="*60)
        print("OPTIMIZATION REPORT")
        print("="*60)
        
        # Summary
        print(f"\nDuplicate file sets: {len(self.findings['duplicates'])}")
        print(f"Large files: {len(self.findings['large_files'])}")
        print(f"Stale branches: {len(self.findings['stale_branches'])}")
        print(f"Optimization suggestions: {len(self.findings['optimization_suggestions'])}")
        
        # Recommendations
        if self.findings['optimization_suggestions']:
            print("\n=== Recommendations ===")
            for i, suggestion in enumerate(self.findings['optimization_suggestions'], 1):
                print(f"{i}. {suggestion}")
        
        # Save report
        report_path = self.repo_path / 'optimization_report.json'
        with open(report_path, 'w') as f:
            json.dump(self.findings, f, indent=2)
        print(f"\nDetailed report saved to: {report_path}")
    
    def optimize_auto(self):
        """Automatically apply safe optimizations."""
        print("\n=== Applying Automatic Optimizations ===")
        
        # Run git gc
        print("\nRunning git garbage collection...")
        self.run_command(['git', 'gc', '--auto'], capture_output=False)
        
        # Prune old reflog entries
        print("\nPruning old reflog entries...")
        self.run_command(['git', 'reflog', 'expire', '--expire=30.days.ago', '--all'])
        
        print("\n✓ Automatic optimizations complete")


def main():
    parser = argparse.ArgumentParser(
        description="Repository optimization tool"
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Run full analysis'
    )
    parser.add_argument(
        '--optimize',
        action='store_true',
        help='Apply optimizations'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Apply automatic safe optimizations'
    )
    parser.add_argument(
        '--find-duplicates',
        action='store_true',
        help='Find duplicate files'
    )
    parser.add_argument(
        '--find-large-files',
        type=int,
        metavar='MB',
        help='Find files larger than specified MB'
    )
    parser.add_argument(
        '--clean-branches',
        action='store_true',
        help='Find stale branches'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=90,
        help='Days threshold for stale branches (default: 90)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--repo-path',
        type=Path,
        help='Path to git repository (default: current directory)'
    )
    
    args = parser.parse_args()
    
    optimizer = RepoOptimizer(
        repo_path=args.repo_path,
        dry_run=args.dry_run
    )
    
    if args.analyze:
        optimizer.find_duplicates()
        optimizer.find_large_files(threshold_mb=1)
        optimizer.analyze_stale_branches(days=args.days)
        optimizer.analyze_git_objects()
        optimizer.check_gitignore_coverage()
        optimizer.generate_report()
    elif args.optimize:
        if args.auto:
            optimizer.optimize_auto()
        else:
            print("Interactive optimization not yet implemented")
            print("Use --auto for automatic optimizations")
    elif args.find_duplicates:
        optimizer.find_duplicates()
    elif args.find_large_files:
        optimizer.find_large_files(threshold_mb=args.find_large_files)
    elif args.clean_branches:
        optimizer.analyze_stale_branches(days=args.days)
    else:
        print("Please specify an operation:")
        print("  --analyze: Run full analysis")
        print("  --optimize --auto: Apply automatic optimizations")
        print("  --find-duplicates: Find duplicate files")
        print("  --find-large-files MB: Find large files")
        print("  --clean-branches: Find stale branches")
        sys.exit(1)


if __name__ == '__main__':
    main()
