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

    def harvest_losses(self, current_prices: dict):
        # Scan for lots with unrealized losses > threshold
        threshold = self.settings.get("tax", {}).get("tlh_min_loss_threshold", -500.0)
        marginal_rate = self.settings.get("tax", {}).get("marginal_tax_rate", 0.35)

        open_lots = self.db.query(TaxLot).filter(TaxLot.is_closed == False).all()

        for lot in open_lots:
            current_price = current_prices.get(lot.symbol)
            if not current_price: continue

            unrealized_pnl = (current_price - lot.cost_basis) * lot.qty
            if unrealized_pnl < threshold:
                # Opportunity Cost Check
                # saving = abs(unrealized_pnl) * marginal_rate
                # if saving > self._estimate_30d_opportunity_cost(lot.symbol):
                #     self._execute_harvest(lot)
                pass

    def _execute_harvest(self, lot: TaxLot):
        # 1. Generate SELL order
        # 2. Add to WashSaleBlacklist
        # 3. Log to TaxHarvestLog
        pass

    def generate_form_8949(self) -> str:
        """Returns CSV content for IRS Form 8949."""
        closed_lots = self.db.query(TaxLot).filter(TaxLot.is_closed == True).all()
        csv_lines = ["Description,Date Acquired,Date Sold,Proceeds,Cost,Adjustment,Gain/Loss"]
        for lot in closed_lots:
            line = f"{lot.symbol},{lot.acquisition_date},{lot.close_date},{lot.close_price*lot.qty},{lot.cost_basis*lot.qty},,{lot.realized_gain_loss}"
            csv_lines.append(line)
        return "\n".join(csv_lines)
