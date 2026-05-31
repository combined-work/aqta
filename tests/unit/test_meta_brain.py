import pytest
from engine.meta_brain.nlp_engine import NLPEngine, NLPTier

def test_nlp_vader_fallback():
    engine = NLPEngine({"nlp": {"llm_mode": "DISABLED"}})
    result = engine.analyze_news("AAPL", ["Apple stocks are soaring today!", "Great earnings report."])

    assert result.direction == "BULLISH"
    assert result.tier_used == NLPTier.TIER_3_DET
    assert result.sentiment_score > 50

def test_nlp_vader_bearish():
    engine = NLPEngine({"nlp": {"llm_mode": "DISABLED"}})
    result = engine.analyze_news("TSLA", ["Tesla shares plummet after disappointing delivery numbers.", "Bad news for investors."])

    assert result.direction == "BEARISH"
    assert result.sentiment_score < 50
