import numpy as np
from typing import Dict, Tuple

class ContextualThompsonSampler:
    def __init__(self, strategies: List[str]):
        # Each (strategy, regime) pair has Beta(alpha, beta)
        # For simplicity, we'll start with just strategy-level stats
        self.stats = {s: {"alpha": 1.0, "beta": 1.0} for s in strategies}

    def update(self, strategy_id: str, pnl: float):
        if strategy_id not in self.stats: return

        if pnl > 0:
            self.stats[strategy_id]["alpha"] += 1
        else:
            self.stats[strategy_id]["beta"] += 1

    def get_weights(self) -> Dict[str, float]:
        samples = {}
        for s, params in self.stats.items():
            samples[s] = np.random.beta(params["alpha"], params["beta"])

        # Normalize
        total = sum(samples.values())
        if total == 0: return {s: 1.0/len(self.stats) for s in self.stats}

        return {s: v/total for s, v in samples.items()}
