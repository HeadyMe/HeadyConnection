from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "heady_project" / "src"
sys.path.insert(0, str(SRC))

from throttle import ComputeThrottle, TaskIntent  # noqa: E402
from verticals.bio import EphemeralProcessor  # noqa: E402
from verticals.mint import TokenIssuer  # noqa: E402
from verticals.symphony import NarrativeToMIDI  # noqa: E402


class VerticalGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.throttle = ComputeThrottle()

    def test_symphony_governance(self) -> None:
        symphony = NarrativeToMIDI(self.throttle)
        result = symphony.render("Melancholy Rain")
        governance = result["governance"]
        self.assertEqual(governance["vertical"], "HeadySymphony")
        self.assertEqual(governance["intent"], TaskIntent.REALTIME_AUDIO.value)
        self.assertGreater(governance["usage_units"], 0)
        self.assertIn("notes", result["midi"])

    def test_bio_governance(self) -> None:
        bio = EphemeralProcessor(self.throttle)
        result = bio.process(b"sample")
        governance = result["governance"]
        self.assertEqual(governance["vertical"], "HeadyBio")
        self.assertEqual(governance["intent"], TaskIntent.EPHEMERAL_PROCESSING.value)
        self.assertGreater(governance["usage_units"], 0)
        self.assertEqual(result["payload_bytes"], 6)

    def test_mint_governance_and_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = Path(tmpdir) / "mint" / "ledger.jsonl"
            mint = TokenIssuer(self.throttle, ledger_path)
            result = mint.issue(12.5)
            governance = result["governance"]
            self.assertEqual(governance["vertical"], "HeadyMint")
            self.assertEqual(governance["intent"], TaskIntent.BACKGROUND_MINING.value)
            self.assertGreater(governance["usage_units"], 0)
            ledger_lines = ledger_path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(ledger_lines), 1)
            entry = json.loads(ledger_lines[0])
            self.assertIn("hash", entry)


if __name__ == "__main__":
    unittest.main()
