from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from engine.database.models import TaxLot, WashSaleBlacklist
import enum

class LotMethod(enum.StrEnum):
    FIFO = "FIFO"
    HIFO = "HIFO"
    LTCG_FIRST = "LTCG_FIRST"
    LOSS_FIRST = "LOSS_FIRST"

class TaxEngine:
    def __init__(self, db: Session, settings: dict):
        self.db = db
        self.settings = settings

    def select_lot_method(self, symbol: str, portfolio_state: dict) -> LotMethod:
        # Default logic
        if self.settings.get("tax", {}).get("tlh_enabled", True):
             return LotMethod.LOSS_FIRST
        return LotMethod.FIFO

    def harvest_losses(self):
        # Scan for lots with unrealized losses > threshold
        threshold = self.settings.get("tax", {}).get("tlh_min_loss_threshold", -500.0)

        loss_lots = self.db.query(TaxLot).filter(
            TaxLot.is_closed == False,
            TaxLot.realized_gain_loss < threshold
        ).all()

        for lot in loss_lots:
            # Execute TLH: Sell lot, add to blacklist
            pass
