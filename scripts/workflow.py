#!/usr/bin/env python3
"""
Repository Management Workflow

This is a convenience script that combines all three repository management tools
into common workflows.

Usage:
    python3 workflow.py optimize-and-commit
    python3 workflow.py daily-sync
    python3 workflow.py release-prep --version 2.0.0
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_script(script_name: str, args: list) -> int:
    """Run a script and return its exit code."""
    script_path = Path(__file__).parent / f"{script_name}.py"
    cmd = ['python3', str(script_path)] + args
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, check=False)
    return result.returncode


def workflow_optimize_and_commit():
    """Optimize repository and commit changes."""
    print("\n🔧 WORKFLOW: Optimize and Commit\n")
    
    # Step 1: Analyze repository
    print("Step 1: Analyzing repository...")
    if run_script('repo_optimizer', ['--analyze']) != 0:
        print("❌ Analysis failed")
        return 1
    
    # Step 2: Show status
    print("\nStep 2: Checking repository status...")
    if run_script('commit_push_manager', ['--status']) != 0:
        print("❌ Status check failed")
        return 1
    
    print("\n✓ Workflow complete! Review optimization_report.json for recommendations.")
    return 0


def workflow_daily_sync():
    """Daily development sync workflow."""
    print("\n📅 WORKFLOW: Daily Sync\n")
    
    # Step 1: Check status
    print("Step 1: Checking status...")
    if run_script('commit_push_manager', ['--status']) != 0:
        print("❌ Status check failed")
        return 1
    
    # Step 2: Sync with remote
    print("\nStep 2: Syncing with remote...")
    if run_script('commit_push_manager', ['--sync', '--remote', 'origin']) != 0:
        print("❌ Sync failed")
        return 1
    
    print("\n✓ Daily sync complete!")
    return 0


def workflow_quick_commit(message: str = None, push: bool = False):
    """Quick commit with optional push."""
    print("\n⚡ WORKFLOW: Quick Commit\n")
    
    args = ['--stage-all']
    
    if message:
        args.extend(['--message', message])
    else:
        args.append('--auto-message')
    
    if push:
        args.append('--push')
    
    print("Creating commit...")
    if run_script('commit_push_manager', args) != 0:
        print("❌ Commit failed")
        return 1
    
    print("\n✓ Quick commit complete!")
    return 0


def workflow_release_prep(version: str):
    """Prepare repository for release."""
    print(f"\n🚀 WORKFLOW: Release Preparation (v{version})\n")
    
    # Step 1: Analyze and optimize
    print("Step 1: Analyzing repository...")
    if run_script('repo_optimizer', ['--analyze']) != 0:
        print("❌ Analysis failed")
        return 1
    
    # Step 2: Optimize git database
    print("\nStep 2: Optimizing git database...")
    if run_script('repo_optimizer', ['--optimize', '--auto']) != 0:
        print("❌ Optimization failed")
        return 1
    
    # Step 3: Create release commit
    print(f"\nStep 3: Creating release commit...")
    message = f"Release v{version}"
    if run_script('commit_push_manager', ['--message', message, '--stage-all']) != 0:
        print("❌ Commit failed")
        return 1
    
    print(f"\n✓ Release preparation complete for v{version}!")
    print("Review changes and push when ready:")
    print(f"  python3 scripts/commit_push_manager.py --push")
    return 0


def workflow_cleanup():
    """Clean up repository."""
    print("\n🧹 WORKFLOW: Repository Cleanup\n")
    
    # Step 1: Find duplicates
    print("Step 1: Finding duplicate files...")
    if run_script('repo_optimizer', ['--find-duplicates']) != 0:
        print("❌ Duplicate search failed")
        return 1
    
    # Step 2: Find large files
    print("\nStep 2: Finding large files (>5MB)...")
    if run_script('repo_optimizer', ['--find-large-files', '5']) != 0:
        print("❌ Large file search failed")
        return 1
    
    # Step 3: Find stale branches
    print("\nStep 3: Finding stale branches (>60 days)...")
    if run_script('repo_optimizer', ['--clean-branches', '--days', '60']) != 0:
        print("❌ Branch analysis failed")
        return 1
    
    print("\n✓ Cleanup analysis complete! Review findings and take action as needed.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Repository management workflow automation"
    )
    
    subparsers = parser.add_subparsers(dest='workflow', help='Workflow to run')
    
    # optimize-and-commit workflow
    subparsers.add_parser(
        'optimize-and-commit',
        help='Analyze repository and prepare for commit'
    )
    
    # daily-sync workflow
    subparsers.add_parser(
        'daily-sync',
        help='Daily development sync workflow'
    )
    
    # quick-commit workflow
    quick_parser = subparsers.add_parser(
        'quick-commit',
        help='Quick commit with auto-message'
    )
    quick_parser.add_argument('--message', '-m', help='Commit message')
    quick_parser.add_argument('--push', action='store_true', help='Push after commit')
    
    # release-prep workflow
    release_parser = subparsers.add_parser(
        'release-prep',
        help='Prepare repository for release'
    )
    release_parser.add_argument('--version', required=True, help='Release version')
    
    # cleanup workflow
    subparsers.add_parser(
        'cleanup',
        help='Analyze repository for cleanup opportunities'
    )
    
    args = parser.parse_args()
    
    if not args.workflow:
        parser.print_help()
        print("\nAvailable workflows:")
        print("  optimize-and-commit  - Analyze and prepare for commit")
        print("  daily-sync          - Sync with remote")
        print("  quick-commit        - Quick commit with auto-message")
        print("  release-prep        - Prepare for release")
        print("  cleanup             - Analyze for cleanup")
        sys.exit(1)
    
    # Run the selected workflow
    if args.workflow == 'optimize-and-commit':
        sys.exit(workflow_optimize_and_commit())
    elif args.workflow == 'daily-sync':
        sys.exit(workflow_daily_sync())
    elif args.workflow == 'quick-commit':
        sys.exit(workflow_quick_commit(args.message, args.push))
    elif args.workflow == 'release-prep':
        sys.exit(workflow_release_prep(args.version))
    elif args.workflow == 'cleanup':
        sys.exit(workflow_cleanup())


if __name__ == '__main__':
    main()
