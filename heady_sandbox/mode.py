from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ModeController:
    mode: str = "Standard"

    def set_mode(self, new_mode: str) -> None:
        if new_mode not in {"Standard", "Clinical"}:
            raise ValueError("Invalid mode")
        self.mode = new_mode
