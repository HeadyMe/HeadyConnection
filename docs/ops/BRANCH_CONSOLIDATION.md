# Branch Consolidation Runbook (HeadyConnection/HeadySystems)

This runbook describes a safe, repeatable method for combining three branches while preserving auditability and minimizing merge conflicts.

## Method (High Level)
1. **Generate a consolidation plan** to select the most convergent base branch and identify conflict hotspots.
2. **Review overlap files** and pre-resolve contentious areas (shared services, shared docs, build files).
3. **Execute merges in an isolated worktree** to avoid destabilizing the active branch.
4. **Open a consolidation PR** with the plan output attached for review.

## Scripted Workflow

### 1) Plan the merge order
```bash
python3 scripts/dev/branch_consolidate.py \
  --repo /path/to/HeadyConnection/HeadySystems \
  --branches main staging feature \
  --output branch_plan.json
```

The plan includes:
- **base_branch**: the branch with the smallest delta from the others.
- **merge_order**: an ordered list of branches to reduce overlap conflicts.
- **overlap_files**: files changed by multiple branches (hotspots).

### 2) Execute merges in a temporary worktree
```bash
python3 scripts/dev/branch_consolidate.py \
  --repo /path/to/HeadyConnection/HeadySystems \
  --branches main staging feature \
  --execute
```

This creates a new branch named `combined/<timestamp>` that contains the merged history.

### 3) Review and submit
- Run local validation commands.
- Attach `branch_plan.json` to the PR for transparency.
- Document any manual conflict resolutions in the PR summary.

## Risk & Rollback
- **Risk:** Merge conflicts in shared files (schema, config, docs).
- **Mitigation:** Use the overlap list to pre-review hotspots.
- **Rollback:** Delete the consolidation branch and rerun with a different base or order.

## Validation
After consolidation, rerun standard repo checks, for example:
```bash
make docs-validate
make status-feed-validate
```
