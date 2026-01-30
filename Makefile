.PHONY: dev-bootstrap governance-install governance-hooks docs-validate docs-drift docs-site-build docs-site-serve docs-living-federation-validate docs-heady-music-validate docs-heady-iterations-validate docs-genesis-validate headycoin-seed status-feed-validate heady-lens-validate admin-ui-validate patent-validate receipts-validate branch-consolidate-plan governance-lock-validate heady-kinetic-validate pops-oracle-validate heady-project-validate heady-symphony-validate

dev-bootstrap:
	bash scripts/dev/bootstrap_ddev.sh

governance-install:
	bash scripts/governance/install_policy_pack.sh

governance-hooks:
	bash scripts/governance/install_git_hooks.sh

docs-validate:
	python3 scripts/docs/validate_docs.py

docs-drift:
	python3 scripts/docs/check_drift.py --base HEAD~1 --head HEAD

docs-living-federation-validate:
	python3 scripts/docs/validate_living_federation.py

docs-heady-music-validate:
	python3 scripts/docs/validate_heady_music_symphony.py

docs-heady-iterations-validate:
	python3 scripts/docs/validate_heady_iterations.py

docs-genesis-validate:
	python3 scripts/docs/validate_genesis_dashboard.py

docs-site-build:
	mkdocs build --strict

docs-site-serve:
	mkdocs serve

headycoin-seed:
	drush heady-coin:seed

status-feed-validate:
	python3 scripts/ops/validate_status_feed.py ops/compose/status/system.json.example

heady-lens-validate:
	python3 scripts/web/validate_heady_lens.py

admin-ui-validate:
	python3 scripts/web/validate_heady_admin_ui.py

patent-validate:
	python3 scripts/patents/validate_patent_index.py

receipts-validate:
	python3 scripts/ops/validate_receipts.py ops/receipts/receipts.jsonl

branch-consolidate-plan:
	python3 scripts/dev/branch_consolidate.py --repo . --branches $(BRANCHES) --output branch_plan.json --allow-single

governance-lock-validate:
	python3 scripts/governance/validate_governance_lock.py

heady-kinetic-validate:
	python3 scripts/ops/validate_heady_kinetic.py

pops-oracle-validate:
	python3 scripts/crypto/validate_pops_oracle.py crypto/pops_oracle/sample_payload.json

heady-project-validate:
	python3 scripts/ops/validate_heady_project.py

heady-symphony-validate:
	python3 scripts/ops/validate_heady_symphony.py
