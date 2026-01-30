# Repository Management Scripts

This directory contains powerful scripts for managing git repositories with intelligent squash merging, optimization, and commit/push operations.

## Scripts Overview

### 1. intelligent_squash_merge.py

Intelligently analyzes and squashes commits by grouping them into logical categories.

**Features:**
- Analyzes commit patterns (fixes, features, documentation, etc.)
- Interactive and automated squash modes
- Squash merge between branches with intelligent message generation
- Dry-run mode for safety

**Usage:**

```bash
# Interactive mode - choose what to squash
python3 intelligent_squash_merge.py --interactive

# Auto-squash last 10 commits by pattern
python3 intelligent_squash_merge.py --auto --commits 10

# Squash merge a branch into main
python3 intelligent_squash_merge.py --branch feature-branch --target main

# Dry run to see what would happen
python3 intelligent_squash_merge.py --auto --dry-run
```

**Examples:**

```bash
# Analyze and squash commits on current branch
python3 intelligent_squash_merge.py --interactive

# Squash all fix commits together
python3 intelligent_squash_merge.py --auto --commits 20

# Merge feature branch with intelligent squashing
python3 intelligent_squash_merge.py --branch feature/new-auth --target main
```

### 2. repo_optimizer.py

Analyzes repositories for optimization opportunities including duplicate files, large files, and stale branches.

**Features:**
- Duplicate file detection using SHA256 hashing
- Large file identification
- Stale branch analysis
- Git object database optimization
- .gitignore coverage checking

**Usage:**

```bash
# Full repository analysis
python3 repo_optimizer.py --analyze

# Find duplicate files
python3 repo_optimizer.py --find-duplicates

# Find files larger than 5MB
python3 repo_optimizer.py --find-large-files 5

# Find branches inactive for 90+ days
python3 repo_optimizer.py --clean-branches --days 90

# Apply automatic optimizations
python3 repo_optimizer.py --optimize --auto

# Dry run
python3 repo_optimizer.py --analyze --dry-run
```

**Examples:**

```bash
# Full analysis with report generation
python3 repo_optimizer.py --analyze

# Find what's taking up space
python3 repo_optimizer.py --find-large-files 1

# Clean up old branches
python3 repo_optimizer.py --clean-branches --days 60

# Optimize git database
python3 repo_optimizer.py --optimize --auto
```

### 3. commit_push_manager.py

Unified interface for managing commits and pushes to local and remote repositories.

### 4. workflow.py

Convenience script that combines all tools into common workflows.

**Features:**
- Smart commit message generation
- Pre-commit validation
- Multi-remote support
- Branch synchronization
- Conflict detection
- Dry-run mode

**Usage:**

```bash
# Commit with message
python3 commit_push_manager.py --message "Fix authentication bug" --stage-all

# Auto-generate commit message and push
python3 commit_push_manager.py --auto-message --stage-all --push

# Sync with remote
python3 commit_push_manager.py --sync --remote origin --branch main

# Push to all remotes
python3 commit_push_manager.py --message "Update docs" --push-all

# Show detailed status
python3 commit_push_manager.py --status

# Dry run
python3 commit_push_manager.py --message "Test" --push --dry-run
```

**Examples:**

```bash
# Quick commit and push
python3 commit_push_manager.py --auto-message --stage-all --push

# Sync local branch with remote
python3 commit_push_manager.py --sync --remote origin

# Force push with lease (safer than --force)
python3 commit_push_manager.py --message "Rewrite history" --push --force

# Check repository status
python3 commit_push_manager.py --status
```

**Features:**
- Pre-built workflows for common tasks
- Automated multi-step processes
- Simple command-line interface
- Combines all three tools intelligently

**Usage:**

```bash
# Quick commit and analyze
python3 workflow.py optimize-and-commit

# Daily development sync
python3 workflow.py daily-sync

# Quick commit with auto-message
python3 workflow.py quick-commit

# Quick commit and push
python3 workflow.py quick-commit --push

# Prepare for release
python3 workflow.py release-prep --version 2.0.0

# Repository cleanup analysis
python3 workflow.py cleanup
```

## Common Workflows

### Workflow 1: Clean Up and Optimize Repository

```bash
# 1. Analyze repository
python3 repo_optimizer.py --analyze

# 2. Remove duplicate files (review output first)
# Manually remove duplicates based on report

# 3. Clean up stale branches
python3 repo_optimizer.py --clean-branches --days 90
# Review and delete unneeded branches

# 4. Optimize git database
python3 repo_optimizer.py --optimize --auto

# 5. Commit changes
python3 commit_push_manager.py --message "Clean up repository" --stage-all --push
```

### Workflow 2: Intelligent Branch Merge

```bash
# 1. Squash merge feature branch
python3 intelligent_squash_merge.py --branch feature/new-feature --target main

# 2. Review the merge
git log -5

# 3. Push to remote
python3 commit_push_manager.py --push --remote origin --branch main
```

### Workflow 3: Daily Development

```bash
# 1. Check status
python3 commit_push_manager.py --status

# 2. Stage and commit with auto-message
python3 commit_push_manager.py --auto-message --stage-all

# 3. Sync with remote
python3 commit_push_manager.py --sync --remote origin

# 4. Push changes
python3 commit_push_manager.py --push
```

### Workflow 4: Release Preparation

```bash
# 1. Analyze and optimize
python3 repo_optimizer.py --analyze
python3 repo_optimizer.py --optimize --auto

# 2. Squash commits since last release
python3 intelligent_squash_merge.py --auto --commits 50

# 3. Create release commit
python3 commit_push_manager.py --message "Release v2.0.0" --stage-all

# 4. Push to all remotes
python3 commit_push_manager.py --push-all
```

## Best Practices

### Using Squash Merge

1. **Always use --dry-run first** to preview changes
2. **Work on a backup branch** when learning the tool
3. **Review commit groups** before auto-squashing
4. **Keep important commits** separate (releases, major features)

### Repository Optimization

1. **Run analysis regularly** (weekly or monthly)
2. **Review reports before acting** on optimization suggestions
3. **Keep .gitignore updated** based on recommendations
4. **Clean stale branches** to keep repository tidy
5. **Use --dry-run** to preview changes

### Commit and Push Management

1. **Use auto-message for small changes**, manual messages for important commits
2. **Always sync before pushing** to avoid conflicts
3. **Use --force carefully** (prefer --force-with-lease via --force flag)
4. **Check status regularly** to track changes
5. **Validate messages** meet your team's conventions

## Configuration

### Repository Path

All scripts accept `--repo-path` to work on a specific repository:

```bash
python3 intelligent_squash_merge.py --repo-path /path/to/repo --analyze
```

### Dry Run

Always available for safety:

```bash
python3 <script>.py --dry-run <other-args>
```

### Verbose Mode

Available in commit_push_manager.py:

```bash
python3 commit_push_manager.py --verbose --status
```

## Troubleshooting

### "Not a git repository" Error

Ensure you're in a git repository or use `--repo-path`:

```bash
python3 script.py --repo-path /path/to/repo
```

### "No staged changes" Error

Stage files first:

```bash
git add .
# or
python3 commit_push_manager.py --stage-all --message "Update"
```

### Merge Conflicts

The tools will detect conflicts but won't resolve them automatically. Resolve manually:

```bash
git status
# Fix conflicts
git add <resolved-files>
git commit
```

### Permission Errors

Make scripts executable:

```bash
chmod +x scripts/*.py
```

## Integration with CI/CD

These scripts can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Optimize Repository
  run: python3 scripts/repo_optimizer.py --analyze

- name: Commit Changes
  run: |
    python3 scripts/commit_push_manager.py \
      --auto-message --stage-all --push
```

## Safety Features

All scripts include:

- ✓ Dry-run mode
- ✓ Input validation
- ✓ Error handling
- ✓ Reversible operations (where possible)
- ✓ Detailed logging

## Requirements

- Python 3.6+
- Git 2.0+
- Standard Python library (no external dependencies)

## Support

For issues or questions:
1. Check this README
2. Use `--help` flag on any script
3. Review generated reports (in optimization_report.json)
4. Check git status and logs

## License

These scripts are part of the HeadyConnection repository and follow the repository's license.
