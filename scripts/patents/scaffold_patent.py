#!/usr/bin/env python3
"""Scaffold a placeholder patent application (DOCX) + IDF entry.

Usage:
  python3 scripts/patents/scaffold_patent.py \
    --id 041 \
    --slug example-system \
    --title "Example System" \
    --date 2026-01-22
"""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def build_docx(paragraphs: list[str], output: Path) -> None:
    body = []
    for para in paragraphs:
        body.append(f"    <w:p><w:r><w:t>{escape(para)}</w:t></w:r></w:p>")

    document_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
{body}
  </w:body>
</w:document>
""".format(body="\n".join(body))

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
"""

    rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels_xml)
        z.writestr("word/document.xml", document_xml)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a patent placeholder.")
    parser.add_argument("--id", required=True, help="Patent application number, e.g., 041")
    parser.add_argument("--slug", required=True, help="Slug for IDF filename")
    parser.add_argument("--title", required=True, help="Short system title")
    parser.add_argument("--date", default="2026-01-22", help="Filing date (YYYY-MM-DD)")
    args = parser.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit("--date must be in YYYY-MM-DD format") from exc

    idf_path = ROOT / "docs/patents/invention_disclosures" / f"IDF-{args.date.replace('-', '')}-00-{args.slug}.md"
    docx_path = ROOT / "docs/patents/provisional" / f"HS-PA-{args.id}_{args.title.replace(' ', '')}_{args.date}.docx"

    idf_content = f"""# IDF-{args.date.replace('-', '')}-00: {args.title}

## Problem
[INSERT PROBLEM STATEMENT]

## Prior Approaches (High Level)
- [INSERT PRIOR APPROACH 1]
- [INSERT PRIOR APPROACH 2]

## Inventive Concept
[INSERT INVENTIVE CONCEPT]

## Key Differentiators
- [INSERT DIFFERENTIATOR 1]
- [INSERT DIFFERENTIATOR 2]

## Technical Details
- [INSERT TECHNICAL DETAIL 1]
- [INSERT TECHNICAL DETAIL 2]

## Alternative Embodiments
- [INSERT ALTERNATIVE 1]
- [INSERT ALTERNATIVE 2]

## Benefits
- [INSERT BENEFIT 1]
- [INSERT BENEFIT 2]

## Potential Claim Themes
- [INSERT CLAIM THEME 1]
- [INSERT CLAIM THEME 2]

## Notes
- Assignee: HeadySystems Inc.
- Inventor: Eric Haywood
- Date: {args.date}
- Attorney Docket: HS-PPA-{args.id} (placeholder)
"""

    docx_paragraphs = [
        f"Patent Application {args.id}: {args.title}",
        "[INSERT FULL TITLE]",
        "",
        "Assignee: HeadySystems Inc.",
        "Inventor: Eric Haywood",
        f"Date: {args.date}",
        "",
        "Specification",
        "",
        "Abstract",
        "[0001] [INSERT ABSTRACT — 150–250 words. Describe the system, key components, and primary advantage.]",
        "",
        "Technical Field",
        "[0002] [INSERT TECHNICAL FIELD — e.g., distributed systems; AI governance; security; cryptography; etc.]",
        "",
        "Background",
        "[0003] [INSERT BACKGROUND — describe existing approaches and shortcomings.]",
        "[0004] [INSERT PROBLEM STATEMENT — what is broken/inefficient/unsafe today?]",
        "",
        "Summary",
        "[0005] [INSERT SUMMARY — high-level description of invention; how it solves the problem.]",
        "[0006] [INSERT SUMMARY CONT. — list major modules/features and primary benefits.]",
        "",
        "Brief Description of the Drawings",
        "[0007] FIG. 1 is a conceptual block diagram of an example system architecture according to the present disclosure.",
        "",
        "FIG. 1",
        "",
        "Definitions",
        "[0008] [DEFINE key term 1.]",
        "[0009] [DEFINE key term 2.]",
        "[0010] [DEFINE key term 3.]",
        "",
        "System Overview",
        "[0011] [INSERT SYSTEM OVERVIEW — components, interfaces, data flows.]",
        "[0012] [INSERT SECURITY/SAFETY/GOVERNANCE NOTE — if applicable.]",
        "",
        "Detailed Description",
        "[0013] [INSERT DETAILED DESCRIPTION — module A, module B, module C.]",
        "[0014] [INSERT DATA MODELS / PROTOCOLS — schemas, message formats, receipts, etc.]",
        "[0015] [INSERT OPERATIONAL FLOW — step-by-step method.]",
        "",
        "Example Embodiments",
        "[0016] [INSERT EMBODIMENT 1 — example deployment/use case.]",
        "[0017] [INSERT EMBODIMENT 2 — alternative configuration.]",
        "",
        "Advantages",
        "[0018] [INSERT ADVANTAGES — quantify improvements when possible: speed, security, cost, reliability, safety.]",
        "",
        "Exemplary Claim Concepts (Non-Limiting)",
        "[0019] [INSERT CLAIM CONCEPT 1 — system claim.]",
        "[0020] [INSERT CLAIM CONCEPT 2 — method claim.]",
        "[0021] [INSERT CLAIM CONCEPT 3 — non-transitory computer-readable medium claim.]",
        "",
        "Conclusion",
        "[0022] The foregoing description is provided to enable a person skilled in the art to make and use the disclosed invention and is not intended to limit the scope of the invention to the embodiments described.",
    ]

    idf_path.parent.mkdir(parents=True, exist_ok=True)
    idf_path.write_text(idf_content, encoding="utf-8")
    build_docx(docx_paragraphs, docx_path)

    print(f"Created {idf_path}")
    print(f"Created {docx_path}")


if __name__ == "__main__":
    main()
