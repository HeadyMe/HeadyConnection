#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATENTS_ROOT = ROOT / "docs" / "patents"
IDF_DIR = PATENTS_ROOT / "invention_disclosures"
PROVISIONAL_DIR = PATENTS_ROOT / "provisional"
IDF_INDEX = PATENTS_ROOT / "INVENTION_DISCLOSURE_INDEX.md"
PROVISIONAL_LINKS = PATENTS_ROOT / "PROVISIONAL_LINKS.md"
FILING_QUEUE = PATENTS_ROOT / "FILING_QUEUE.md"

IDF_LINK_RE = re.compile(r"\((docs/patents/invention_disclosures/[^)]+)\)")
PROVISIONAL_LINK_RE = re.compile(r"\((docs/patents/provisional/[^)]+\.docx)\)")


def load_links(path: Path, pattern: re.Pattern[str]) -> set[str]:
    content = path.read_text(encoding="utf-8")
    return set(match.group(1) for match in pattern.finditer(content))


def main() -> int:
    missing = []

    idf_files = {f"docs/patents/invention_disclosures/{path.name}" for path in IDF_DIR.glob("*.md")}
    idf_links = load_links(IDF_INDEX, IDF_LINK_RE)

    missing_idfs = idf_files - idf_links
    if missing_idfs:
        missing.append(f"Missing IDFs in index: {', '.join(sorted(missing_idfs))}")

    extra_idfs = idf_links - idf_files
    if extra_idfs:
        missing.append(f"Index references missing IDFs: {', '.join(sorted(extra_idfs))}")

    provisional_files = {f"docs/patents/provisional/{path.name}" for path in PROVISIONAL_DIR.glob("*.docx")}
    provisional_links = load_links(PROVISIONAL_LINKS, PROVISIONAL_LINK_RE)

    missing_provisionals = provisional_files - provisional_links
    if missing_provisionals:
        missing.append(f"Missing provisional links: {', '.join(sorted(missing_provisionals))}")

    extra_provisionals = provisional_links - provisional_files
    if extra_provisionals:
        missing.append(f"Provisional links reference missing files: {', '.join(sorted(extra_provisionals))}")

    filing_queue_text = FILING_QUEUE.read_text(encoding="utf-8")
    for provisional in provisional_files:
        match = re.search(r"(HS-PA-\d{3})", provisional)
        if match and match.group(1) not in filing_queue_text:
            missing.append(f"Filing queue missing entry for {match.group(1)}")

    if missing:
        for item in missing:
            print(item)
        return 1

    print("Patent index validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
