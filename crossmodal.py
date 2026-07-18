"""
geal.vector
===========
Shared low-level data type used across the GEAL package.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from typing import Dict, Tuple


def clamp(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    """Clamp a scalar into [lo, hi]."""
    return max(lo, min(hi, x))


@dataclass
class EmotionVector:
    """
    A single emotion mapped onto continuous Valence-Arousal-Dominance space.

    Attributes:
        name: Canonical label for the emotion (e.g. "joy", "nostalgia").
        valence: Pleasure axis, range [-1.0, 1.0]. Negative = unpleasant,
            positive = pleasant.
        arousal: Activation axis, range [-1.0, 1.0]. Negative = calm/low
            energy, positive = excited/high energy.
        dominance: Control axis, range [-1.0, 1.0]. Negative = submissive /
            feeling controlled, positive = dominant / in control.
        source: Provenance tag ("baseline", "learned:text", "learned:paper",
            "crossmodal:music", ...) so the matrix stays auditable in Git
            diffs.
        confidence: Heuristic confidence in [0.0, 1.0] for learned entries.
            Baseline (literature-sourced) entries default to 1.0.
    """

    name: str
    valence: float
    arousal: float
    dominance: float
    source: str = "baseline"
    confidence: float = 1.0

    def __post_init__(self) -> None:
        self.name = self.name.strip().lower()
        self.valence = clamp(self.valence)
        self.arousal = clamp(self.arousal)
        self.dominance = clamp(self.dominance)
        self.confidence = clamp(self.confidence, 0.0, 1.0)

    def as_tuple(self) -> Tuple[float, float, float]:
        """Return the (V, A, D) coordinates as a plain tuple."""
        return (self.valence, self.arousal, self.dominance)

    def distance_to(self, other: "EmotionVector") -> float:
        """Euclidean distance between this vector and another, in VAD space."""
        v1, a1, d1 = self.as_tuple()
        v2, a2, d2 = other.as_tuple()
        return math.sqrt((v1 - v2) ** 2 + (a1 - a2) ** 2 + (d1 - d2) ** 2)

    def blend(self, other: "EmotionVector", weight: float) -> "EmotionVector":
        """
        Linearly interpolate this vector toward `other`.

        weight=0.0 returns self unchanged; weight=1.0 returns other's
        coordinates. Used to regularize freshly-learned emotions toward
        their nearest known neighbor.
        """
        weight = clamp(weight, 0.0, 1.0)
        return EmotionVector(
            name=self.name,
            valence=self.valence * (1 - weight) + other.valence * weight,
            arousal=self.arousal * (1 - weight) + other.arousal * weight,
            dominance=self.dominance * (1 - weight) + other.dominance * weight,
            source=self.source,
            confidence=self.confidence,
        )

    def to_dict(self) -> Dict[str, float | str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, float | str]) -> "EmotionVector":
        return cls(**data)  # type: ignore[arg-type]
