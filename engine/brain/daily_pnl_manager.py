from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime, date
import json
from sqlalchemy.orm import Session
from engine.database.models import DailyCycleLog, ControlFlag, PortfolioSnapshot

class CapitalState(Enum):
    NORMAL_OPERATION = "NORMAL_OPERATION"
    RECOVERY_MODE = "RECOVERY_MODE"
    COMPOUNDING_MODE = "COMPOUNDING_MODE"
    SOFT_HALT = "SOFT_HALT"
    HARD_HALT = "HARD_HALT"
    EMERGENCY_HALT = "EMERGENCY_HALT"
    CAPITAL_PRESERVATION = "CAPITAL_PRESERVATION"
    OPPORTUNITY_SURGE = "OPPORTUNITY_SURGE"
    EXCEPTIONAL_DAY = "EXCEPTIONAL_DAY"

@dataclass
class DailyTargetConfig:
    starting_capital: float
    min_target_usd: float
    ideal_target_usd: float
    stretch_target_usd: float
    soft_halt_usd: float
    hard_halt_usd: float
    emergency_halt_usd: float
    profit_lock_trigger_usd: float
    source: str  # "DYNAMIC_PCT" | "OVERRIDE_PCT" | "OVERRIDE_USD"
    override_note: Optional[str] = None

class DailyPnLManager:
    def __init__(self, db: Session, settings: dict):
        self.db = db
        self.settings = settings
        self.current_state = CapitalState.NORMAL_OPERATION
        self.config: Optional[DailyTargetConfig] = None
        self.profit_lock_floor = 0.0
        self.recovery_days_used = 0
        self.compounding_streak = 0

    def initialize_day(self, starting_capital: float):
        # Check for overrides in control_flags
        override_usd = self._get_control_flag("target_override_usd")
        override_pct = self._get_control_flag("target_override_pct")

        cap_settings = self.settings.get('capital', {})

        if override_usd:
            source = "OVERRIDE_USD"
            min_target = float(override_usd)
            # For simplicity, we scale other targets based on the ratio if override_usd is set
            # But the spec says "Use exact dollar value" for target_override_usd.
            # Assuming it overrides the min_profit_target.
            ratio = min_target / (starting_capital * cap_settings.get('min_profit_target_pct', 1.5) / 100)
            ideal_target = (starting_capital * cap_settings.get('ideal_profit_target_pct', 3.0) / 100) * ratio
            stretch_target = (starting_capital * cap_settings.get('stretch_profit_target_pct', 5.0) / 100) * ratio
        elif override_pct:
            source = "OVERRIDE_PCT"
            pct = float(override_pct) / 100
            min_target = starting_capital * pct
            ideal_target = starting_capital * (cap_settings.get('ideal_profit_target_pct', 3.0) / 100) * (pct / (cap_settings.get('min_profit_target_pct', 1.5) / 100))
            stretch_target = starting_capital * (cap_settings.get('stretch_profit_target_pct', 5.0) / 100) * (pct / (cap_settings.get('min_profit_target_pct', 1.5) / 100))
        else:
            source = "DYNAMIC_PCT"
            min_target = starting_capital * (cap_settings.get('min_profit_target_pct', 1.5) / 100)
            ideal_target = starting_capital * (cap_settings.get('ideal_profit_target_pct', 3.0) / 100)
            stretch_target = starting_capital * (cap_settings.get('stretch_profit_target_pct', 5.0) / 100)

        self.config = DailyTargetConfig(
            starting_capital=starting_capital,
            min_target_usd=min_target,
            ideal_target_usd=ideal_target,
            stretch_target_usd=stretch_target,
            soft_halt_usd=starting_capital * (cap_settings.get('soft_halt_loss_pct', 1.5) / 100),
            hard_halt_usd=starting_capital * (cap_settings.get('hard_halt_loss_pct', 3.0) / 100),
            emergency_halt_usd=starting_capital * (cap_settings.get('emergency_halt_loss_pct', 5.0) / 100),
            profit_lock_trigger_usd=ideal_target * (cap_settings.get('profit_lock_trigger_pct', 20.0) / 100),
            source=source
        )

        # Log to daily_cycle_log
        log_entry = DailyCycleLog(
            cycle_date=datetime.utcnow().date(),
            starting_capital=starting_capital,
            cycle_state=self.current_state.value,
            notes=f"Initialized with {source}"
        )
        # Using merge or checking if exists for the day
        existing = self.db.query(DailyCycleLog).filter(DailyCycleLog.cycle_date == datetime.utcnow().date()).first()
        if existing:
            existing.starting_capital = starting_capital
            existing.cycle_state = self.current_state.value
        else:
            self.db.add(log_entry)
        self.db.commit()

    def _get_control_flag(self, key: str) -> str:
        flag = self.db.query(ControlFlag).filter(ControlFlag.flag_key == key).first()
        return flag.flag_value if flag else ""

    def update_state(self, current_equity: float):
        if not self.config:
            return

        pnl = current_equity - self.config.starting_capital
        pnl_pct = (pnl / self.config.starting_capital) * 100 if self.config.starting_capital else 0

        cap_settings = self.settings.get('capital', {})

        # Check for halts
        if pnl <= -self.config.emergency_halt_usd:
            self.current_state = CapitalState.EMERGENCY_HALT
        elif pnl <= -self.config.hard_halt_usd:
            self.current_state = CapitalState.HARD_HALT
        elif pnl <= -self.config.soft_halt_usd:
            if self.current_state == CapitalState.NORMAL_OPERATION:
                self.current_state = CapitalState.SOFT_HALT

        # Exceptional day
        if pnl_pct >= cap_settings.get('exceptional_day_pct', 7.5):
            self.current_state = CapitalState.EXCEPTIONAL_DAY

        # Update profit lock
        self.lock_in_profits(current_equity)

    def lock_in_profits(self, current_equity: float):
        if not self.config: return
        pnl = current_equity - self.config.starting_capital
        if pnl >= self.config.profit_lock_trigger_usd:
            cap_settings = self.settings.get('capital', {})
            # Lock 60% of gains above trigger
            gains_above_trigger = pnl - self.config.profit_lock_trigger_usd

            protect_pct = cap_settings.get('profit_protect_pct', 0.60)
            if pnl >= 2 * self.config.ideal_target_usd:
                protect_pct = cap_settings.get('profit_lock_step2_pct', 0.70)

            locked_amount = gains_above_trigger * protect_pct
            new_floor = self.config.starting_capital + self.config.profit_lock_trigger_usd + locked_amount
            self.profit_lock_floor = max(self.profit_lock_floor, new_floor)

    def settle_regular_session(self, current_equity: float):
        if not self.config: return
        pnl = current_equity - self.config.starting_capital

        log = self.db.query(DailyCycleLog).filter(DailyCycleLog.cycle_date == datetime.utcnow().date()).first()
        if log:
            log.preliminary_pnl = pnl
            log.settlement_timestamp_preliminary = datetime.utcnow()
        self.db.commit()

    def settle_final(self, current_equity: float):
        if not self.config: return
        final_pnl = current_equity - self.config.starting_capital

        log = self.db.query(DailyCycleLog).filter(DailyCycleLog.cycle_date == datetime.utcnow().date()).first()
        preliminary_pnl = log.preliminary_pnl if log and log.preliminary_pnl else 0.0

        if log:
            log.final_pnl = final_pnl
            log.after_hours_pnl = final_pnl - preliminary_pnl
            log.ending_equity = current_equity
            log.daily_pnl_pct = (final_pnl / self.config.starting_capital) * 100
            log.settlement_timestamp_final = datetime.utcnow()

            # Profit extraction
            if final_pnl > self.config.min_target_usd:
                log.profit_extracted = final_pnl - self.config.min_target_usd
                # Update profit_wallet cumulative (simplified)
                # In a real app, we'd query the last wallet entry

            # State transitions for next day
            if final_pnl < 0:
                self.current_state = CapitalState.RECOVERY_MODE
                self.compounding_streak = 0
            elif final_pnl >= self.config.min_target_usd:
                self.compounding_streak += 1
                if self.compounding_streak >= self.settings.get('capital', {}).get('compounding_streak_days', 5):
                    self.current_state = CapitalState.COMPOUNDING_MODE
                else:
                    self.current_state = CapitalState.NORMAL_OPERATION
            else:
                self.current_state = CapitalState.NORMAL_OPERATION

        self.db.commit()
