# HeadyConnection Repository Management Tools

This repository includes powerful tools for intelligent git repository management, including squash merging, optimization, and automated commit/push operations.

## Quick Start

### 1. Repository Optimization

Analyze your repository for optimization opportunities:

```bash
python3 scripts/repo_optimizer.py --analyze
```

This will:
- Find duplicate files
- Identify large files
- Detect stale branches
- Check .gitignore coverage
- Generate an optimization report

### 2. Intelligent Squash Merge

Clean up commit history with intelligent squashing:

```bash
python3 scripts/intelligent_squash_merge.py --interactive
```

This will:
- Analyze recent commits
- Group commits by type (fixes, features, docs, etc.)
- Allow you to squash groups intelligently
- Preserve important metadata

### 3. Unified Commit and Push

Streamline your commit and push workflow:

```bash
python3 scripts/commit_push_manager.py --auto-message --stage-all --push
```

This will:
- Stage all changes
- Generate an intelligent commit message
- Create the commit
- Push to remote

## Features

### 🔀 Intelligent Squash Merge (`intelligent_squash_merge.py`)

- **Pattern Recognition**: Automatically groups commits by type (fixes, features, documentation, tests, refactoring)
- **Interactive Mode**: Review and choose what to squash
- **Automated Mode**: Apply intelligent squashing automatically
- **Branch Merging**: Squash merge between branches with smart commit messages
- **Safe Operations**: Dry-run mode to preview changes

### 🔧 Repository Optimizer (`repo_optimizer.py`)

- **Duplicate Detection**: Find duplicate files using SHA256 hashing
- **Large File Analysis**: Identify files consuming significant space
- **Stale Branch Detection**: Find branches that haven't been updated
- **Git Object Optimization**: Optimize the git object database
- **Coverage Checking**: Ensure .gitignore is properly configured
- **Detailed Reports**: JSON reports with actionable insights

### 📝 Commit Push Manager (`commit_push_manager.py`)

- **Smart Messages**: Auto-generate commit messages from changes
- **Validation**: Pre-commit message and change validation
- **Multi-Remote**: Support for multiple git remotes
- **Synchronization**: Sync local and remote branches
- **Conflict Detection**: Identify and help resolve conflicts
- **Status Overview**: Detailed repository status display

## Installation

No installation required! Just clone the repository and use Python 3.6+:

```bash
git clone https://github.com/HeadyMe/HeadyConnection.git
cd HeadyConnection
python3 scripts/repo_optimizer.py --help
```

## Documentation

Detailed documentation is available in:
- [`scripts/README.md`](scripts/README.md) - Complete script documentation and examples
- Each script has `--help` flag for quick reference

## Common Use Cases

### Clean Up Before Release

```bash
# Analyze repository
python3 scripts/repo_optimizer.py --analyze

# Squash feature commits
python3 scripts/intelligent_squash_merge.py --auto --commits 20

# Optimize git database
python3 scripts/repo_optimizer.py --optimize --auto

# Commit and push
python3 scripts/commit_push_manager.py --message "Prepare v2.0 release" --push
```

### Daily Development Workflow

```bash
# Check status
python3 scripts/commit_push_manager.py --status

# Commit with auto-message
python3 scripts/commit_push_manager.py --auto-message --stage-all --push

# Sync with remote
python3 scripts/commit_push_manager.py --sync
```

### Repository Maintenance

```bash
# Find what's taking up space
python3 scripts/repo_optimizer.py --find-large-files 5

# Find duplicate files
python3 scripts/repo_optimizer.py --find-duplicates

# Clean up old branches
python3 scripts/repo_optimizer.py --clean-branches --days 90
```

## Best Practices

1. **Always use --dry-run first** when learning new commands
2. **Review generated reports** before taking action
3. **Keep backups** of important branches
4. **Run optimizations regularly** (weekly or monthly)
5. **Use meaningful commit messages** even with auto-generation

## Requirements

- Python 3.6 or higher
- Git 2.0 or higher
- No external Python packages required (uses standard library only)

## Safety Features

All scripts include:
- ✅ Dry-run mode for safe preview
- ✅ Input validation
- ✅ Error handling and recovery
- ✅ Detailed operation logging
- ✅ Confirmation prompts for destructive operations

## Examples

### Example 1: Merge Feature Branch

```bash
# Squash merge with intelligent commit grouping
python3 scripts/intelligent_squash_merge.py \
    --branch feature/authentication \
    --target main

# Push the result
python3 scripts/commit_push_manager.py --push
```

### Example 2: Optimize Repository

```bash
# Run full analysis
python3 scripts/repo_optimizer.py --analyze

# Review the optimization_report.json
cat optimization_report.json

# Apply automatic optimizations
python3 scripts/repo_optimizer.py --optimize --auto
```

### Example 3: Quick Commit and Push

```bash
# One-liner: stage, commit with auto-message, and push
python3 scripts/commit_push_manager.py --auto-message --stage-all --push
```

## Contributing

When contributing to this repository:

1. Test changes with `--dry-run` first
2. Run the optimizer to ensure code quality
3. Use the commit manager for consistent commits
4. Follow the established patterns in existing scripts

## Troubleshooting

### Common Issues

**"Not a git repository"**
- Ensure you're in a git repository or use `--repo-path`

**"No staged changes"**
- Stage files first: `git add .` or use `--stage-all`

**"Permission denied"**
- Make scripts executable: `chmod +x scripts/*.py`

### Getting Help

```bash
# Each script has detailed help
python3 scripts/intelligent_squash_merge.py --help
python3 scripts/repo_optimizer.py --help
python3 scripts/commit_push_manager.py --help
```

## Project Structure

```
HeadyConnection/
├── scripts/
│   ├── intelligent_squash_merge.py   # Squash merge operations
│   ├── repo_optimizer.py             # Repository optimization
│   ├── commit_push_manager.py        # Commit/push management
│   └── README.md                     # Detailed documentation
├── HeadyDirective/                   # Directive files
├── HeadySystems/                     # Systems components
└── REPO_MANAGEMENT.md                # This file
```

## License

This project is part of the HeadyConnection repository. See [LICENSE](HeadyDirective/LICENSE) for details.

## Support

For issues, questions, or suggestions:
1. Check the documentation in `scripts/README.md`
2. Use `--help` on individual scripts
3. Review generated reports
4. Open an issue on GitHub

---

**Made with ❤️ for better git workflows**
