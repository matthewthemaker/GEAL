"""
GEAL — Glacier Emotion Artificial Life
=======================================
An engine that models, maps, and expands an emotional matrix based on
text, music metrics, and scientific literature.

Public API:
    EmotionVector    - geal.vector.EmotionVector
    AffectiveSpace   - geal.engine.AffectiveSpace
    LexiconExpansion - geal.learning.LexiconExpansion
    MusicMapper      - geal.crossmodal.MusicMapper
    MusicFeatures    - geal.crossmodal.MusicFeatures
"""

from .vector import EmotionVector
from .engine import AffectiveSpace
from .learning import LexiconExpansion
from .crossmodal import MusicMapper, MusicFeatures

__all__ = [
    "EmotionVector",
    "AffectiveSpace",
    "LexiconExpansion",
    "MusicMapper",
    "MusicFeatures",
]

__version__ = "0.1.0"
