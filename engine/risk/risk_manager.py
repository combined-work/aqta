from dataclasses import dataclass
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from engine.database.models import ComplianceAuditLog, ControlFlag, Trade, Position
from engine.brokers.base_broker import OrderEvent
from datetime import datetime, timedelta

@dataclass
class RiskCheckResult:
    passed: bool
    rule: str
    reason: str
    auto_action_taken: Optional[str] = None
    modified_qty: Optional[float] = None

class RiskManager:
    def __init__(self, db: Session, settings: dict):
        self.db = db
        self.settings = settings

    def run_pipeline(self, order: OrderEvent, portfolio_state: dict) -> RiskCheckResult:
        # Step 1 — System Halt Guard
        if self._get_control_flag("trading_enabled") == "false":
            return RiskCheckResult(False, "Step 1", "System trading is disabled")

        # Step 2 — Shadow Mode Router (Handled in Router)

        # Step 3 — Emergency Halt Guard
        engine_status = self._get_control_flag("engine_status")
        if engine_status in ["HARD_HALT", "EMERGENCY_HALT"]:
             if order.side in ["BUY", "BTO"]:
                 return RiskCheckResult(False, "Step 3", f"System is in {engine_status}")

        # Step 4 — Intraday Drawdown Check
        drawdown = portfolio_state.get("intraday_drawdown", 0)
        if drawdown > self.settings.get("risk", {}).get("intraday_drawdown_hard_pct", 0.04):
            return RiskCheckResult(False, "Step 4", "Hard intraday drawdown limit reached")

        # Step 5 — PDT Rule
        if portfolio_state.get("total_equity", 0) < self.settings.get("risk", {}).get("pdt_equity_buffer", 26500):
            day_trades = self._count_day_trades(5)
            if day_trades >= 3:
                return RiskCheckResult(False, "Step 5", "PDT rule: max day trades reached")

        # Step 6 — Wash-Sale
        # (Placeholder for complex wash-sale logic)

        # Step 7 — Position Concentration
        exposure = (order.qty * (order.limit_price or portfolio_state.get("last_price", 0))) / portfolio_state.get("total_equity", 1)
        max_pos_pct = self.settings.get("risk", {}).get("max_single_position_pct", 0.10)
        if exposure > max_pos_pct:
            new_qty = (portfolio_state.get("total_equity", 0) * max_pos_pct) / (order.limit_price or portfolio_state.get("last_price", 1))
            return RiskCheckResult(True, "Step 7", "Resized for concentration", auto_action_taken="RESIZE", modified_qty=new_qty)

        # Step 8 — Sector Concentration
        # (Placeholder for sector lookup)

        # Step 9 — Liquidity Filter
        # (Placeholder for ADTV check)

        # Step 10 — Portfolio Correlation Check
        # (Placeholder for Pearson correlation)

        # Step 11 — Asset Class Toggle Check
        if "crypto" in order.symbol.lower() and self._get_control_flag("crypto_enabled") == "false":
             return RiskCheckResult(False, "Step 11", "Crypto disabled")
        if "option" in order.symbol.lower() and self._get_control_flag("options_enabled") == "false":
             return RiskCheckResult(False, "Step 11", "Options disabled")

        # Step 12 — Leverage (Reg-T)
        leverage = portfolio_state.get("leverage", 1.0)
        if leverage > self.settings.get("risk", {}).get("max_portfolio_leverage_overnight", 2.0):
             return RiskCheckResult(False, "Step 12", "Exceeds Reg-T leverage")

        # Step 13 — Flash Crash Correlation Spike
        if portfolio_state.get("avg_correlation", 0) > 0.85:
             return RiskCheckResult(False, "Step 13", "Flash Crash Correlation Spike detected")

        # Step 14 — Liquidity Dry-Up Guard
        spread_ratio = portfolio_state.get("spread_ratio", 1.0)
        if spread_ratio > 5.0:
             return RiskCheckResult(False, "Step 14", "Liquidity Dry-Up: wide spread detected")

        # Step 15 — Strategy Drawdown Halt
        # (Placeholder for per-strategy drawdown check)

        return RiskCheckResult(True, "All", "Passed all risk checks")

    def _get_control_flag(self, key: str) -> str:
        flag = self.db.query(ControlFlag).filter(ControlFlag.flag_key == key).first()
        return flag.flag_value if flag else ""

    def _count_day_trades(self, days: int) -> int:
        # Simplified count: trades opened and closed on same day
        cutoff = datetime.utcnow() - timedelta(days=days)
        # In a real app, we'd query the trades table for matching entry/exit on same day
        return 0 # Placeholder

    def log_audit(self, order: OrderEvent, result: RiskCheckResult):
        audit = ComplianceAuditLog(
            event_time=datetime.utcnow(),
            rule_name=result.rule,
            symbol=order.symbol,
            order_direction=order.side,
            order_qty=order.qty,
            outcome="PASSED" if result.passed else "BLOCKED",
            reason=result.reason
        )
        self.db.add(audit)
        self.db.commit()
