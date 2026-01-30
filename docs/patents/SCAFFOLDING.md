# Patent Draft Scaffolding

Use this guide when staging a new provisional application that is not yet ready for legal review.

## When to Use
- The system name is not finalized.
- The core concept exists but requires additional technical detail.
- Counsel review is pending and you need a tracked placeholder.

## How to Scaffold
1. Run the scaffold helper to generate a placeholder IDF and DOCX:
   ```bash
   python3 scripts/patents/scaffold_patent.py --id 041 --slug example-system --title "Example System" --date 2026-01-22
   ```
2. Update `docs/patents/INVENTION_DISCLOSURE_INDEX.md` and `docs/patents/PROVISIONAL_LINKS.md` with the new files.
3. Add the entry to `docs/patents/FILING_QUEUE.md` with a short description.
4. Replace all bracketed placeholder fields before counsel review.

## Compliance Notes
- Do not include investment promises or legal conclusions.
- Keep compliance-first language in any token-related drafts.
