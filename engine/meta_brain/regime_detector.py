import numpy as np
from hmmlearn import hmm
import pandas as pd
from typing import Tuple, List

class RegimeDetector:
    def __init__(self, n_components: int = 6):
        self.model = hmm.GaussianHMM(n_components=n_components, covariance_type="full", n_iter=1000)
        self.is_trained = False
        self.regime_names = [
            "BULL_TREND", "BEAR_TREND", "SIDEWAYS_LOW",
            "SIDEWAYS_HIGH", "CRASH_RISK", "RECOVERY"
        ]

    def train(self, df: pd.DataFrame):
        # Features: [daily_return, log_volume, vix_norm, atr_norm]
        # In this mock/initial version, we'll use returns and volatility
        df['returns'] = df['Close'].pct_change()
        df['range'] = (df['High'] - df['Low']) / df['Close']
        features = df[['returns', 'range']].dropna().values

        self.model.fit(features)
        self.is_trained = True

    def predict_regime(self, current_data: np.ndarray) -> Tuple[str, np.ndarray]:
        if not self.is_trained:
            return "UNKNOWN", np.array([])

        # Predict state
        state = self.model.predict(current_data.reshape(1, -1))[0]
        probs = self.model.predict_proba(current_data.reshape(1, -1))[0]

        regime_name = self.regime_names[state] if state < len(self.regime_names) else f"STATE_{state}"
        return regime_name, probs
