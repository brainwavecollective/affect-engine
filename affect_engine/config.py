from dataclasses import dataclass
from pathlib import Path


@dataclass
class AffectConfig:
    """
    Configuration for AffectEngine.

    All tuning parameters live here.
    Mutate before calling engine.start().
    """

    # ---------------------------------------------------------
    # Core Emotional Tuning
    # ---------------------------------------------------------

    passion: float = 2.25
    drama: float = 0.65

    default_influence: float = 0.22
    baseline_influence: float = 0.70

    dwell_seconds: float = 1.2
    hold_seconds: float = 0.8
    decay_rate: float = 0.06

    tick_rate_hz: float = 10.0

    # ---------------------------------------------------------
    # Bounds
    # ---------------------------------------------------------

    min_vadcc: float = 0.0
    max_vadcc: float = 1.0

    # ---------------------------------------------------------
    # NLP Models
    # ---------------------------------------------------------

    nrc_lexicon_path: str = "data/NRC-VAD-Lexicon-v2.1/NRC-VAD-Lexicon-v2.1.txt"
    sentence_model_name: str = "all-MiniLM-L6-v2"

    # ---------------------------------------------------------
    # Anchor (Slow Baseline)
    # ---------------------------------------------------------

    enable_anchor: bool = False
    anchor_model_name: str = "nemotron-mini:4b-instruct-q5_K_M"

    warm_baseline_on_start: bool = True
    baseline_window_words: int = 100

    # ---------------------------------------------------------
    # Context Tracking
    # ---------------------------------------------------------

    context_buffer_words: int = 200

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    debug: bool = False

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(self):

        if not (0.0 <= self.passion <= 5.0):
            raise ValueError("passion must be between 0 and 5")

        if not (0.0 <= self.drama <= 1.0):
            raise ValueError("drama must be between 0 and 1")

        if self.tick_rate_hz <= 0:
            raise ValueError("tick_rate_hz must be positive")

        if self.min_vadcc >= self.max_vadcc:
            raise ValueError("min_vadcc must be < max_vadcc")

        if not Path(self.nrc_lexicon_path).exists():
            raise FileNotFoundError(
                f"NRC lexicon not found at {self.nrc_lexicon_path}"
            )
