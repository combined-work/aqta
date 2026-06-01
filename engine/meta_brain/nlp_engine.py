from typing import Dict, List, Optional
from dataclasses import dataclass
import enum
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class NLPTier(enum.IntEnum):
    TIER_1_LLM = 1
    TIER_2_SLM = 2
    TIER_3_DET = 3

@dataclass
class NLPResult:
    symbol: str
    sentiment_score: float # 0 to 100
    direction: str # BULLISH, BEARISH, NEUTRAL
    confidence: float # 0.0 to 1.0
    tier_used: NLPTier
    metadata: Dict

class NLPEngine:
    def __init__(self, config: dict):
        self.config = config
        self.vader = SentimentIntensityAnalyzer()
        self.llm_mode = config.get("nlp", {}).get("llm_mode", "DISABLED")

    def analyze_news(self, symbol: str, headlines: List[str]) -> NLPResult:
        # Tier 1 & 2 placeholders
        if self.llm_mode != "DISABLED":
            # Attempt Tier 1 or 2
            pass

        # Tier 3 Fallback
        return self._tier3_vader(symbol, headlines)

    def _tier3_vader(self, symbol: str, headlines: List[str]) -> NLPResult:
        combined_text = " ".join(headlines)
        scores = self.vader.polarity_scores(combined_text)
        compound = scores['compound'] # -1 to 1

        # Map -1..1 to 0..100
        sentiment_score = (compound + 1) * 50

        if compound > 0.5:
            direction = "BULLISH"
        elif compound < -0.5:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"

        return NLPResult(
            symbol=symbol,
            sentiment_score=sentiment_score,
            direction=direction,
            confidence=0.6, # Tier 3 fixed confidence
            tier_used=NLPTier.TIER_3_DET,
            metadata={"vader_scores": scores}
        )
