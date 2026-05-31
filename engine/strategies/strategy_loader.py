import importlib
import pkgutil
from typing import List, Dict
from engine.strategies.base_strategy import BaseStrategy
from engine.database.models import StrategyPerformance
from sqlalchemy.orm import Session

class StrategyLoader:
    def __init__(self, db: Session):
        self.db = db
        self.strategies: Dict[str, BaseStrategy] = {}

    def load_all(self):
        # Dynamically load from directories
        # For now, manually add the ones we implemented
        from engine.strategies.equity.momentum.eq01_trend_following import EQ01TrendFollowing
        from engine.strategies.equity.momentum.a_batch import A1ORB, A2VWAPMomo

        instances = [EQ01TrendFollowing(), A1ORB(), A2VWAPMomo()]
        for inst in instances:
            self.strategies[inst.strategy_id] = inst
            self._sync_db(inst)

    def _sync_db(self, strategy: BaseStrategy):
        perf = self.db.query(StrategyPerformance).filter(StrategyPerformance.strategy_id == strategy.strategy_id).first()
        if not perf:
            perf = StrategyPerformance(
                strategy_id=strategy.strategy_id,
                display_name=strategy.name,
                is_enabled=strategy.is_enabled
            )
            self.db.add(perf)
            self.db.commit()

    def get_enabled_strategies(self) -> List[BaseStrategy]:
        enabled_ids = [s.strategy_id for s in self.db.query(StrategyPerformance).filter(StrategyPerformance.is_enabled == True).all()]
        return [self.strategies[sid] for sid in enabled_ids if sid in self.strategies]
