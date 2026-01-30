#!/usr/bin/env python3
"""
Intelligent Squash Merge Script

This script provides intelligent squashing of commits by analyzing commit messages,
authors, and changes to create optimized merge commits. It can work in both
interactive and automated modes.

Features:
- Analyzes commit patterns and groups related commits
- Detects merge commits and handles them appropriately
- Preserves important commit metadata
- Supports dry-run mode for safety
- Can work with multiple branches

Usage:
    python3 intelligent_squash_merge.py --branch feature-branch --target main
    python3 intelligent_squash_merge.py --interactive
    python3 intelligent_squash_merge.py --auto --commits 5
"""

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple


class CommitInfo:
    """Represents a git commit with its metadata."""
    
    def __init__(self, sha: str, message: str, author: str, date: str, files: List[str]):
        self.sha = sha
        self.message = message
        self.author = author
        self.date = date
        self.files = files
        
    def __repr__(self):
        return f"CommitInfo({self.sha[:8]}, {self.message[:30]}...)"


class IntelligentSquashMerge:
    """Handles intelligent squash merge operations."""
    
    def __init__(self, repo_path: Path = None, dry_run: bool = False):
        self.repo_path = repo_path or Path.cwd()
        self.dry_run = dry_run
        
    def run_git_command(self, cmd: List[str], capture_output: bool = True) -> str:
        """Execute a git command and return output."""
        try:
            if self.dry_run and cmd[1] not in ['log', 'show', 'diff', 'status', 'branch']:
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
            print(f"Error executing git command: {' '.join(cmd)}")
            print(f"Error: {e.stderr if hasattr(e, 'stderr') else str(e)}")
            sys.exit(1)
    
    def get_commits(self, branch: str, count: int = None) -> List[CommitInfo]:
        """Get commits from the specified branch."""
        cmd = ['git', 'log', '--format=%H|%s|%an|%ai', branch]
        if count:
            cmd.append(f'-{count}')
        
        output = self.run_git_command(cmd)
        commits = []
        
        for line in output.split('\n'):
            if not line:
                continue
            sha, message, author, date = line.split('|', 3)
            
            # Get files changed in this commit
            files_output = self.run_git_command(
                ['git', 'show', '--name-only', '--format=', sha]
            )
            files = [f for f in files_output.split('\n') if f]
            
            commits.append(CommitInfo(sha, message, author, date, files))
        
        return commits
    
    def analyze_commit_patterns(self, commits: List[CommitInfo]) -> Dict[str, List[CommitInfo]]:
        """Analyze commits and group them by patterns."""
        groups = defaultdict(list)
        
        for commit in commits:
            # Determine commit category
            msg_lower = commit.message.lower()
            
            if any(keyword in msg_lower for keyword in ['fix', 'bug', 'patch', 'hotfix']):
                groups['fixes'].append(commit)
            elif any(keyword in msg_lower for keyword in ['feat', 'feature', 'add', 'implement']):
                groups['features'].append(commit)
            elif any(keyword in msg_lower for keyword in ['doc', 'readme', 'comment']):
                groups['documentation'].append(commit)
            elif any(keyword in msg_lower for keyword in ['test', 'spec']):
                groups['tests'].append(commit)
            elif any(keyword in msg_lower for keyword in ['refactor', 'clean', 'optimize']):
                groups['refactoring'].append(commit)
            elif any(keyword in msg_lower for keyword in ['merge', 'pull request', 'pr']):
                groups['merges'].append(commit)
            else:
                groups['other'].append(commit)
        
        return groups
    
    def create_squash_commit_message(self, commits: List[CommitInfo], group_name: str) -> str:
        """Create an intelligent squash commit message."""
        if len(commits) == 1:
            return commits[0].message
        
        # Create a descriptive title
        title = f"[{group_name.title()}] Consolidated changes"
        
        # List all original commit messages
        details = []
        for commit in commits:
            details.append(f"  - {commit.message} ({commit.author}, {commit.sha[:8]})")
        
        # Combine
        message = f"{title}\n\nConsolidated commits:\n" + "\n".join(details)
        return message
    
    def get_common_ancestor(self, branch1: str, branch2: str) -> str:
        """Find common ancestor between two branches."""
        return self.run_git_command(['git', 'merge-base', branch1, branch2])
    
    def squash_commits(self, commits: List[CommitInfo], message: str):
        """Squash the given commits with the specified message."""
        if len(commits) < 2:
            print("Need at least 2 commits to squash")
            return
        
        # Reset to the commit before the first one we want to squash
        oldest_commit = commits[-1].sha
        parent_commit = self.run_git_command(['git', 'rev-parse', f'{oldest_commit}^'])
        
        print(f"Squashing {len(commits)} commits...")
        
        # Soft reset to parent
        self.run_git_command(['git', 'reset', '--soft', parent_commit])
        
        # Create new squashed commit
        self.run_git_command(['git', 'commit', '-m', message])
        
        print(f"Successfully squashed {len(commits)} commits")
    
    def interactive_squash(self, branch: str):
        """Interactive mode for squashing commits."""
        commits = self.get_commits(branch, count=20)
        
        print(f"\n=== Recent commits on {branch} ===")
        for i, commit in enumerate(commits):
            print(f"{i+1}. [{commit.sha[:8]}] {commit.message} ({commit.author})")
        
        print("\nCommit groups:")
        groups = self.analyze_commit_patterns(commits)
        
        for group_name, group_commits in groups.items():
            if not group_commits:
                continue
            print(f"\n{group_name.upper()} ({len(group_commits)} commits):")
            for commit in group_commits:
                print(f"  - [{commit.sha[:8]}] {commit.message}")
        
        print("\nOptions:")
        print("1. Squash by group")
        print("2. Squash range of commits")
        print("3. Exit")
        
        choice = input("\nSelect option: ")
        
        if choice == "1":
            group_name = input("Enter group name to squash: ")
            if group_name in groups and len(groups[group_name]) > 1:
                message = self.create_squash_commit_message(groups[group_name], group_name)
                print(f"\nProposed commit message:\n{message}")
                confirm = input("\nProceed? (y/n): ")
                if confirm.lower() == 'y':
                    self.squash_commits(groups[group_name], message)
            else:
                print("Invalid group or not enough commits in group")
        
        elif choice == "2":
            start = int(input("Start index: ")) - 1
            end = int(input("End index: ")) - 1
            if 0 <= start <= end < len(commits):
                selected = commits[start:end+1]
                message = input("Enter commit message: ")
                self.squash_commits(selected, message)
            else:
                print("Invalid range")
    
    def auto_squash(self, branch: str, count: int):
        """Automatically squash commits by intelligent grouping."""
        commits = self.get_commits(branch, count=count)
        groups = self.analyze_commit_patterns(commits)
        
        print(f"\n=== Auto-squashing on {branch} ===")
        
        for group_name, group_commits in groups.items():
            if len(group_commits) > 1:
                message = self.create_squash_commit_message(group_commits, group_name)
                print(f"\nSquashing {len(group_commits)} {group_name} commits")
                print(f"Message: {message.split(chr(10))[0]}")
                self.squash_commits(group_commits, message)
    
    def merge_with_squash(self, source_branch: str, target_branch: str):
        """Perform a squash merge from source to target branch."""
        print(f"\n=== Squash merging {source_branch} into {target_branch} ===")
        
        # Checkout target branch
        self.run_git_command(['git', 'checkout', target_branch])
        
        # Get all commits in source that aren't in target
        merge_base = self.get_common_ancestor(source_branch, target_branch)
        commits = self.get_commits(f'{merge_base}..{source_branch}')
        
        print(f"Found {len(commits)} commits to merge")
        
        # Perform squash merge
        self.run_git_command(['git', 'merge', '--squash', source_branch])
        
        # Create merge message
        groups = self.analyze_commit_patterns(commits)
        merge_message = f"Merge {source_branch} into {target_branch}\n\n"
        
        for group_name, group_commits in groups.items():
            if group_commits:
                merge_message += f"\n{group_name.title()} ({len(group_commits)}):\n"
                for commit in group_commits:
                    merge_message += f"  - {commit.message}\n"
        
        print(f"\nProposed merge message:\n{merge_message}")
        
        if not self.dry_run:
            confirm = input("\nProceed with merge? (y/n): ")
            if confirm.lower() == 'y':
                self.run_git_command(['git', 'commit', '-m', merge_message])
                print("Merge completed successfully")
            else:
                print("Merge aborted")
                self.run_git_command(['git', 'reset', '--hard', 'HEAD'])


def main():
    parser = argparse.ArgumentParser(
        description="Intelligent squash merge tool for git repositories"
    )
    parser.add_argument(
        '--branch',
        help='Branch to work with'
    )
    parser.add_argument(
        '--target',
        help='Target branch for merge operations'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Automatically squash commits by pattern'
    )
    parser.add_argument(
        '--commits',
        type=int,
        default=10,
        help='Number of recent commits to consider (default: 10)'
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
    
    merger = IntelligentSquashMerge(
        repo_path=args.repo_path,
        dry_run=args.dry_run
    )
    
    if args.interactive:
        branch = args.branch or merger.run_git_command(['git', 'branch', '--show-current'])
        merger.interactive_squash(branch)
    elif args.auto:
        branch = args.branch or merger.run_git_command(['git', 'branch', '--show-current'])
        merger.auto_squash(branch, args.commits)
    elif args.branch and args.target:
        merger.merge_with_squash(args.branch, args.target)
    else:
        print("Please specify operation mode:")
        print("  --interactive: Interactive squash mode")
        print("  --auto: Automatic squash by pattern")
        print("  --branch SOURCE --target TARGET: Squash merge between branches")
        sys.exit(1)


if __name__ == '__main__':
    main()
