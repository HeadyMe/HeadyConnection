#!/usr/bin/env python3
"""
Unified Commit and Push Utility

This script provides a unified interface for managing commits and pushes to both
local and remote repositories with intelligent validation and error handling.

Features:
- Smart commit message generation
- Pre-commit validation
- Support for multiple remotes
- Conflict detection and resolution assistance
- Branch synchronization
- Dry-run mode for safety

Usage:
    python3 commit_push_manager.py --message "Fix bug" --push
    python3 commit_push_manager.py --auto-message --push-all
    python3 commit_push_manager.py --sync --remote origin --branch main
"""

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class CommitPushManager:
    """Manages commit and push operations for git repositories."""
    
    def __init__(self, repo_path: Path = None, dry_run: bool = False, verbose: bool = False):
        self.repo_path = repo_path or Path.cwd()
        self.dry_run = dry_run
        self.verbose = verbose
        
    def run_git_command(self, cmd: List[str], capture_output: bool = True, check: bool = True) -> Tuple[int, str, str]:
        """Execute a git command and return (returncode, stdout, stderr)."""
        if self.dry_run and cmd[1] not in ['status', 'diff', 'log', 'branch', 'remote', 'show']:
            print(f"[DRY RUN] Would execute: {' '.join(cmd)}")
            return (0, "", "")
        
        if self.verbose:
            print(f"$ {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=capture_output,
                text=True,
                check=check
            )
            return (result.returncode, result.stdout, result.stderr)
        except subprocess.CalledProcessError as e:
            return (e.returncode, e.stdout, e.stderr)
    
    def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        _, stdout, _ = self.run_git_command(['git', 'branch', '--show-current'])
        return stdout.strip()
    
    def get_status(self) -> str:
        """Get git status output."""
        _, stdout, _ = self.run_git_command(['git', 'status', '--porcelain'])
        return stdout
    
    def has_uncommitted_changes(self) -> bool:
        """Check if there are uncommitted changes."""
        status = self.get_status()
        return bool(status.strip())
    
    def get_staged_files(self) -> List[str]:
        """Get list of staged files."""
        _, stdout, _ = self.run_git_command(['git', 'diff', '--cached', '--name-only'])
        return [f for f in stdout.split('\n') if f]
    
    def get_unstaged_files(self) -> List[str]:
        """Get list of unstaged modified files."""
        _, stdout, _ = self.run_git_command(['git', 'diff', '--name-only'])
        return [f for f in stdout.split('\n') if f]
    
    def get_untracked_files(self) -> List[str]:
        """Get list of untracked files."""
        _, stdout, _ = self.run_git_command(['git', 'ls-files', '--others', '--exclude-standard'])
        return [f for f in stdout.split('\n') if f]
    
    def stage_files(self, files: List[str] = None):
        """Stage files for commit. If files is None, stage all."""
        if files:
            for file in files:
                self.run_git_command(['git', 'add', file], capture_output=False)
        else:
            self.run_git_command(['git', 'add', '-A'], capture_output=False)
        
        print(f"✓ Staged {'all files' if not files else f'{len(files)} file(s)'}")
    
    def generate_commit_message(self) -> str:
        """Generate an intelligent commit message based on changes."""
        staged = self.get_staged_files()
        
        if not staged:
            return "Update repository"
        
        # Analyze file types
        file_types = defaultdict(list)
        for file in staged:
            ext = Path(file).suffix
            file_types[ext].append(file)
        
        # Generate message based on patterns
        if len(staged) == 1:
            file_path = Path(staged[0])
            if file_path.suffix == '.md':
                return f"Update {file_path.name}"
            elif file_path.suffix in ['.py', '.js', '.ts', '.java']:
                return f"Update {file_path.stem} implementation"
            else:
                return f"Update {file_path.name}"
        
        # Multiple files
        parts = []
        if '.py' in file_types:
            parts.append(f"Python files ({len(file_types['.py'])})")
        if '.js' in file_types or '.ts' in file_types:
            parts.append("JavaScript/TypeScript files")
        if '.md' in file_types:
            parts.append("documentation")
        if '.json' in file_types:
            parts.append("configuration")
        
        if parts:
            return f"Update {', '.join(parts)}"
        else:
            return f"Update {len(staged)} files"
    
    def validate_commit_message(self, message: str) -> Tuple[bool, str]:
        """Validate commit message format.
        
        Note: First line is limited to 72 characters following git conventions.
        This is a hard limit enforced by this tool.
        """
        if not message or not message.strip():
            return (False, "Commit message cannot be empty")
        
        if len(message) < 3:
            return (False, "Commit message too short (minimum 3 characters)")
        
        first_line = message.split('\n')[0]
        if len(first_line) > 72:
            return (False, "First line should be 72 characters or less (git convention)")
        
        return (True, "")
    
    def create_commit(self, message: str, amend: bool = False) -> bool:
        """Create a commit with the given message."""
        valid, error = self.validate_commit_message(message)
        if not valid:
            print(f"❌ Invalid commit message: {error}")
            return False
        
        cmd = ['git', 'commit', '-m', message]
        if amend:
            cmd.insert(2, '--amend')
        
        returncode, stdout, stderr = self.run_git_command(cmd, capture_output=False)
        
        if returncode == 0:
            print(f"✓ Created commit: {message}")
            return True
        else:
            print(f"❌ Failed to create commit: {stderr}")
            return False
    
    def get_remotes(self) -> List[str]:
        """Get list of configured remotes."""
        _, stdout, _ = self.run_git_command(['git', 'remote'])
        return [r for r in stdout.split('\n') if r]
    
    def get_remote_url(self, remote: str) -> str:
        """Get URL for a remote."""
        _, stdout, _ = self.run_git_command(['git', 'remote', 'get-url', remote])
        return stdout.strip()
    
    def check_remote_connection(self, remote: str) -> bool:
        """Check if remote is accessible."""
        returncode, _, _ = self.run_git_command(
            ['git', 'ls-remote', '--heads', remote],
            check=False
        )
        return returncode == 0
    
    def fetch_remote(self, remote: str) -> bool:
        """Fetch from remote."""
        print(f"Fetching from {remote}...")
        returncode, _, stderr = self.run_git_command(
            ['git', 'fetch', remote],
            capture_output=False,
            check=False
        )
        
        if returncode == 0:
            print(f"✓ Fetched from {remote}")
            return True
        else:
            print(f"❌ Failed to fetch from {remote}: {stderr}")
            return False
    
    def push_to_remote(self, remote: str, branch: str, force: bool = False) -> bool:
        """Push to remote."""
        cmd = ['git', 'push', remote, branch]
        if force:
            cmd.append('--force-with-lease')
        
        print(f"Pushing {branch} to {remote}...")
        returncode, stdout, stderr = self.run_git_command(cmd, capture_output=False, check=False)
        
        if returncode == 0:
            print(f"✓ Pushed to {remote}/{branch}")
            return True
        else:
            print(f"❌ Failed to push to {remote}: {stderr}")
            return False
    
    def sync_with_remote(self, remote: str, branch: str) -> bool:
        """Synchronize local branch with remote."""
        print(f"\n=== Synchronizing {branch} with {remote} ===")
        
        # Fetch latest
        if not self.fetch_remote(remote):
            return False
        
        # Check for divergence
        _, local_sha, _ = self.run_git_command(['git', 'rev-parse', branch])
        _, remote_sha, _ = self.run_git_command(['git', 'rev-parse', f'{remote}/{branch}'])
        
        local_sha = local_sha.strip()
        remote_sha = remote_sha.strip()
        
        if local_sha == remote_sha:
            print("✓ Already up to date")
            return True
        
        # Check if we can fast-forward
        returncode, _, _ = self.run_git_command(
            ['git', 'merge-base', '--is-ancestor', remote_sha, local_sha],
            check=False
        )
        
        if returncode == 0:
            # Remote is behind, we can push
            print("Remote is behind local. Pushing...")
            return self.push_to_remote(remote, branch)
        
        # Check if local is behind
        returncode, _, _ = self.run_git_command(
            ['git', 'merge-base', '--is-ancestor', local_sha, remote_sha],
            check=False
        )
        
        if returncode == 0:
            # Local is behind, we can pull
            print("Local is behind remote. Pulling...")
            returncode, _, _ = self.run_git_command(['git', 'pull', remote, branch])
            return returncode == 0
        
        print("⚠️  Branches have diverged. Manual intervention required.")
        return False
    
    def show_status(self):
        """Display detailed repository status."""
        print("\n=== Repository Status ===")
        
        branch = self.get_current_branch()
        print(f"Current branch: {branch}")
        
        staged = self.get_staged_files()
        unstaged = self.get_unstaged_files()
        untracked = self.get_untracked_files()
        
        if staged:
            print(f"\nStaged files ({len(staged)}):")
            for file in staged:
                print(f"  ✓ {file}")
        
        if unstaged:
            print(f"\nUnstaged changes ({len(unstaged)}):")
            for file in unstaged:
                print(f"  M {file}")
        
        if untracked:
            print(f"\nUntracked files ({len(untracked)}):")
            for file in untracked:
                print(f"  ? {file}")
        
        if not (staged or unstaged or untracked):
            print("\n✓ Working tree clean")
        
        # Show remotes
        remotes = self.get_remotes()
        if remotes:
            print(f"\nConfigured remotes ({len(remotes)}):")
            for remote in remotes:
                url = self.get_remote_url(remote)
                print(f"  {remote}: {url}")


def main():
    parser = argparse.ArgumentParser(
        description="Unified commit and push manager for git repositories"
    )
    parser.add_argument(
        '--message', '-m',
        help='Commit message'
    )
    parser.add_argument(
        '--auto-message',
        action='store_true',
        help='Generate commit message automatically'
    )
    parser.add_argument(
        '--stage-all',
        action='store_true',
        help='Stage all changes before committing'
    )
    parser.add_argument(
        '--push',
        action='store_true',
        help='Push after committing'
    )
    parser.add_argument(
        '--push-all',
        action='store_true',
        help='Push to all remotes'
    )
    parser.add_argument(
        '--remote',
        default='origin',
        help='Remote to push to (default: origin)'
    )
    parser.add_argument(
        '--branch',
        help='Branch to work with (default: current branch)'
    )
    parser.add_argument(
        '--sync',
        action='store_true',
        help='Synchronize with remote'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show detailed status'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force push with lease'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--repo-path',
        type=Path,
        help='Path to git repository (default: current directory)'
    )
    
    args = parser.parse_args()
    
    manager = CommitPushManager(
        repo_path=args.repo_path,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    if args.status:
        manager.show_status()
        return
    
    branch = args.branch or manager.get_current_branch()
    
    if args.sync:
        remotes = [args.remote] if not args.push_all else manager.get_remotes()
        for remote in remotes:
            manager.sync_with_remote(remote, branch)
        return
    
    # Handle commit and push workflow
    if args.message or args.auto_message:
        # Stage files if requested
        if args.stage_all:
            manager.stage_files()
        
        # Check if there are staged changes
        if not manager.get_staged_files():
            print("No staged changes to commit")
            sys.exit(1)
        
        # Get or generate commit message
        if args.auto_message:
            message = manager.generate_commit_message()
            print(f"Generated message: {message}")
        else:
            message = args.message
        
        # Create commit
        if manager.create_commit(message):
            # Push if requested
            if args.push or args.push_all:
                remotes = manager.get_remotes() if args.push_all else [args.remote]
                
                for remote in remotes:
                    manager.push_to_remote(remote, branch, force=args.force)
        else:
            sys.exit(1)
    else:
        print("Please specify an operation:")
        print("  --status: Show repository status")
        print("  --message 'msg' [--push]: Commit and optionally push")
        print("  --auto-message [--push]: Auto-generate message and commit")
        print("  --sync: Synchronize with remote")
        sys.exit(1)


if __name__ == '__main__':
    main()
