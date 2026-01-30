# Repository Management Tools - Quick Reference

## Quick Commands

### Status & Analysis
```bash
# Repository status
python3 scripts/commit_push_manager.py --status

# Full analysis with report
python3 scripts/repo_optimizer.py --analyze

# Find duplicates
python3 scripts/repo_optimizer.py --find-duplicates

# Find large files (>5MB)
python3 scripts/repo_optimizer.py --find-large-files 5
```

### Commit & Push
```bash
# Quick commit with auto-message
python3 scripts/commit_push_manager.py --auto-message --stage-all

# Commit and push
python3 scripts/commit_push_manager.py --auto-message --stage-all --push

# Sync with remote
python3 scripts/commit_push_manager.py --sync --remote origin
```

### Squash & Merge
```bash
# Interactive squash
python3 scripts/intelligent_squash_merge.py --interactive

# Auto-squash last 10 commits
python3 scripts/intelligent_squash_merge.py --auto --commits 10

# Squash merge branches
python3 scripts/intelligent_squash_merge.py --branch feature --target main
```

### Workflows
```bash
# Daily development sync
python3 scripts/workflow.py daily-sync

# Quick commit and push
python3 scripts/workflow.py quick-commit --push

# Prepare for release
python3 scripts/workflow.py release-prep --version 1.0.0

# Repository cleanup
python3 scripts/workflow.py cleanup
```

## Safety First

Always add `--dry-run` to preview changes:
```bash
python3 scripts/intelligent_squash_merge.py --auto --dry-run
python3 scripts/repo_optimizer.py --analyze --dry-run
```

## Help

Get help for any script:
```bash
python3 scripts/<script-name>.py --help
```

## Common Workflows

### Morning Routine
```bash
python3 scripts/workflow.py daily-sync
```

### Before Commit
```bash
python3 scripts/commit_push_manager.py --status
python3 scripts/commit_push_manager.py --auto-message --stage-all --push
```

### Weekly Cleanup
```bash
python3 scripts/workflow.py cleanup
python3 scripts/repo_optimizer.py --optimize --auto
```

### Release Preparation
```bash
python3 scripts/workflow.py release-prep --version 2.0.0
```

## Documentation

- **Full Documentation**: `scripts/README.md`
- **Main Guide**: `REPO_MANAGEMENT.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`

## Key Features

✅ Pattern-based commit analysis
✅ Duplicate file detection  
✅ Large file identification
✅ Auto-commit messages
✅ Multi-remote support
✅ Dry-run mode
✅ Workflow automation

---
For more details, see the full documentation in the `scripts/` directory.
