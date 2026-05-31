from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class ComplianceAuditLog(Base):
    __tablename__ = 'compliance_audit_log'
    id = Column(Integer, primary_key=True)
    event_time = Column(DateTime)
    rule_name = Column(String)
    symbol = Column(String)
    order_direction = Column(String)
    order_qty = Column(Float)
    outcome = Column(String) # BLOCKED/WARNED/PASSED
    reason = Column(String)
    strategy_id = Column(String)

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    asset_class = Column(String)  # EQUITY/OPTION/CRYPTO/ETF/CASH
    broker = Column(String)
    strategy_id = Column(String)
    direction = Column(String)  # BUY/SELL/BTO/STC
    qty = Column(Float)
    order_type = Column(String)
    limit_price = Column(Float)
    fill_price = Column(Float)
    commission = Column(Float)
    slippage_bps = Column(Float)
    status = Column(String)  # PENDING/FILLED/CANCELLED/REJECTED
    broker_order_id = Column(String)
    fill_timestamp = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    algo_type = Column(String)
    algo_params_json = Column(Text)
    settlement_session = Column(String)  # REGULAR | AFTER_HOURS

class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    asset_class = Column(String)
    broker = Column(String)
    current_qty = Column(Float)
    average_cost = Column(Float)
    last_price = Column(Float)
    unrealized_pl = Column(Float)
    unrealized_pl_pct = Column(Float)
    realized_pl = Column(Float)
    days_held = Column(Integer)
    strategy_id = Column(String)
    stop_price = Column(Float)
    take_profit_price = Column(Float)
    delta = Column(Float)
    theta = Column(Float)
    vega = Column(Float)
    gamma = Column(Float)
    rho = Column(Float)
    option_expiry = Column(DateTime)
    option_strike = Column(Float)
    option_type = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)
    portfolio_delta_contribution = Column(Float)
    iv_at_entry = Column(Float)
    iv_current = Column(Float)
    trailing_stop_pct = Column(Float)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    parent_trade_id = Column(Integer, ForeignKey('trades.id'))
    broker_order_id = Column(String)
    status = Column(String)
    fills_json = Column(Text)
    routing_reason = Column(String)
    latency_ms = Column(Float)
    venue_quotes_json = Column(Text)

class TaxLot(Base):
    __tablename__ = 'tax_lots'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    acquisition_date = Column(DateTime)
    qty = Column(Float)
    cost_basis = Column(Float)
    lot_method = Column(String)
    is_closed = Column(Boolean, default=False)
    close_date = Column(DateTime)
    close_price = Column(Float)
    realized_gain_loss = Column(Float)
    is_long_term = Column(Boolean)
    wash_sale_disallowed = Column(Boolean, default=False)
    amt_adjustment = Column(Float)
    asset_class = Column(String)

class WashSaleBlacklist(Base):
    __tablename__ = 'wash_sale_blacklist'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    loss_realized_date = Column(DateTime)
    expiration_date = Column(DateTime)
    loss_amount = Column(Float)
    proxy_used = Column(String)
    proxy_score = Column(Float)

class StrategyPerformance(Base):
    __tablename__ = 'strategy_performance'
    id = Column(Integer, primary_key=True)
    strategy_id = Column(String, unique=True)
    display_name = Column(String)
    asset_class = Column(String)
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    total_pnl = Column(Float, default=0.0)
    avg_hold_days = Column(Float, default=0.0)
    sharpe_ratio = Column(Float, default=0.0)
    sortino_ratio = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    profit_factor = Column(Float, default=0.0)
    current_weight = Column(Float, default=0.0)
    bandit_alpha = Column(Float, default=1.0)
    bandit_beta = Column(Float, default=1.0)
    is_enabled = Column(Boolean, default=True)
    status = Column(String, default='HEALTHY') # HEALTHY | DISABLED_USER | DISABLED_ERROR
    error_message = Column(Text)
    last_updated = Column(DateTime, default=datetime.utcnow)

class MarketRegimeLog(Base):
    __tablename__ = 'market_regime_log'
    id = Column(Integer, primary_key=True)
    log_date = Column(DateTime, unique=True)
    hmm_state = Column(String)
    hmm_probabilities = Column(Text) # JSON
    vix_level = Column(Float)
    sp500_return_5d = Column(Float)
    yield_spread_10y2y = Column(Float)
    put_call_ratio = Column(Float)
    macro_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class AlphaSignalsLog(Base):
    __tablename__ = 'alpha_signals_log'
    id = Column(Integer, primary_key=True)
    signal_id = Column(String)
    strategy_id = Column(String)
    symbol = Column(String)
    direction = Column(String)
    strength = Column(Float)
    conviction = Column(String)
    recommended_size = Column(Float)
    stop_price = Column(Float)
    take_profit_price = Column(Float)
    metadata_json = Column(Text)
    acted_on = Column(Boolean, default=False)
    blocked_by = Column(String)
    outcome_pnl = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class PortfolioSnapshot(Base):
    __tablename__ = 'portfolio_snapshots'
    id = Column(Integer, primary_key=True)
    snapshot_time = Column(DateTime, unique=True)
    total_equity = Column(Float)
    cash_balance = Column(Float)
    positions_value = Column(Float)
    daily_pnl = Column(Float)
    total_pnl = Column(Float)
    num_open_positions = Column(Integer)
    drawdown_pct = Column(Float)
    sharpe_rolling_30d = Column(Float)
    var_99 = Column(Float)
    regime_state = Column(String)
    stress_test_json = Column(Text)
    monte_carlo_json = Column(Text)

class DailyCycleLog(Base):
    __tablename__ = 'daily_cycle_log'
    id = Column(Integer, primary_key=True)
    cycle_date = Column(DateTime, unique=True)
    starting_capital = Column(Float)
    ending_equity = Column(Float)
    preliminary_pnl = Column(Float)
    final_pnl = Column(Float)
    after_hours_pnl = Column(Float)
    daily_pnl_pct = Column(Float)
    profit_extracted = Column(Float)
    profit_wallet_cumulative = Column(Float)
    cycle_state = Column(String)
    num_trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    largest_win = Column(Float)
    largest_loss = Column(Float)
    strategies_used = Column(Text) # JSON
    regime_state = Column(String)
    settlement_timestamp_preliminary = Column(DateTime)
    settlement_timestamp_final = Column(DateTime)
    notes = Column(Text)

class ControlFlag(Base):
    __tablename__ = 'control_flags'
    id = Column(Integer, primary_key=True)
    flag_key = Column(String, unique=True)
    flag_value = Column(String)
    updated_by = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)

class LLMFallbackLog(Base):
    __tablename__ = 'llm_fallback_log'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    symbol = Column(String)
    data_source = Column(String)
    tier_attempted = Column(Integer)
    tier_used = Column(Integer)
    fallback_reason = Column(Text)
    vader_score = Column(Float)
    finbert_score = Column(Float)
    regex_hit_count = Column(Integer)
    action_taken = Column(String)

class StrategyCorrelationMatrix(Base):
    __tablename__ = 'strategy_correlation_matrix'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, unique=True)
    matrix_json = Column(Text)

class DarkPoolPrint(Base):
    __tablename__ = 'dark_pool_prints'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    symbol = Column(String)
    price = Column(Float)
    volume = Column(Float)
    notional_value = Column(Float)
    is_sweep = Column(Boolean)
    exchange_code = Column(String)
    direction_inferred = Column(String)
    candle_direction_5m = Column(String)

class OptionsPosition(Base):
    __tablename__ = 'options_positions'
    id = Column(Integer, primary_key=True)
    underlying = Column(String)
    expiry = Column(DateTime)
    strike = Column(Float)
    option_type = Column(String)
    qty = Column(Float)
    premium_paid = Column(Float)
    delta = Column(Float)
    gamma = Column(Float)
    theta = Column(Float)
    vega = Column(Float)
    rho = Column(Float)
    iv = Column(Float)
    days_to_expiry = Column(Integer)
    broker = Column(String)
    strategy_id = Column(String)
    opened_at = Column(DateTime)
    closed_at = Column(DateTime)
    realized_pnl = Column(Float)

class GreeksSnapshot(Base):
    __tablename__ = 'greeks_snapshots'
    id = Column(Integer, primary_key=True)
    snapshot_time = Column(DateTime)
    net_delta = Column(Float)
    net_gamma = Column(Float)
    net_theta = Column(Float)
    net_vega = Column(Float)
    net_rho = Column(Float)
    positions_count = Column(Integer)
    portfolio_nav = Column(Float)

class CryptoPosition(Base):
    __tablename__ = 'crypto_positions'
    id = Column(Integer, primary_key=True)
    token = Column(String)
    network = Column(String)
    wallet_address = Column(String)
    qty = Column(Float)
    avg_cost = Column(Float)
    protocol_staked = Column(String)
    apy = Column(Float)
    last_harvest = Column(DateTime)
    current_value = Column(Float)

class FundingRateLog(Base):
    __tablename__ = 'funding_rate_log'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    exchange = Column(String)
    rate = Column(Float)
    timestamp = Column(DateTime)
    cumulative_8h_periods = Column(Integer)
