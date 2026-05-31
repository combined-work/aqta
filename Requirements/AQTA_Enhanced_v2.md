# AUTONOMOUS QUANTITATIVE TRADING ARCHITECTURE (AQTA)
## Comprehensive System Specification & Master Blueprint — Enhanced Edition v2.0

> **Infrastructure:** Local Windows (Tier 1 only). No cloud dependency.
> **LLM:** Optional module — all strategies operate fully without it.
> **Strategy Count:** 130+ strategies across 8 families.

---

## CHANGE LOG vs v1.0

| Area | Change |
|---|---|
| Architecture | Removed Tier 2 Enterprise Cloud. Enhanced local stack with DuckDB analytics layer and optional local Redis. |
| LLM | Demoted to optional module behind `llm_analysis_enabled` flag. All strategies implement a `_rule_based_fallback()` path. |
| Strategy Arsenal | 130+ total strategies; primary 6 families expanded from ~36 to 110+ strategies. |
| Meta-Brain | Added Transformer-based regime detector, Kalman Filter signal smoother, online learning loop, and ensemble voting without LLM dependency. |
| Risk Engine | Added Greeks-aware portfolio risk, margin optimizer, intraday VaR rolling window, and per-strategy Kelly sizing audit. |
| UI | Rewritten as a multi-tab, WebSocket-driven SPA. Nine dedicated dashboards, charting suite, alert center, parameter tuning console, and optional LLM insights panel. |
| Scheduling | 14-step 24-hour schedule (was 10). Added pre-open data warmup, intraday micro-cycle, and adaptive retraining triggers. |
| Tax Engine | Added wash-sale proxy intelligence scoring, AMT impact estimator, and fiscal year rollover planner. |
| Observability | Added local Prometheus metrics endpoint, DuckDB-backed analytics queries, and HTML performance report exporter. |

---

## 1. SYSTEM OVERVIEW & OPERATING DOCTRINE

AQTA is a self-directed, multi-asset, multi-broker quantitative trading platform engineered for continuous 24/7/365 autonomous operation on local Windows infrastructure. It maximizes risk-adjusted, tax-aware returns by combining systematic strategies, machine learning regime detection, smart order routing, and a robust daily capital cycle — all without requiring cloud services or LLM availability.

---

### 1.1 Capital Framework & Daily Cycle Rules

The system treats each trading day as an independent compounding event against a rolling capital base.

- **Capital Base:** $10,000 baseline per cycle (auto-adjusted post-profit-sweep).
- **Daily Profit Targets:**
  - *Minimum:* $150 (1.5%)
  - *Ideal:* $300 (3.0%)
  - *Stretch:* $500 (5.0%)
  - *Exceptional (no force-halt):* $750 (7.5%) — system continues but strategy allocation shifts to capital-preservation mode.
- **Profit Extraction Rule:** If EOD equity > $10,000 + Minimum Target, the excess flows to a virtual `profit_wallet`. Real cash stays in brokerage until the weekly ACH threshold (`PROFIT_SWEEP_THRESHOLD = $30,000`) is met, or manually triggered via UI.
- **Profit Lock Mechanism:** Once intraday profit ≥ $2,000, 60% (`profit_protect_pct = 0.60`) is locked. A soft halt triggers if equity drops below this locked floor. At $3,000 profit, locks increase to 70%.
- **Tiered Loss Limits:**
  - *Soft Halt:* -$150 (-1.5%) → 50% reduction in all new position sizing; generates `SOFT_HALT` alert.
  - *Hard Halt:* -$300 (-3.0%) → full system halt; cancels all open limit orders; requires manual resume.
  - *Emergency Halt:* -$500 (-5.0%) → triggers emergency liquidation of all open positions (market orders), sends critical alert.
- **Capital Scaling Rule:** After every 10 consecutive profitable days, the capital base for sizing calculations grows by 5%, up to 2.0x the original base. This allows compounding without over-leveraging.

---

### 1.2 Zero-Loss Protocol & Recovery Mode

- **Duration:** Up to 5 trading days (`recovery_max_days = 5`).
- **Target:** `recovery_target = abs(daily_pnl) * 1.1` (exact loss + 10% buffer).
- **Risk Adjustment:** Position sizes halved (`recovery_risk_multiplier = 0.5`).
- **Strategy Bias:** Mean Reversion, Cash Management, and Hedging strategies receive a 40% allocation premium. Intraday and high-beta momentum strategies are capped at 20% of capital.
- **Recovery Acceleration:** If intraday profit > 50% of recovery target before noon, the system may cautiously re-enable 1 additional momentum strategy.
- **Compounding Mode (Converse):** After 5 consecutive profitable days, the position size multiplier increases to 1.2x. After 10, it reaches 1.35x (capped). Resets on any losing day.
- **Failure Escalation:** If recovery target is not met after 5 days, AQTA enters **Capital Preservation Mode**: only Cash Management, Hedging, and theta-positive options strategies may trade, until a full profitable day restores normal mode.

---

### 1.3 Target KPIs & Performance Benchmarks

| KPI | Target | Measurement Window |
|---|---|---|
| Annualized Sharpe Ratio | > 3.0 | Monthly rolling |
| Sortino Ratio | > 4.5 | Monthly rolling |
| Maximum Drawdown | < 8% portfolio-wide | Rolling 90 days |
| Calmar Ratio | > 2.5 | Annual |
| Win Rate | > 55% all strategies | Rolling 90 days |
| Average Hold Period | 2–15 days (equities) | Rolling 30 days |
| Options PnL Contribution | > 30% of total PnL | Weekly |
| Theta Decay Capture | > 80% of written premium | Per position |
| Execution Latency (SOR) | < 5ms | Per order |
| System Uptime | > 99.5% | Monthly |
| Tax Alpha (after-tax vs pre-tax) | > 0.5% annually | Quarterly |
| LLM Accuracy (when enabled) | > 65% direction accuracy | Rolling 30 days |
| Strategy Correlation (avg pairwise) | < 0.30 | Weekly |

---

### 1.4 Market Regime Operating Modes

The Meta-Brain's regime detector determines which operating mode is active, reshaping all allocation weights dynamically:

| Regime | Momentum | Mean Rev | Arb/Quant | Macro | Cash/Hedge |
|---|---|---|---|---|---|
| BULL_TREND | 35% | 15% | 20% | 20% | 10% |
| BEAR_TREND | 5% | 25% | 20% | 25% | 25% |
| SIDEWAYS_LOW_VOL | 10% | 30% | 30% | 10% | 20% |
| SIDEWAYS_HIGH_VOL | 10% | 20% | 20% | 15% | 35% |
| CRASH_RISK | 0% | 10% | 15% | 15% | 60% |
| RECOVERY | 20% | 30% | 20% | 15% | 15% |

---

## 2. ARCHITECTURE & TECHNOLOGY STACK

AQTA runs entirely on local Windows infrastructure. There is no cloud dependency. All data, models, databases, and services reside on the host machine or local network.

---

### 2.1 Local Windows Deployment

- **Runtime:** Python 3.11+ (asyncio-native, `uvloop` optional for Linux performance parity via WSL2).
- **Operational Database:** SQLite 3 (WAL mode, `PRAGMA foreign_keys = ON`, `PRAGMA journal_mode = WAL`, `PRAGMA synchronous = NORMAL`) + SQLAlchemy 2.0.30.
- **Analytics Database:** DuckDB 0.10+ (columnar, in-process). Used for all read-heavy queries: strategy performance analytics, PnL attribution, tax reporting, and backtesting result storage. Zero network overhead; accessed directly via `duckdb` Python library.
- **In-Memory Cache & Pub/Sub (Optional):** Redis 7 (localhost, Windows WSL2 or Redis for Windows). Enabled via `redis_enabled = true` control flag. Used for real-time signal bus, session caching, and rate-limit counters. Falls back to in-process `asyncio.Queue` if Redis is unavailable.
- **Task Scheduling:** APScheduler 3.10.4 (`AsyncIOScheduler`, `America/New_York` timezone).
- **API & Engine:** FastAPI 0.111.0 + Uvicorn 0.30.0 (Engine on :8765, UI on :8766).
- **UI Frontend:** Single-Page Application in Vanilla HTML5/CSS3/ES2022 (no Node/npm). Uses Chart.js 4.x, D3.js 7.x, and Lightweight Charts (TradingView) for financial charting. All JS bundled inline — zero CDN dependencies at runtime (pre-cached locally).
- **Process Management:** NSSM (Non-Sucking Service Manager) registers `AQTA_Engine` and `AQTA_UI` as Windows services with auto-restart on failure. `watchdog` Python library monitors file system for hot-reload of config changes.
- **Local Observability (Optional):** Prometheus 2.x (metrics endpoint at `/metrics` on :8765) + Grafana (local install on :3000). Pre-built dashboard JSON included in `ui/grafana/`. Enabled via `prometheus_enabled = true`.
- **Backup:** SQLite hot backup to `data_cache/backups/` nightly. DuckDB checkpoint exported to Parquet. 7-zip compression with 30-day retention.

---

### 2.2 LLM Module (Optional)

The LLM subsystem is controlled by `llm_analysis_enabled` in `control_flags`. **Every feature that calls the LLM must implement a `_rule_based_fallback()` method** that activates when LLM is disabled or unavailable. The system is fully functional at 100% capacity without any LLM.

- **Local (Preferred):** Ollama server on localhost. Supported models: `llama3.3`, `mistral-nemo`, `deepseek-r1:8b`, `phi3.5`. Model selected by `LLM_LOCAL_MODEL` env var.
- **Cloud Fallback (Optional):** `anthropic` SDK (Claude Sonnet), `openai` SDK (GPT-4o-mini). Only used if local Ollama is unreachable AND `llm_cloud_fallback = true`.
- **FinBERT (Embedded, Always On):** `ProsusAI/finbert` via Hugging Face `transformers`. Runs locally, GPU-accelerated if CUDA available. This is NOT gated by `llm_analysis_enabled` — it is a lightweight ML model, not an LLM.
- **Rule-Based Fallback:** Keyword scoring engine using curated financial lexicons (bullish/bearish/neutral word lists). Scores news headlines without any LLM call.

---

### 2.3 Core Python Libraries

**Data & Math:**
`pandas 2.2.2`, `numpy 1.26.4`, `scipy 1.13.0`, `pandas-ta 0.3.14b`, `ta-lib` (compiled), `duckdb 0.10+`, `pyarrow 16.0`.

**ML & Quant:**
`scikit-learn 1.5.0`, `hmmlearn 0.3.2`, `statsmodels 0.14.2`, `pyportfolioopt 1.5.5`, `riskfolio-lib 5.x`, `cvxpy 1.5`, `filterpy 1.4.5` (Kalman), `arch 6.x` (GARCH volatility), `lightgbm 4.x`, `optuna 3.6` (hyperparameter tuning).

**Options:**
`py_vollib_vectorized 0.1.2`, `QuantLib-Python 1.33`.

**LLM (Optional):**
`ollama 0.2.1`, `transformers 4.40+`, `anthropic`, `openai`, `sentence-transformers` (embeddings).

**Brokers & Market Data:**
`schwab-py 1.2.0`, `robin_stocks 3.0.4`, `ib_insync 0.9.86`, `alpaca-trade-api 3.x`, `ccxt 4.x`, `web3 6.x`, `yfinance 0.2.x`, `polygon-api-client 1.x`, `finnhub-python`, `pytrends`, `praw`.

**Async I/O & Utilities:**
`aiohttp 3.9.5`, `aiofiles`, `websockets 12.0`, `httpx`, `tenacity` (retry), `structlog`, `prometheus-client`, `pydantic 2.7`, `pyotp`, `schedule`.

---

### 2.4 Enhanced Directory Structure

```
C:\TradingSystem\
├── engine\
│   ├── api\
│   │   ├── engine_api.py           # FastAPI on :8765
│   │   ├── websocket_manager.py    # WebSocket broadcast hub
│   │   └── metrics.py              # Prometheus metrics definitions
│   ├── brain\
│   │   ├── opportunity_ranker.py
│   │   ├── daily_pnl_manager.py
│   │   ├── capital_allocator.py
│   │   └── signal_aggregator.py    # NEW: cross-strategy signal dedup
│   ├── brokers\
│   │   ├── base_broker.py
│   │   ├── schwab_broker.py
│   │   ├── robinhood_broker.py
│   │   ├── ibkr_broker.py
│   │   ├── alpaca_broker.py
│   │   ├── coinbase_broker.py
│   │   └── mock_broker.py
│   ├── data\
│   │   ├── market_data.py
│   │   ├── options_data.py
│   │   ├── macro_data.py
│   │   ├── alternative_data.py
│   │   ├── level2_data.py          # NEW: L2 order book / tape
│   │   ├── dark_pool_data.py       # NEW: dark pool print aggregator
│   │   └── on_chain_data.py
│   ├── database\
│   │   ├── models.py               # SQLAlchemy ORM (SQLite)
│   │   ├── analytics_db.py         # NEW: DuckDB analytics layer
│   │   ├── session.py
│   │   └── migrations.py
│   ├── execution\
│   │   ├── order_router.py
│   │   ├── execution_engine.py
│   │   └── algo_orders.py          # TWAP/VWAP/Iceberg/POV/Sniper
│   ├── meta_brain\
│   │   ├── regime_detector.py      # HMM + Transformer ensemble
│   │   ├── allocator.py            # Thompson Sampling + Bayesian
│   │   ├── llm_analyst.py          # Optional; graceful fallback
│   │   ├── finbert_scorer.py       # Always-on NLP
│   │   ├── keyword_scorer.py       # Rule-based NLP fallback
│   │   ├── portfolio_optimizer.py
│   │   ├── kalman_smoother.py      # NEW: signal noise reduction
│   │   └── online_learner.py       # NEW: incremental model updates
│   ├── risk\
│   │   ├── risk_manager.py
│   │   ├── compliance.py
│   │   ├── greeks_monitor.py       # NEW: portfolio Greeks limits
│   │   └── margin_optimizer.py     # NEW: margin utilization
│   ├── scanner\
│   │   ├── opportunity_scanner.py
│   │   ├── stock_screener.py
│   │   ├── options_flow_scanner.py # NEW: unusual options activity
│   │   └── dark_pool_scanner.py    # NEW
│   ├── scheduler\
│   │   └── jobs.py
│   ├── strategies\
│   │   ├── base_strategy.py
│   │   ├── equity\
│   │   │   ├── momentum\           # EQ-01, A1–A18
│   │   │   └── mean_reversion\     # EQ-03, B1–B14
│   │   ├── options\                # OP-01–OP-12, C4, C6–C9
│   │   ├── crypto\                 # CR-01–CR-07
│   │   ├── macro\                  # F1–F18
│   │   ├── quant\                  # EQ-02, E1–E16
│   │   ├── sentiment\              # D1–D16
│   │   ├── cash_hedging\           # CM-01–CM-12, EQ-04
│   │   └── fx_fi\                  # FX-01–FX-05, FI-01–FI-04
│   ├── tax\
│   │   ├── tax_engine.py
│   │   ├── tax_optimizer.py
│   │   └── tax_reporter.py         # NEW: Form 8949, estimated payments
│   ├── backtest\                   # NEW module
│   │   ├── backtester.py
│   │   ├── walk_forward.py
│   │   ├── monte_carlo.py
│   │   └── performance_stats.py
│   ├── notifications\              # NEW module
│   │   ├── alert_manager.py
│   │   └── channels.py             # Desktop toast, email, SMS, webhook
│   ├── main.py
│   └── config.py
├── ui\
│   ├── ui_server.py                # FastAPI on :8766
│   └── static\
│       ├── index.html              # SPA shell
│       ├── app.js                  # Core SPA router and state
│       ├── tabs\
│       │   ├── overview.js         # Tab 1: Command Center
│       │   ├── strategies.js       # Tab 2: Strategy Matrix
│       │   ├── positions.js        # Tab 3: Positions & Orders
│       │   ├── analytics.js        # Tab 4: Performance Analytics
│       │   ├── options.js          # Tab 5: Options Dashboard
│       │   ├── scanner.js          # Tab 6: Live Scanner
│       │   ├── tax.js              # Tab 7: Tax Dashboard
│       │   ├── backtest.js         # Tab 8: Backtest Console
│       │   └── settings.js         # Tab 9: Parameter Tuning
│       ├── components\
│       │   ├── chart_equity.js
│       │   ├── chart_heatmap.js
│       │   ├── chart_greeks.js
│       │   ├── notification_center.js
│       │   └── llm_insights.js     # Collapsible, only when LLM on
│       ├── lib\                    # Locally vendored Chart.js, D3, LW-Charts
│       └── styles.css
├── shared\
│   ├── trading.db                  # SQLite operational DB
│   └── analytics.duckdb            # DuckDB analytics DB
├── logs\
│   ├── engine.jsonl                # Rotating JSON logs (structlog)
│   ├── trades.jsonl
│   └── errors.jsonl
├── data_cache\
│   ├── features\                   # Parquet feature store per symbol
│   ├── models\                     # Serialized HMM, LightGBM, etc.
│   ├── backups\                    # Nightly DB backups
│   ├── reports\                    # HTML/PDF performance reports
│   └── sp500_components.json
├── config\
│   ├── settings.toml               # Primary config (TOML, human-readable)
│   ├── broker_secrets.env          # OAuth tokens, API keys (gitignored)
│   └── proxy_swap_map.json
└── tests\
    ├── unit\
    ├── integration\
    └── strategy_simulations\
```

---

## 3. DATABASE SCHEMA & STATE MANAGEMENT

AQTA uses a **dual-database architecture**: SQLite (WAL mode) for all real-time operational writes, and DuckDB for all analytical reads. Writes never touch DuckDB directly — a nightly ETL job (`analytics_db.py:sync_to_duckdb()`) copies closed trades, signals, and snapshots to DuckDB for fast OLAP queries.

---

### 3.1 Core Trading Tables (SQLite)

- **`trades`**: `id` (PK), `symbol`, `asset_class` (EQUITY/OPTION/CRYPTO/ETF/CASH/FX/FI), `broker`, `strategy_id`, `direction` (BUY/SELL/BTO/STC/STO/BTC), `qty`, `order_type` (MARKET/LIMIT/STOP/STOP_LIMIT/TRAIL), `limit_price`, `fill_price`, `commission`, `slippage_bps`, `status` (PENDING/FILLED/PARTIAL/CANCELLED/REJECTED), `broker_order_id`, `fill_timestamp`, `algo_type` (MARKET/TWAP/VWAP/ICEBERG/POV), `algo_params_json`, `created_at`, `notes`.

- **`positions`**: `id` (PK), `symbol` (Unique), `asset_class`, `broker`, `current_qty`, `average_cost`, `last_price`, `unrealized_pl`, `unrealized_pl_pct`, `realized_pl`, `days_held`, `strategy_id`, `stop_price`, `take_profit_price`, `trailing_stop_pct`, `delta`, `theta`, `vega`, `gamma`, `rho`, `portfolio_delta_contribution`, `option_expiry`, `option_strike`, `option_type`, `iv_at_entry`, `iv_current`, `last_updated`.

- **`orders`**: `id` (PK), `parent_trade_id`, `broker_order_id`, `status`, `fills_json`, `routing_reason`, `latency_ms`, `venue_quotes_json` (MiFID II best-ex log), `slippage_realized_bps`.

- **`signals_queue`**: `id` (PK), `strategy_id`, `symbol`, `direction`, `strength` (0.0–1.0), `conviction` (LOW/MEDIUM/HIGH/EXTREME), `recommended_size`, `stop_price`, `take_profit_price`, `signal_type` (ENTRY/EXIT/SCALE_IN/SCALE_OUT), `metadata_json`, `status` (PENDING/ACTED/BLOCKED/EXPIRED), `expiry_at`, `created_at`. Expired signals (> 5 min for intraday, > 2 days for swing) are auto-archived.

---

### 3.2 Tax & Compliance Tables (SQLite)

*(As in v1.0, plus the following additions)*

- **`tax_lots`**: *(unchanged from v1.0)* + `amt_adjustment` (float) — AMT cost basis adjustment flag.
- **`wash_sale_blacklist`**: *(unchanged)* + `proxy_score` (float, 0–1): similarity score between sold security and its best available proxy. Higher score → better wash-sale avoidance.
- **`estimated_tax_payments`**: `id` (PK), `period` (Q1/Q2/Q3/Q4), `fiscal_year`, `estimated_stcg`, `estimated_ltcg`, `estimated_ordinary_income`, `federal_liability`, `state_liability`, `safe_harbor_amount`, `payment_due_date`, `status` (PROJECTED/DUE/PAID).

---

### 3.3 Intelligence & ML Tables (SQLite)

- **`strategy_performance`**: *(unchanged)* + `avg_entry_score` (float): avg composite opportunity score at entry. `avg_regime_match` (float): % of trades taken in the strategy's ideal regime. `profit_factor` (float): gross wins / gross losses.
- **`market_regime_log`**: *(unchanged)* + `transformer_state` (TEXT): regime predicted by transformer ensemble. `ensemble_agreement` (float): % agreement between HMM and transformer. `regime_duration_days` (int): consecutive days in current regime.
- **`alpha_signals_log`**: *(unchanged)* + `kalman_smoothed_strength` (float): signal strength after Kalman filter smoothing. `correlation_penalty` (float): reduction applied due to portfolio correlation check.
- **`alternative_signals`**: *(unchanged)* + `dark_pool_print_size` (float): dollar value of detected dark pool print if source=DARK_POOL. `uoa_contract_count` (int): unusual options activity contract count if source=OPTIONS_FLOW.
- **`backtest_results`**: `id` (PK), `run_id`, `strategy_id`, `start_date`, `end_date`, `total_return`, `annualized_return`, `sharpe_ratio`, `sortino_ratio`, `max_drawdown`, `calmar_ratio`, `win_rate`, `profit_factor`, `total_trades`, `avg_hold_days`, `params_json`, `walk_forward_is_oos` (bool), `created_at`.

---

### 3.4 Capital & System State Tables (SQLite)

*(As in v1.0, plus the following)*

- **`portfolio_snapshots`**: *(unchanged)* + `net_delta` (float), `net_theta` (float), `net_vega` (float), `margin_used` (float), `margin_available` (float), `volatility_target_scalar` (float).
- **`control_flags`** (pre-populated defaults):

| Key | Default | Description |
|---|---|---|
| `trading_enabled` | `true` | Master kill switch |
| `shadow_mode` | `true` | Paper trading mode |
| `llm_analysis_enabled` | `false` | Optional LLM module |
| `llm_cloud_fallback` | `false` | Allow cloud LLM if local unavailable |
| `tlh_enabled` | `true` | Tax-loss harvesting |
| `crypto_enabled` | `false` | Crypto strategies |
| `options_enabled` | `false` | Options strategies |
| `meta_brain_enabled` | `true` | HMM + regime detection |
| `redis_enabled` | `false` | Local Redis pub/sub |
| `prometheus_enabled` | `false` | Metrics endpoint |
| `dark_pool_enabled` | `false` | Dark pool data scanning |
| `level2_enabled` | `false` | Level 2 order book feed |
| `intraday_strategies_enabled` | `true` | Intraday sub-strategies |
| `macro_strategies_enabled` | `true` | Macro/thematic strategies |
| `engine_status` | `STOPPED` | Runtime state |
| `volatility_targeting_enabled` | `true` | Vol-target position scaling |
| `auto_rebalance_enabled` | `true` | Weekend portfolio rebalance |

---

### 3.5 DuckDB Analytics Schema

DuckDB stores denormalized, read-optimized copies of closed trades and signals. Schema is auto-generated by `analytics_db.py`. Key tables:

- **`fact_trades`**: Full trade record including fill, cost, tax lot method, after-tax PnL, hold period, strategy, regime at entry.
- **`fact_signals`**: All signals with outcome PnL, accuracy classification, and Kalman-smoothed score.
- **`dim_strategy`**: Strategy metadata, family, risk class.
- **`dim_regime`**: Regime state history with duration.
- **`agg_daily_pnl`**: Pre-aggregated daily PnL by strategy, asset class, and regime.
- **`agg_tax_summary`**: Annual/quarterly tax rollup for fast dashboard queries.

---

## 4. DATA INGESTION & ALTERNATIVE DATA ENGINE

All data fetching is asynchronous. Blocking libraries are wrapped with `asyncio.get_event_loop().run_in_executor()`. Data is cached locally in Parquet (`data_cache/features/`). Rate limits are enforced by `asyncio.Semaphore` per API provider.

---

### 4.1 Market Data (`engine/data/market_data.py`)

- **Historical OHLCV:** Primary: Polygon.io REST API (paid tier). Fallback: `yfinance`. Cached as `{symbol}_{period}_{interval}.parquet`. Cache TTL: 24h for daily bars, 1h for intraday.
- **Real-Time Quotes:** WebSocket streams from Finnhub (equities) and Polygon (options). Normalized to `QuoteEvent(symbol, price, bid, ask, volume, timestamp_ns, source)`.
- **Batch Quotes:** `asyncio.gather()` with `asyncio.Semaphore(15)`. Auto-throttles on 429 responses.
- **Indicators (`pandas_ta`):** RSI(14), MACD(12,26,9), Bollinger Bands(20,2), ATR(14), EMA(9,21,50,200), ADX(14), OBV, Stochastic(14,3), Williams %R(14), CCI(14), KAMA(10,2,30), VWAP (intraday), Parabolic SAR, Ichimoku Cloud, Donchian Channels(20), Keltner Channels(20,2), Heikin Ashi candles.
- **Multi-Timeframe Data:** For intraday strategies, fetches 1m, 5m, 15m, 1h, and daily bars simultaneously. `MultiTimeframeData` dataclass aggregates across timeframes.
- **Macro Data:** FRED API (DGS10, DGS2, DGS30, FEDFUNDS, CPIAUCSL, UNRATE, GDP, UMCSENT). Cached 24h.
- **Economic Calendar:** Scraped from Investing.com (earnings, FOMC, NFP, CPI, PMI, retail sales) and cached in `economic_events` SQLite table.

---

### 4.2 Options Data (`engine/data/options_data.py`)

- **Options Chain:** Polygon Options API (primary), `yfinance` fallback. Full chain cached every 15 mins during market hours.
- **IV Surface:** Constructs a `{strike → expiry → IV}` surface using cubic spline interpolation. Calculates IV rank (52-week percentile) and IV percentile.
- **Greeks Calculation:** `py_vollib_vectorized` for Delta, Gamma, Theta, Vega, Rho using Black-Scholes-Merton. QuantLib used for American-style options with early-exercise premium.
- **Portfolio Greeks:** Net Delta, Gamma, Theta, Vega, Rho aggregated across all positions. Stored in `portfolio_snapshots` every 5 minutes.
- **Unusual Options Activity (UOA):** Detects large options sweeps: `volume > open_interest * 2` and `premium_paid > $50,000`. Classified as BULLISH_SWEEP, BEARISH_SWEEP, or NEUTRAL_BLOCK. Written to `alternative_signals`.

---

### 4.3 Level 2 & Tape Data (`engine/data/level2_data.py`) — Optional

Enabled via `level2_enabled = true`. Requires Polygon WebSocket subscription or IBKR Level 2 feed.

- **Order Book Snapshot:** Top 5 bid/ask levels per symbol. Recalculates `bid_ask_imbalance = (bid_size - ask_size) / (bid_size + ask_size)`. Values > 0.3 indicate buying pressure.
- **Tape Reader:** Aggregates individual prints into 1-second buckets. Calculates `aggressor_ratio` (buyer-initiated vs seller-initiated). Rising ratio at support = bullish signal.
- **Iceberg Detection:** Flags orders that consistently refresh at the same price level, suggesting hidden large orders.

---

### 4.4 Alternative Data (`engine/data/alternative_data.py`)

*(All sources from v1.0, plus the following enhancements)*

- **Dark Pool Prints:** Finra ATS data (free, T+1) + CBOE BYX dark pool reports. Aggregates `dark_pool_volume_pct = dark_pool_volume / total_volume` per symbol. Stored in `alternative_signals` with `source = DARK_POOL`. Enabled via `dark_pool_enabled = true`.
- **13F Filing Velocity:** Beyond raw new positions, tracks the *rate of change* in a fund's position (added vs prior quarter). Scores based on conviction increase (same fund adds to position 2 quarters running).
- **Supply Chain Contagion:** Maintains a `supply_chain_graph.json` mapping top suppliers/customers for S&P 500 companies. When a company reports negative guidance, flags its top 3 customers and suppliers as watchlist candidates.
- **Short Interest Velocity:** Tracks short interest change week-over-week. A >15% increase in short float in one week triggers a watchlist flag (potential squeeze or legitimate deterioration).
- **Options Sentiment Score:** Combines put/call ratio, skew (25-delta), and UOA direction into a single `options_sentiment_score` per symbol (−1.0 to +1.0). Updated hourly.
- **Earnings Whisper:** Scrapes Estimize.com consensus vs Street consensus gap. A >5% upside whisper vs consensus with positive options sentiment = high-conviction earnings play.

---

## 5. BROKER INTEGRATION & SMART ORDER ROUTING

*(Core v1.0 architecture retained; enhanced below)*

---

### 5.1 Universal Broker Interface — Additions

- **`get_level2_snapshot(symbol)`**: Returns top 5 bid/ask for brokers supporting L2 (IBKR, Alpaca).
- **`get_options_chain_greeks(symbol, expiry)`**: Returns chain with live Greeks calculated server-side (IBKR native greeks endpoint).
- **`get_margin_status()`**: Returns `{margin_used, margin_available, reg_t_excess, portfolio_margin_available}`.
- **Circuit Breaker Enhancement:** Tracks error types separately. Transient network errors (5xx, timeout) retry; authentication errors (401, 403) trigger immediate re-auth flow without circuit-open.

---

### 5.2 Smart Order Router — Enhanced Routing Logic

Order evaluation chain (evaluated top-to-bottom, first match wins):

1. Shadow Mode → `MockBroker`.
2. Emergency/Halt liquidation → `IBKRBroker` (fastest fills).
3. CRYPTO → `CoinbaseBroker` (primary), `RobinhoodBroker` (fallback).
4. OPTION → `SchwabBroker` (primary), `IBKRBroker` (complex, > 4-leg).
5. Notional > $100k → `IBKRBroker`.
6. Pre/Post-market (before 09:29 or after 16:01 ET) → `RobinhoodBroker` or `AlpacaBroker`.
7. Fractional (qty < 1.0) → `RobinhoodBroker`.
8. FX/Futures → `IBKRBroker`.
9. Standard equity < $100k → Best bid/ask across `SchwabBroker` + `AlpacaBroker`; default `SchwabBroker`.

---

### 5.3 Execution Algorithms (`engine/execution/algo_orders.py`)

| Algorithm | Use Case | Logic |
|---|---|---|
| MARKET | Urgency: stop triggers, halt liquidation | Direct market order |
| LIMIT | Standard entry/exit | Joins bid/ask midpoint; chases at configurable tick increments |
| TWAP | Large orders over time | Splits into equal slices over a configurable window (default 20 min) |
| VWAP | Market-impact minimization | Slice sizes proportional to 5-min historical volume profile |
| ICEBERG | Conceal order size | Shows 10% to market; auto-refills on fills |
| POV (Participation of Volume) | Track market volume % | Targets 15–20% of real-time volume; throttles with market |
| SNIPER | Short-lived momentum | Fires IOC (Immediate-Or-Cancel) limit at ask + 1 tick; cancels if unfilled in 200ms |
| CLOSE_ONLY | MOC/LOC orders | Routes as market-on-close or limit-on-close orders before 15:55 ET |

---

## 6. THE META-BRAIN (AI & QUANT CORE)

---

### 6.1 Market Regime Detector (`engine/meta_brain/regime_detector.py`)

**Ensemble of two independent models:**

**Model A — Gaussian HMM (`hmmlearn`):**
- `GaussianHMM(n_components=6, covariance_type="full", n_iter=500)`.
- Features: 2 years of SPY daily data. `X = [daily_return, log_volume, vix_norm, atr_norm, macd_hist_norm, yield_spread_10y2y, put_call_ratio, obv_change_norm]`.
- States: `BULL_TREND`, `BEAR_TREND`, `SIDEWAYS_LOW_VOL`, `SIDEWAYS_HIGH_VOL`, `CRASH_RISK`, `RECOVERY`.
- Retrained weekly (nightly if > 14 days since last retrain or if ensemble disagreement persists > 3 days).

**Model B — LightGBM Classifier:**
- Trained on 5 years of labeled regimes (manually labeled via UI or bootstrap-labeled using HMM). Features: all HMM inputs + credit spreads, VIX term structure slope, advance/decline ratio, % stocks above 200-day MA.
- Outputs 6-class probability distribution.

**Ensemble Voting:** Weighted average of HMM and LightGBM probabilities. Weights: HMM=0.45, LightGBM=0.55 (adjustable, tuned via Optuna). `ensemble_agreement = max(probability_vector)`. If < 0.45, regime is `UNCERTAIN` and system reduces all position sizes by 25%.

---

### 6.2 Opportunity Scanner & Screener (`engine/scanner/`)

*(v1.0 logic retained; enhanced scoring)*

**Enhanced Tier 2 Composite Score:**
```
composite_score = (
    0.20 * momentum_score     +   # RSI, MACD, EMA alignment
    0.15 * volume_score       +   # vs 20-day average
    0.12 * trend_score        +   # ADX + directional strength
    0.15 * catalyst_score     +   # earnings, insider, news, L2 imbalance
    0.18 * regime_score       +   # strategy-regime compatibility
    0.10 * options_flow_score +   # UOA alignment (if options_enabled)
    0.10 * sentiment_score        # FinBERT + social composite
)
```

**Signal Deduplication (`brain/signal_aggregator.py`):** Before sending any signal to the execution engine, the `SignalAggregator` checks if the same symbol + direction already has an open position or pending signal within the last 30 minutes (configurable). Duplicate signals are merged (strengthened) rather than creating redundant orders.

---

### 6.3 Capital Allocator (`engine/meta_brain/allocator.py`)

*(v1.0 Thompson Sampling retained; enhanced)*

- **Contextual Thompson Sampling:** Beta distribution per `(strategy_id, regime, time_of_day_bucket)`. Time-of-day buckets: PRE_MARKET, OPEN_HOUR, MID_MORNING, LUNCH, AFTERNOON, POWER_HOUR, AFTER_HOURS.
- **Bayesian Update:** Win → `alpha += 1 + (pnl_pct / avg_win_pct)` (weighted by profitability), Loss → `beta += 1 + abs(pnl_pct / avg_loss_pct)`.
- **Anti-Concentration Penalty:** If a strategy would receive > 30% allocation, the excess is redistributed proportionally to strategies with < 15% allocation.
- **Minimum Activity Floor:** Each enabled strategy receives at least 5% allocation, ensuring the system continues to gather performance data across all strategies.

---

### 6.4 Multi-LLM Analyst (`engine/meta_brain/llm_analyst.py`) — OPTIONAL

*Only active when `llm_analysis_enabled = true`. Every call has a `_rule_based_fallback()` path.*

- **Local Primary:** Ollama (`llama3.3`, `mistral-nemo`, or `deepseek-r1:8b`). Timeout: 8 seconds. If no response, falls back immediately.
- **Cloud Fallback (if `llm_cloud_fallback = true`):** Anthropic Claude Sonnet or OpenAI GPT-4o-mini. Rate-limited to 20 calls/day to control cost.
- **FinBERT (Always On, Separate):** `ProsusAI/finbert` runs independently regardless of `llm_analysis_enabled`. Processes news headlines in batches. GPU-accelerated if CUDA available; CPU fallback with quantization.

**Structured Prompts:**
- *News Analysis:* `{"sentiment_score": 0–100, "direction": "BULLISH|BEARISH|NEUTRAL", "confidence": 0.0–1.0, "key_entities": [], "time_horizon": "INTRADAY|SWING|LONG_TERM"}`.
- *Earnings Call:* `{"guidance_revision": "UP|DOWN|NEUTRAL", "surprise_factor": "BEAT|MISS|IN_LINE", "tone_score": 0–100, "management_confidence": "HIGH|MED|LOW"}`.
- *10-K Risk:* `{"risk_score": 0–100, "risk_categories": [], "trend_vs_prior_year": "IMPROVING|WORSENING|STABLE"}`.

**Ensemble Voting:** Local LLM + FinBERT scores combined. If they disagree by > 35 points, system abstains from the LLM-driven component only (rule-based fallbacks still fire for the same signal).

**Rule-Based Fallback:** `keyword_scorer.py` uses curated lexicons: 200+ bullish terms, 200+ bearish terms, 50+ uncertainty modifiers. Headlines are tokenized, scored, and normalized to the same -1.0 to +1.0 range as FinBERT output.

---

### 6.5 Kalman Filter Signal Smoother (`engine/meta_brain/kalman_smoother.py`)

Uses `filterpy.kalman.KalmanFilter` to smooth noisy composite signal strength scores before they are acted upon. Each strategy family has its own Kalman filter tuned to its typical signal frequency:

- **Momentum strategies:** Fast update (process noise Q = 0.1).
- **Mean Reversion strategies:** Slow update (Q = 0.05).
- **Macro strategies:** Very slow update (Q = 0.02).

The smoothed signal (`kalman_smoothed_strength`) is stored alongside the raw strength in `alpha_signals_log`. Only the smoothed signal is used for position sizing; raw signal is retained for research.

---

### 6.6 Online Learning Loop (`engine/meta_brain/online_learner.py`)

- **Incremental Model Updates:** LightGBM classifier and feature importance weights are updated incrementally (not full retrain) every 24 hours using the prior day's closed trades as labeled examples.
- **Concept Drift Detection:** Uses Page-Hinkley test on rolling strategy win rates. If drift detected (p-value < 0.05), triggers an emergency full retrain of the affected strategy's LightGBM model.
- **Feature Importance Tracking:** Feature importance scores from LightGBM are stored in `feature_store` table and displayed in the Analytics tab of the UI.

---

### 6.7 Portfolio Optimizer (`engine/meta_brain/portfolio_optimizer.py`)

*(v1.0 retained; additions below)*

- **Hierarchical Risk Parity (HRP):** Riskfolio-Lib HRP model used as a third allocation approach alongside MVO and CVaR-MVO. HRP is cluster-based and robust to estimation error in the covariance matrix.
- **Regime-Conditional Optimization:** Separate covariance matrices estimated per regime state (BULL, BEAR, SIDEWAYS, CRASH). At regime transition, the portfolio optimizer switches to the appropriate matrix within 2 trading days.
- **Transaction Cost Awareness:** Optimization objective penalizes turnover exceeding 20% of portfolio per week using a quadratic transaction cost term.

---

## 7. STRATEGY ARSENAL (130+ STRATEGIES)

All strategies inherit from `BaseStrategy(ABC)` and implement:
- `generate_signals(df, portfolio_state) -> list[SignalEvent]`
- `calculate_position_size(signal, portfolio_state) -> float`
- `_rule_based_fallback(df) -> float` — returns a sentiment/strength score 0–1 without any LLM call.

**Default Sizing:** Kelly Criterion `f = (win_rate/avg_loss - (1-win_rate)/avg_win) * 0.25`, capped at 10% of equity. Overridden by the Capital Allocator's Thompson Sampling weight.

---

### 7.1 Equity Momentum & Intraday — PRIMARY (EQ-01 to EQ-10, A1–A18)

*Goal: Capture directional price momentum from minutes to weeks using multi-timeframe confirmation, unusual volume, and catalyst-driven breakouts.*

**EQ-01 / Classic Trend Following:**
BUY when EMA-9 crosses above EMA-21, EMA-21 > EMA-50, ADX-14 > 25, RSI between 45–75. SELL signal when EMA-9 crosses below EMA-21 or RSI > 78. Stop: `close - 2*ATR(14)`. Take-Profit: `close + 4*ATR(14)`. Hold period: 3–10 days. Regime preference: BULL_TREND.

**EQ-05 / Trend Acceleration (Parabolic SAR):**
Enters when Parabolic SAR flips from above to below price AND ADX-14 slope is rising (current ADX > prior-day ADX * 1.05). Requires EMA-9 > EMA-21 alignment. Sized at 0.75x Kelly. Tightens stop using SAR value itself. Exits if SAR flips back above price.

**EQ-06 / Intraday Sector Momentum (30-Min):**
Every 30 minutes, ranks the 11 SPDR sector ETFs by their intraday return vs SPY. Goes long the top-performing sector ETF if its return > SPY + 0.4% and volume is above 1.5x average. Flattens all positions by 15:45 ET. Regime preference: BULL_TREND, SIDEWAYS_LOW_VOL.

**EQ-07 / Relative Volume Surge:**
Scans universe for `real_time_volume_rate > 4x` the average 5-minute volume rate. Requires price holding above 5-min VWAP and RSI between 50–70. Enters with a 0.5x Kelly size (smaller; these are fast-moving). Sets a tight 1.5*ATR stop. Holds max 90 minutes.

**EQ-08 / First-Hour Momentum Continuation:**
Identifies stocks that are up > 2% in the first 30 minutes with volume > 3x average. Enters on first 5-minute pullback to the 5-min VWAP that holds. Stop: 5-min low of pullback candle. Target: measured move (gap size projected forward). Only valid 10:00–11:30 AM ET.

**EQ-09 / Power Hour Sweep (15:30–16:00 ET):**
In the last 30 minutes of trading, momentum often accelerates. Scans for stocks making new intraday highs on above-average volume between 15:00 and 15:30 ET. Enters a small position (0.4x Kelly) at 15:30 if still holding the high. Exits with a MOC order at 15:55 ET (or earlier stop).

**EQ-10 / Intraday Breadth Divergence:**
Calculates S&P 500 advance/decline ratio every 15 minutes. If A/D ratio > 2.5 (strongly positive) but SPY is flat or slightly down (negative divergence), assumes the broad market will catch up and buys SPY. Reverse for A/D < 0.4. Small size (0.5x Kelly). Exit intraday.

**A1 / Opening Range Breakout (ORB):**
Calculates high/low of 9:30–9:45 candles. BUY if price breaks ORB high with volume > 2x 20-day average 15-min volume. SELL SHORT if breaks ORB low. Signals generated only before 11:30 AM. Stop: opposite side of ORB. Target: 1.5x ORB range projected from breakout.

**A2 / VWAP Momentum:**
BUY on first pullback to VWAP when: price > VWAP, VWAP slope > 0 (rising), and RSI bounces from 45–55 zone. Stop: 1*ATR below VWAP. Target: prior-day high or 2*ATR above entry. Regime preference: BULL_TREND, SIDEWAYS_LOW_VOL.

**A3 / Gap-and-Go:**
Pre-market gap > 3%. Requires: float < 100M OR (if LLM enabled: news sentiment > 70; fallback: positive keyword score > 0.6 using headline keywords). Enter at 9:32 AM if price is holding above prior close on real-time volume confirmation. Stop: pre-market low. Target: +5% from entry or prior resistance.

**A4 / Relative Strength Rotation:**
Ranks 11 SPDR ETFs by composite momentum: `(5d_return * 0.4 + 20d_return * 0.35 + 60d_return * 0.25)`. Long top 3, short bottom 1. Rebalances weekly (Friday close). Uses 1% NAV per position. Hold: 5–10 days.

**A5 / EMA Ribbon Expansion:**
Monitors `EMA(9), EMA(13), EMA(21), EMA(34), EMA(55)`. BUY when all EMAs are in perfect order (9 > 13 > 21 > 34 > 55) and the ribbon is expanding (each EMA slope is positive). This indicates a clean trending environment. Stop: close below EMA-21.

**A6 / 52-Week High Breakout:**
Scans universe for new 52-week highs with volume > 2x 20-day average. Enter on first intraday pullback (0.5–1.5% retracement) that holds above the prior 52-week high as new support. Stop: 2% below breakout level. Hold: 5–15 days.

**A7 / Unusual Volume Spike (No-News):**
Volume > 3x 20-day average with no earnings, no news (keyword scan). Assumes institutional accumulation. Enter long (or short if down-day volume spike). Stop: prior day low. Size: 0.6x Kelly. Hold: 2–7 days.

**A8 / Multi-Timeframe Momentum Confluence:**
Only fires when 4 timeframes (5m, 15m, 1h, daily) all agree on direction. Checks EMA alignment and MACD histogram sign on each. A confluence score (0–4) is calculated; signals only on score = 4. High conviction: sized at 1.2x Kelly. Regime: any except CRASH_RISK.

**A9 / Options Flow Momentum (Equity Trigger):**
When `options_flow_scanner.py` detects a bullish sweep (volume > OI * 2, net premium > $100k, calls/puts > 3.0), buys the underlying equity. If bearish sweep: buys puts (if options_enabled) or short-sells (if PDT allows). Stop: 3% adverse move. Hold: 1–3 days. Regime: BULL_TREND, SIDEWAYS_LOW_VOL.

**A10 / Pre-Market Momentum Scanner:**
Runs at 8:30 AM ET. Scans for stocks up > 4% on pre-market volume > $1M, with a positive catalyst (earnings beat, FDA approval, analyst upgrade detected via keyword scan). Queues these for A3/Gap-and-Go or A8 monitoring at open.

**A11 / HALT Resume Strategy:**
Monitors all NASDAQ/NYSE halts via feed. When a regulatory halt (LULD circuit breaker or news pending) resumes, enters the first 5-minute candle after resumption if the price is above HALT_PRICE and volume is > 5x normal. Stop: resumption low. Very small size (0.35x Kelly). High-risk, high-reward.

**A12 / Market-on-Close Imbalance Capture:**
After 15:40 ET, monitors NYSE's published MOC imbalance feed (available via Polygon or IBKR). If imbalance indicates significant buy orders for a liquid stock (imbalance > 0.5% of float), enters a position to benefit from the closing print. Exits at MOC.

**A13 / Bid-Ask Tape Reading:**
Requires `level2_enabled = true`. Monitors `bid_ask_imbalance` and `aggressor_ratio` from `level2_data.py`. BUY when imbalance > 0.35 (heavy bid) and aggressor_ratio > 0.60 (buyers initiating). Filters to stocks already in an uptrend (EMA-9 > EMA-21). Tight 0.75*ATR stop. 30-minute max hold.

**A14 / Intraday Sector Rotation (30-Min Granular):**
Finer-grained version of EQ-06. Uses the 30-min sector momentum signal but combines it with the current HMM regime state for size multiplier. In BULL_TREND: 1.2x Kelly. In SIDEWAYS_HIGH_VOL: 0.5x Kelly. Also rotates between sub-sector ETFs (e.g., XLK → IGV software, SOXX semiconductors).

**A15 / Key Level Reversal (Pivot Points):**
Calculates daily Pivot Points (R1, R2, S1, S2) using prior day's OHLC. Enters long at S1/S2 with RSI < 40 and price showing bullish reversal candle (hammer, engulfing). Enters short at R1/R2 with RSI > 60 and bearish reversal. Stop: 2 ticks beyond the pivot level. Hold: intraday to 1 day.

**A16 / News Catalyst Momentum (Rule-Based):**
Regardless of `llm_analysis_enabled`, this strategy uses `keyword_scorer.py` to score all news headlines every 5 minutes. A headline with score > 0.75 (strong positive keywords: "beat", "raised guidance", "acquisition", "FDA approved") triggers a momentum entry if price is already moving in the positive direction. Fallback when LLM is off.

**A17 / Earnings Gap Continuation:**
The day AFTER an earnings beat (confirmed via Estimize or consensus beat), stock often continues to drift higher. Enters on the open of Day+1 if the earnings gap was > 5% up and stock is trading above the gap-open price. Stop: gap fill (prior close). Target: +5–8% additional move. Hold: 2–5 days.

**A18 / Dark Pool Accumulation:**
Requires `dark_pool_enabled = true`. When `dark_pool_volume_pct > 35%` for 3 consecutive days and price action is flat/slightly down (suggesting institutional accumulation, not distribution), enters a long position anticipating an upcoming catalyst or reveal. Stop: 3% below entry. Hold: 5–15 days.

---

### 7.2 Equity Mean Reversion — PRIMARY (EQ-03, B1–B14)

*Goal: Profit from temporary price dislocations in liquid stocks, expecting reversion to statistical mean, VWAP, or Bollinger midline.*

**EQ-03 / Bollinger Band Mean Reversion:**
BUY when `close < BBL(20,2)`, RSI-14 < 32, Stoch-K < 25, and next bar opens above BBL. SELL when `close > BBU(20,2)`. Stop: 1.5*ATR below entry. Regime preference: SIDEWAYS_LOW_VOL, SIDEWAYS_HIGH_VOL.

**B1 / Bollinger Band Squeeze Breakout:**
Detects BB Width (BBW) at 6-month low (compression). Enters on breakout: if MACD histogram turns positive → long; if turns negative → short. Stop: BBM (midline). Hold: 3–7 days. BBW < 0.04 for at least 5 days is required.

**B2 / RSI Divergence:**
Price makes new 10-day low, RSI makes a higher low. Confirmed by MACD cross-up. Enter long. Stop: new low minus 0.5*ATR. Target: VWAP or EMA-21. Reverse for bearish divergence. Both conditions must appear within the same 5-bar window.

**B3 / Oversold Large-Cap Bounce:**
S&P 500 members with RSI < 28, price < BBL, no earnings within 5 days, and sector ETF is not in a downtrend (XL* above its EMA-50). Enter long. Stop: 3% below entry. Hold: 3–7 days. Size: 1.0x Kelly. These are high-quality businesses temporarily oversold.

**B4 / Intraday VWAP Deviation:**
Fades intraday deviations > 1.5% from VWAP by 11:00 AM. Entry: price touches the +/-1.5% VWAP band AND shows reversal candle on 5-min chart. Stop: band + 0.25%. Target: VWAP retest. Close entire position by 14:30 ET.

**B5 / Monday Gap Fade:**
Fades Monday open gaps > 0.5% with no macro catalysts (check economic_events table). Sells the gap into strength in the first 10 minutes if the gap shows signs of filling (red candle on high volume). Small size (0.5x Kelly). Close by 12:00 ET.

**B6 / Statistical Z-Score Reversion:**
Calculates a 60-day rolling z-score for each stock's return relative to its own distribution. Z < -2.5: long signal. Z > +2.5: short signal. Exit at Z = 0. Uses 5-day holding period. Runs nightly across full S&P 500 universe. Regime: SIDEWAYS.

**B7 / ETF Premium/Discount Reversion:**
Monitors closed-end funds (CEFs) and leveraged ETFs for premium/discount to NAV. When discount > 5% and the fund has been profitable over 3 years, enters long expecting NAV convergence. Tracks daily NAV from fund sponsor websites. Hold: 10–30 days.

**B8 / Post-Earnings Mean Reversion:**
Specifically targets overreactions to earnings. If a stock gaps down > 8% on an earnings beat (or up > 8% on a miss), enters a counter-trend position on the NEXT trading day after the dust settles. Requires: stock is in S&P 500 (quality filter) and RSI < 35 (for long) or RSI > 65 (for short). Stop: 5% adverse from entry.

**B9 / Seasonal Calendar Reversion:**
Exploits known seasonal patterns in individual stocks and ETFs. Uses a pre-calculated seasonality database (10-year average return by month/week for each symbol). Enters long in historically strong calendar periods with additional momentum confirmation (RSI not in downtrend). Hold: calendar period duration.

**B10 / Overnight Gap Fade:**
At 9:35 AM, identifies stocks that gapped up or down > 1.5% with no material news (keyword score < 0.3). Fades the gap direction. Stop: 1.5% beyond gap open. Target: prior close (full gap fill). Signals only if first 5-min candle shows reversal. Close by 12:00 ET or on gap fill.

**B11 / Anchored VWAP Reversion:**
Calculates VWAP anchored from a major event (earnings date, 52-week high/low date, first trading day of the year). When price deviates > 3% from Anchored VWAP with RSI in overbought/oversold territory, fades the deviation. Target: Anchored VWAP. Stop: 2*ATR. Hold: 2–7 days.

**B12 / Multi-Day Oversold Accumulation:**
A stock that has declined 5+ consecutive days with RSI < 30 AND remains above its 200-day EMA (still in long-term uptrend). Enter long on the 5th consecutive down day in the last 30 minutes. Scale in over 2 days if continues down. Full position by day 2. Hold: 5–15 days.

**B13 / Option-Implied Reversion:**
When IV Rank for a stock is > 85th percentile but the 30-day realized volatility is below the 30th percentile (IV/RV ratio > 2.5), the stock is overpriced for volatility. Enters a delta-neutral short-volatility position: sell near-ATM straddle (if options_enabled) or uses a cash equity position sizing down by 40% (option-free version).

**B14 / High-Beta Reversion in Low-Vol Regimes:**
Targets the most volatile (high-beta) S&P 500 stocks when the HMM regime is SIDEWAYS_LOW_VOL. These stocks overshoot in both directions during low-vol regimes but snap back faster. Enters when beta-adjusted RSI < 25. Sized at 0.6x Kelly. Stop: 2.5*ATR. Hold: 2–5 days.

---

### 7.3 Copy Trading & Sentiment — PRIMARY (D1–D16)

*Goal: Piggyback on information advantages from insiders, Congress, institutions, social media, and smart-money options flow.*

**D1 / Congress Trade Replication:**
Scrapes `housestockwatcher.com` and `senatestockwatcher.com`. Replicates purchases > $15,000 within 48 hours of public filing. Size: 1% NAV. Holds for 30 days unless stop triggered. Preference for purchases by committee chairs with oversight of relevant industries.

**D2 / Insider Cluster Buy:**
Scrapes OpenInsider. Triggers if 3+ officers/directors buy > $50,000 each in the open market within 14 days. Stronger signal if buying is by the CEO or CFO (2x size). Stop: 5% below average insider cost. Hold: 20–60 days.

**D3 / FinBERT Sentiment (Always On):**
Runs `ProsusAI/finbert` on NewsAPI headlines every 30 minutes. BUY if rolling 4-headline average > 0.60. SELL if < -0.40. Requires volume confirmation (> 1.2x average). Includes intraday news (PRE_MARKET and DURING_MARKET windows).

**D4 / WSB Reddit Momentum:**
Scans `r/wallstreetbets`, `r/stocks`, `r/investing`, `r/options`, `r/RobinHoodPennyStocks` via PRAW every hour. Triggers if `mention_velocity = (today_mentions - avg_7d_mentions) / avg_7d_mentions > 3.0` AND short float > 10% (squeeze potential). Size: 0.5x Kelly. Stop: 8%. Hold: 1–3 days.

**D5 / Google Trends Catalyst:**
Maps rising search velocity for category keywords to relevant ETFs and stocks. Examples: "buy gold" → GLD; "electric vehicle" → TSLA/RIVN/NIO; "bank run" → short XLF; "AI" → NVDA/MSFT. Velocity trigger: 7-day trend > 200% of 30-day average. Hold: 3–7 days.

**D6 / Dark Pool Flow Tracker:**
Requires `dark_pool_enabled = true`. Tracks daily dark pool volume percentage. When `dark_pool_pct > 40%` for a large-cap stock accompanied by net positive price movement, classifies as accumulation. When same conditions but price declines: distribution. Accumulation → queue for momentum entry. Distribution → flag existing position for early exit review.

**D7 / Institutional 13F Position Builder:**
Tracks 30 top hedge funds' SEC EDGAR quarterly 13F filings. Identifies new positions and position increases. Buys within 15 trading days of filing date (reduced from 30 in v1.0 for faster execution). Priority given to funds with strong prior track records (tracked in `fund_performance` table). Size: 0.75% NAV.

**D8 / Unusual Options Activity (UOA) → Equity Signal:**
The `options_flow_scanner.py` feeds this strategy directly. When a BULLISH_SWEEP is detected (call volume > 3x OI, premium > $200k, > 30 DTE), enters the underlying equity long. BEARISH_SWEEP → short or avoid. Confirmation: stock must be near technical support/resistance for the trade to be valid. Stop: 4%. Hold: 3–10 days.

**D9 / SEC Form 4 Velocity Escalation:**
Beyond simple cluster detection, tracks the VELOCITY of insider buying over quarters. If the same executive has been increasing purchase size quarter-over-quarter for 3 consecutive quarters, treats it as a conviction escalation signal. Larger position (1.5% NAV). Hold: 60 days.

**D10 / Short Squeeze Probability Score:**
Calculates a composite short squeeze score: `(short_float_pct * 0.35 + days_to_cover * 0.25 + borrow_cost * 0.20 + options_call_volume_ratio * 0.20)`. Score > 75 → adds to a short-squeeze watchlist. When one of these names shows unusual volume (> 2x) AND a bullish technical breakout (price > 20-day high), enters with a tight 5% stop. Hold: 1–5 days.

**D11 / Analyst Upgrade Momentum:**
Monitors major bank upgrades (Goldman, Morgan Stanley, JP Morgan, Bernstein) via NewsAPI keyword filter and Benzinga API. An upgrade from "Hold" or "Sell" to "Buy" or "Strong Buy" from a tier-1 analyst triggers within 15 minutes of market open on announcement day. Stop: 3% below announcement open. Hold: 5–10 days.

**D12 / Social Sentiment Divergence:**
When stock price is declining but social sentiment score (FinBERT + Reddit composite) is strongly positive (> 0.65) for 3+ consecutive days, enters a long position betting on sentiment-driven reversal. Reverse for bearish divergence. Requires stock to be in S&P 500 (prevents micro-cap manipulation). Stop: 6%.

**D13 / ETF Flow Signal:**
Uses ETF daily flow data (from ETF.com API or manual scraping). When a sector ETF receives inflows > $500M in a single day (significant institutional rotation), enters the top 3 holdings of that ETF. Reverse for large outflows. Hold: 3–7 days.

**D14 / Earnings Whisper vs Consensus Gap:**
When Estimize crowd consensus EPS estimate is > 8% above the Street consensus AND call-volume-to-put-volume > 2.5 in the 2 weeks before earnings, enters a small pre-earnings long (0.4x Kelly). Exits the day before earnings (avoids IV crush and earnings risk directly). Profit comes purely from pre-earnings run-up.

**D15 / Institutional Block Trade Detector:**
Monitors the tape for prints > $1M in a single transaction in liquid large-cap stocks. Three block buys within 2 hours at or above the offer price indicates institutional accumulation urgency. Enters long on confirmation of the third block. Stop: prior block trade price. Hold: 1–3 days.

**D16 / Supply Chain Contagion Signal:**
Uses the `supply_chain_graph.json`. When a major company reports a supply constraint, shortage, or pricing power (keyword detection in earnings call transcripts), identifies its top suppliers and enters them long (or major customers short if cost pressures are upstream). Hold: 7–14 days.

---

### 7.4 Quantitative & Statistical Arbitrage — PRIMARY (EQ-02, E1–E16)

*Goal: Exploit statistical mispricings, factor exposures, mean-reverting spreads, and structural market anomalies.*

**EQ-02 / Stat Arb Pairs Trading:**
Runs Engle-Granger cointegration test (p < 0.05) on 500+ ETF and stock pairs from the same sector. Calculates spread z-score (60-day rolling mean/std). BUY leg A / SELL leg B if z < -2.0. Exit at 0. Stop: z < -3.5 (spread diverging further). Refreshes pairs universe weekly.

**E1 / Cointegration Portfolio (3-Leg Basket):**
Extension of EQ-02 to 3-asset baskets using Johansen cointegration. Examples: `[XLE, XOM, CVX]` or `[QQQ, NVDA, AMD]`. Constructs a stationary portfolio using eigenvector weights. Trades when portfolio value z-score > 2.0. More complex but higher capacity than pairwise arb.

**E2 / Volatility Regime Switching:**
`RV_IV_ratio = 20-day_realized_vol / VIX`. If ratio < 0.70: premium selling (sell iron condors, covered calls). If ratio > 1.30: premium buying (buy straddles/strangles). If options_enabled=false: uses leveraged inverse ETF positions (SVXY/UVXY) as a proxy. Regime: any except CRASH_RISK.

**E3 / Cross-Asset Correlation Breakdown:**
Tracks 20-day rolling correlations: BTC/NASDAQ, Gold/USD, Oil/XLE, Bonds/Equities. When a pair's correlation deviates > 2.0 SD from its 1-year mean, enters a pair trade betting on convergence. Sized at 0.5x Kelly (lower conviction; timing of convergence is uncertain). Stop: correlation diverges another 1 SD.

**E4 / ETF NAV Arbitrage:**
Monitors the premium/discount of ETFs to their intraday indicative NAV (iNAV). When discount > 0.3% for a liquid ETF, buys the ETF (and hedges with the basket if IBKR is available). When premium > 0.3%, sells. Primarily a statistical signal for liquid equity ETFs (SPY, QQQ, IWM). Position closed by EOD.

**E5 / Factor Momentum (5-Factor Model):**
Scores S&P 500 universe on: Value (P/E, P/B, EV/EBITDA), Momentum (12-1 month return), Quality (ROE, debt/equity, earnings stability), Low Volatility (60-day beta), and Size (market cap). Long top quintile of composite factor score, short bottom quintile. Rebalances monthly. Hold: 20–30 days.

**E6 / Lead-Lag Sector Analysis:**
Measures lag correlation between all sector pairs. When a leading sector (e.g., Tech) has moved up strongly over 3 days and a historically lagging sector (e.g., Consumer Discretionary) has not yet followed, enters the lagging sector long. Signal is validated by checking that the lagging sector is in the early phase of its own MACD cross.

**E7 / Put-Call Parity Violation:**
Monitors options chains for put-call parity deviations: `C - P ≠ S - K*e^(-rT)` after accounting for dividends. A deviation > 0.3% (net of transaction costs) indicates a synthetic arb opportunity. Executes if IBKR is available (lowest options commissions). Very small positions; purely arbitrage in nature.

**E8 / Calendar Spread Statistical Arbitrage:**
Exploits the historically mean-reverting spread between front-month and back-month VIX futures (via VXX/VXZ ETFs as a proxy). When VXX/VXZ ratio exceeds its 90th percentile (strong contango), short VXX / long VXZ. Reverse when below 10th percentile (backwardation). Stop: spread moves another 10%. Hold: 5–15 days.

**E9 / S&P 500 Index Rebalance Arbitrage:**
S&P 500 additions must be bought by all passive funds before the effective date (announced ~5 days prior). Buys the announced addition within 1 hour of announcement. Sells on the effective date close or at a 2% profit, whichever comes first. Historical win rate > 70%.

**E10 / Options Dispersion Trading:**
When index implied volatility (VIX) is significantly higher than the average implied volatility of the index's components (high dispersion premium), sells index volatility and buys component volatility. Implemented as: sell SPX/SPY iron condor, buy individual stock straddles on top 20 constituents. Requires `options_enabled = true`.

**E11 / PCA Factor Breakout:**
Runs rolling PCA on 30-day returns of the S&P 500. Identifies the top 3 principal components and their current z-scores. Trades the first PC (market beta factor) when its z-score > 2.0: if PC1 is strongly positive, buys high-beta stocks; if strongly negative, buys low-beta defensives. Regime-neutral strategy.

**E12 / Kalman Filter Dynamic Pairs:**
Uses a Kalman filter (via `filterpy`) to estimate the time-varying hedge ratio in a pairs trade, rather than a fixed OLS beta. This allows the hedge ratio to adapt as the relationship between two correlated stocks evolves. More accurate position sizing than static EQ-02 approach. Pairs universe: sector-matched large-caps.

**E13 / HMM State-Transition Arbitrage:**
Uses the regime probability distribution from the Meta-Brain's HMM. Trades the *transition* between regimes rather than within them. When regime probability shifts from < 20% to > 60% for a new state within one week, enters a position that benefits from the new regime's characteristics before the full market repricing. Fast execution required.

**E14 / Volatility Surface Arb (Skew Trade):**
Monitors options IV surface for anomalies. When put-skew (25-delta put IV / 25-delta call IV) is in the top 10% historically AND realized skew is normal, the puts are relatively overpriced. Sells OTM puts, buys OTM calls to capture the skew normalization. Requires `options_enabled = true`.

**E15 / Correlation Regime Arbitrage:**
During regime transitions (identified by HMM), cross-asset correlations tend to spike and then normalize. Trades this normalization: when 30-day equity-bond correlation exceeds its 2-year high (risk-off spike), buys both equities and bonds expecting decorrelation. Stop: correlation remains elevated for > 10 days.

**E16 / Risk Premium Harvesting (Multi-Asset Carry):**
Systematically collects carry across multiple asset classes simultaneously:
- Equity carry: dividend yield > 10-year treasury.
- Credit carry: IG corporate bonds vs treasuries.
- Volatility carry: VIX futures roll-down (when term structure is in contango).
- Commodity carry: commodity futures in backwardation.
All positions sized to equal risk contribution. Hold: 30 days, rolled.

---

### 7.5 Macro & Thematic Strategies — PRIMARY (F1–F18)

*Goal: Capitalize on macroeconomic data releases, central bank policy, geopolitical events, and long-term thematic shifts.*

**F1 / Rate-Sensitive Sector Rotation:**
If 10Y Treasury yield rises > 5 bps in a single day: rotate from XLK (Tech) → XLF (Financials). If rises > 10 bps: add XLV (Healthcare) and XLE (Energy). If yield falls > 5 bps: reverse. Checked daily at 10:00 AM. Positions held 3–7 days.

**F2 / VIX Mean Reversion:**
VIX > 30: buy SPY (market will recover). VIX < 12: buy VXX (volatility is suppressed and will snap back). VIX 25–30 with declining trend: scale into SPY. Regime filter: CRASH_RISK regime disables the SPY buy leg (crisis can persist). Position size scales with VIX level.

**F3 / Fed FOMC Calendar Trade:**
3 days before FOMC meeting: buy VXX (pre-FOMC uncertainty premium). On FOMC day morning: sell VXX at open. After Fed statement (14:30 ET): trade in direction of the market's initial 5-minute reaction IF it's > 0.5% in either direction (confirmation required). Hold post-FOMC directional for 2 days.

**F4 / CPI/PPI Release Reaction:**
1 day before CPI/PPI release: buy straddle on TLT (if options_enabled) or reduce equity/bond exposure. On release: if CPI > consensus by > 0.2%: buy XLE, XLB (energy/materials), short TLT. If CPI < consensus by > 0.2%: buy TLT, XLK, reduce XLE. Confirmation: wait 15 minutes post-release before entering.

**F5 / Gold/Dollar Inverse Correlation:**
If DXY (dollar index via UUP ETF proxy) falls > 0.5% in a day: buy GLD. If DXY rises > 0.5%: sell GLD or buy UUP. Enhanced: adds GDX (gold miners) for leverage when signal strength > 0.8. Correlation monitored rolling 60 days; signal disabled if correlation drops below 0.60.

**F6 / Commodity-to-Equity Lagged Signal:**
If Oil futures (CL via USO ETF) rise > 1.5%: buy XLE same day. If copper (HG via COPX ETF) rises > 1%: buy XLB and industrial plays (CAT, DE). If Nat Gas (UNG) spikes > 3%: buy utility equities (XLU) cautiously (inverse relationship). Hold: 3–5 days.

**F7 / Yield Curve Shape Strategy:**
Monitors 10Y–2Y spread (from FRED). If spread steepens > 20 bps over 5 days (bear steepener): long XLF (banks benefit from wider NIM). If flattens > 20 bps (curve inversion building): defensive rotation to XLV, XLU. If inversion resolves (un-inverts rapidly): buy cyclicals (XLI, XLY). Hold: 5–15 days.

**F8 / NFP Jobs Data Reaction:**
First Friday of each month. 30 minutes before release (8:00 AM ET): reduce all open positions by 50% (risk management). On release at 8:30 AM: if NFP > consensus + 100K: BUY QQQ, SPY at 9:35 AM open (risk-on). If NFP < consensus - 100K: BUY TLT, VXX (risk-off). No trade if within 50K of consensus. Hold: 2–3 days.

**F9 / PMI/ISM Regime Signal:**
Monthly ISM Manufacturing PMI. PMI > 55 (expansion): long XLI (industrials), XLB (materials), XLK. PMI 50–55: neutral. PMI < 50 (contraction): long XLV, XLU; reduce cyclical exposure. Signal updated monthly, blended with the HMM regime for a combined macro-technical composite score.

**F10 / Geopolitical Risk Premium:**
Monitors geopolitical event keywords (via keyword_scorer.py) across NewsAPI: "conflict", "sanctions", "blockade", "military", "OPEC". When geopolitical risk score spikes > 3 SD from 30-day average: buy GLD, XLE (energy security), reduce equity beta by 20%. Reverse when score normalizes. Hold: 3–7 days.

**F11 / Earnings Season Sector Rotation:**
Historical pattern: certain sectors outperform in the 2 weeks before and during their earnings season. Example: Technology sector → buy XLK 2 weeks before the major tech reports start. Financial sector → buy XLF 2 weeks before bank earnings. Pre-loaded calendar in `economic_events` table. Size: 1.5% NAV per sector ETF. Hold through earnings season peak.

**F12 / Seasonal Macro Calendar:**
Exploits calendar effects with > 10-year statistical significance:
- "Sell in May" effect (May–October underperformance): rotate to defensive XLV, XLU in late April.
- Santa Claus Rally (last 5 trading days + first 2 of new year): buy SPY.
- January Effect (small-caps outperform): buy IWM in late December.
- September Weakness: reduce equity beta in August.
- Pre-election year rally: increase equity beta in year 3 of presidential cycle.

**F13 / Credit Spread Equity Signal:**
Monitors Investment Grade (LQD) and High Yield (HYG) spread to treasuries via ETF price ratio: `HYG / TLT`. When this ratio falls sharply (credit spreads widening), reduces equity exposure and buys defensive positions. When ratio recovers (spreads tightening), re-enters risk assets. Threshold: 2 SD move over 10 days.

**F14 / Emerging Market / Developed Market Divergence:**
Tracks EEM (Emerging Markets) vs SPY relative strength. When EEM outperforms SPY by > 5% over 20 days: buy EEM, reduce domestic equity. When EEM underperforms by > 5%: buy DM quality (SPY, QQQ). Also tracks DXY as a correlate: weak dollar often supports EM. Hold: 10–20 days.

**F15 / Inflation Regime Multi-Asset:**
Classifies current inflation environment: DISINFLATION (CPI falling, below 2%), MODERATE (2–3%), ELEVATED (3–5%), HIGH (> 5%). Each regime has a preset asset allocation tilting:
- DISINFLATION: Long growth (QQQ, XLK), long duration bonds (TLT).
- MODERATE: Balanced. Mixed equity, medium-duration.
- ELEVATED: Long TIPS, XLE, XLB, GLD. Reduce TLT.
- HIGH: Inflation fighters only: GLD, commodities, TIPS, short TLT.

**F16 / Central Bank Policy Divergence:**
When the Fed is raising rates while ECB is cutting (or vice versa), trades the resulting FX and equity divergence. Fed hiking → long USD (UUP), potentially short European equities (IEV). Fed cutting while ECB holding → short USD, long EEM. Monitored via FRED interest rate feeds. Hold: 10–30 days.

**F17 / Commodity Futures Roll Yield:**
Tracks the term structure of commodity futures (WTI, Nat Gas, Gold, Copper) via ETF proxies. When a commodity is in backwardation (spot > futures), there is a positive roll yield: buy the commodity ETF and hold for roll gain. When in extreme contango: avoid or short the ETF. Hold: 15–30 days.

**F18 / Housing Market Sensitivity Trade:**
When housing starts or pending home sales miss consensus by > 10%, enters short XLY (consumer discretionary), short ITB (homebuilders). When they beat: long ITB, XLY, and consider HD/LOW. Uses monthly calendar from `economic_events` table. Waits for 15-minute confirmation after release before entering.

---

### 7.6 Cash Management & Hedging — PRIMARY (CM-01–CM-12, EQ-04)

*Goal: Maximize cash yield during idle periods, maintain portfolio-level risk controls, and actively hedge tail risk with minimal drag on returns.*

**CM-01 / Money Market Sweep:**
At 15:50 ET daily, if cash balance > $1,000 + `CASH_BUFFER ($500)`, buys the highest-yielding available money market fund: SWVXX (Schwab), SPRXX (Fidelity), or VMFXX (Vanguard), in order of current 7-day yield. Sells next morning at 9:31 AM. Estimated annual drag of 0, gain of ~5% annualized on idle cash.

**CM-02 / Static Hedge Ladder:**
Maintains a passive hedge: 1–2 far OTM SPY puts (5% OTM, 30–60 DTE). Cost: ~2–3% annualized. Increased to 3–4 puts (full ladder) when HMM regime is BEAR_TREND or CRASH_RISK. Allocates 5–10% to SQQQ when BEAR_TREND or CRASH_RISK persists for > 3 consecutive days.

**EQ-04 / Flash Crash Buy Ladder:**
At 09:28 AM, places 5 GTC limit BUY orders for SPY and QQQ at: -5%, -8%, -12%, -16%, -20% below prior close. Each order is 0.5% NAV. All cancelled at 10:00 AM if not triggered. If triggered, holds for rebound to -3% level (vs prior close) or stop at -25% (further crash).

**CM-03 / Dynamic Portfolio Beta Hedge:**
Calculates portfolio beta (weighted sum of individual stock betas relative to SPY) every 30 minutes during market hours. If portfolio beta > 1.2 (over-leveraged to market moves), automatically reduces beta by selling the highest-beta position or buying SPY puts. Target beta: 0.85–1.05 in BULL_TREND; 0.40–0.70 in BEAR_TREND.

**CM-04 / VIX Term Structure Ladder:**
Monitors VIX9D (9-day), VIX (30-day), VIX3M (3-month), VIX6M (6-month) term structure. When the term structure is in steep contango (VIX << VIX3M), a VIX spike is less likely: reduce hedge allocation. When VIX3M < VIX (backwardation or inversion), an imminent spike is more likely: increase SPY puts and SQQQ allocation. Checked daily.

**CM-05 / Volatility Target Overlay:**
A cross-cutting overlay applied to ALL strategies simultaneously. Calculates 20-day realized portfolio volatility daily. If portfolio vol > `VOL_TARGET (15% annualized)`: multiplies all position size recommendations by `scaling_factor = VOL_TARGET / portfolio_vol`. If portfolio vol < 10%: scales up to `1.25x`. This is a passive risk governor that acts independently of individual strategy signals.

**CM-06 / T-Bill Ladder Optimizer:**
For capital not deployed in active positions, constructs an optimal ladder of T-Bills (4-week, 3-month, 6-month) using IBKR's treasury direct access or secondary market. Maximizes yield across the ladder while maintaining liquidity to fund positions within 2 trading days. Implemented via FI-02 fixed-income strategy.

**CM-07 / Tail Risk Protection (OTM Puts + VIX Calls):**
More aggressive hedge than CM-02. In addition to SPY puts, buys OTM VIX calls (1-2 strikes OTM, 30 DTE) as a crisis hedge. VIX calls appreciate most during sudden sell-offs (unlike SPY puts which suffer from IV spike cost). Allocation: 0.5% NAV per month. Hedges repurchased on expiry or after any profitable use.

**CM-08 / Correlation Breakdown Hedge:**
Normally, portfolio diversification assumes correlations hold during stress. This strategy activates when portfolio correlation spike is detected (the average pairwise correlation of all holdings rises above 0.75). At that point, the system liquidates the 3 most correlated positions (reduces clustering risk) and parks capital in uncorrelated assets (GLD, TLT, short-volatility ETFs depending on regime).

**CM-09 / Delta-Neutral Cash Parking:**
When a significant options position exists, this strategy maintains a near-delta-neutral portfolio by actively adjusting the hedge ratio using the underlying equity. Monitors net portfolio delta every 30 minutes. If |net_delta| > threshold (0.15 * NAV equivalent), places a delta-reducing equity order. Prevents large mark-to-market swings from directional exposure in options book.

**CM-10 / Maximum Diversification Rebalancer:**
Uses Riskfolio-Lib's Maximum Diversification Ratio (MDR) optimization. Runs weekly (Saturday) to rebalance positions to maximize the diversification ratio (portfolio weighted-average volatility / portfolio volatility). This systematically reduces concentration in correlated assets. Minimum hold of 5 days enforced to avoid wash sales and excessive turnover.

**CM-11 / Drawdown Circuit Breaker Ladder:**
An enhanced version of the existing drawdown halt that operates in tiers:
- Drawdown > 2%: Reduce new position sizing by 25%. Log WARN.
- Drawdown > 4%: Reduce all position sizes to 50%. Close all intraday positions.
- Drawdown > 6%: Close all positions except CM hedges and money market. SOFT HALT.
- Drawdown > 8%: Emergency liquidation. HARD HALT. Alert sent via all notification channels.
Drawdown tracks from the prior ATH (all-time high of the rolling 30-day equity curve), not just daily.

**CM-12 / Margin Utilization Optimizer:**
Monitors real-time margin usage from `get_margin_status()`. If margin_used / margin_available > 0.75 (approaching limits), automatically de-levers the most expensive-to-carry positions first (highest margin requirement per dollar of expected return). If margin_used / margin_available > 0.90: immediately reduces 20% of all leveraged positions. Prevents forced liquidation by brokers.

---

### 7.7 Options Strategies (OP-01–OP-12, C4, C6–C9)

*(All v1.0 strategies retained; new additions below. All require `options_enabled = true`)*

**OP-07 / Iron Butterfly (High-IV, Directional Bias):**
When IV Rank > 70% and the stock has a clear near-term directional bias (strong momentum signal from A-series), uses an asymmetric iron butterfly: wider wing on the direction of bias. Captures more premium if move is in the expected direction while limiting loss if wrong.

**OP-08 / Jade Lizard (Bullish, No Upside Risk):**
Sells an OTM put + OTM call spread. Credit received > width of call spread, eliminating upside risk entirely. Ideal when IV is elevated and the stock is expected to move sideways to moderately higher. Entry: IV Rank > 65%, stock above 50-day MA.

**OP-09 / Calendar Spread (Theta + Gamma):**
Buys far-dated ATM call (90 DTE), sells near-dated ATM call (30 DTE) for same strike. Profits from: (1) faster theta decay of short leg, (2) IV increase (if IV expands, long leg benefits more). Close when short leg approaches 21 DTE (roll forward).

**OP-10 / Diagonal Spread (Synthetic Collar):**
Buys ITM long-dated call (120 DTE, 0.70 delta), sells OTM short-dated call (30 DTE, 0.35 delta). Lower cost than covered call with similar income generation. Used when stock is in a moderate uptrend and options are modestly expensive.

**OP-11 / Long Volatility Strangle (Pre-Event):**
Before major catalysts (earnings, FDA decisions, legal verdicts): buys OTM call + OTM put (strangle) at approximately equal delta (0.25 each). Profit if stock moves > combined premium in either direction. Enter 7–10 days before event (before IV ramp fully bakes in). Exit day before event or at 2x premium.

**OP-12 / Short Gamma Scalping:**
Sells near-ATM straddle (short gamma position). Delta hedges by buying/selling underlying equity on every 0.10 delta move. The theta collected from the straddle should exceed the cost of delta hedging. Computationally intensive; runs as a separate async task with 5-minute monitoring loop. Requires: SIDEWAYS_LOW_VOL regime, IV Rank > 50%.

**C7 / Ratio Spread (Cheap Directional Bet):**
Buys 1 ATM call, sells 2 OTM calls (1:2 ratio). Net debit is minimal or zero. Profits if stock moves to the short strikes and stays there. Risk is upside beyond 2x the OTM strike (capped by buying a further OTM call to create a modified condor). Uses for moderate upside expectations without paying full premium.

**C8 / Protective Collar on Core Holdings:**
For long equity positions held > 30 days with significant unrealized gains, constructs a collar: buy OTM put (5% OTM, 60 DTE) + sell OTM call (10% OTM, 60 DTE). Net cost near zero (call premium offsets put cost). Locks in 5–10% profit band. Avoids constructive sale rules by ensuring the short call is not too deep ITM.

**C9 / Wheel Strategy:**
On target stocks (high IV, bullish fundamental view, OK to own): Step 1: Sell cash-secured put (C4). Step 2: If assigned (stock drops below strike), now owns stock. Step 3: Sell covered call (OP-03). Step 4: If called away at profit, restart at Step 1. Fully automated wheel cycle managed in `wheel_cycle_log` table.

---

### 7.8 Crypto, FX & Fixed Income (CR-01–CR-07, FX-01–FX-05, FI-01–FI-04)

*(All require respective `crypto_enabled` / `fx_enabled` / `fi_enabled` flags)*

**CR-05 / BTC Halving Cycle Model:**
Tracks the Bitcoin 4-year halving cycle. Uses a combination of: days since last halving, Stock-to-Flow (S2F) model deviation, and realized cap vs market cap ratio. Generates a long-term positioning signal (multi-week hold). Conservative sizing.

**CR-06 / Crypto Fear & Greed Contrarian:**
The Crypto Fear & Greed Index (scraped from alternative.me API). Extreme Fear (< 20): accumulate BTC/ETH. Extreme Greed (> 80): reduce exposure or short. Mean reversion approach applied to crypto sentiment.

**CR-07 / DeFi Yield Capture:**
Monitors DeFi lending rates (via Aave, Compound APIs via `web3.py`). When stable coin lending APY > 6%, deploys idle USDC to earn yield while awaiting entry signals. Automated within the AQTA cash management framework.

**FX-02 / Dollar Strength Overlay:**
When DXY is rising > 0.5%/week: tilts global equity holdings toward US-domestic revenue companies (reduces ADR/EEM exposure). When DXY falls: increases EM and international exposure.

**FX-03 / Currency Momentum:**
Ranks G10 currencies by 1-month momentum. Long top 2, short bottom 2 via ETF proxies (FXE, FXY, FXB, FXC, FXA).

**FX-04 / Carry + Momentum Combo:**
Combines G10 carry (yield differential) with momentum. Highest-carry-AND-momentum currencies get 1.5x allocation. Lowest: 0.5x or short.

**FX-05 / Volatility-Adjusted Carry:**
Scales FX carry positions by implied volatility. If FX vol is elevated (> 1-year 80th percentile), reduces carry exposure by 50% (carry unwinds are more violent in high-vol environments).

**FI-02 / Treasury Yield Momentum:**
Trades in the direction of 10Y yield momentum (20-day trend). Yield rising → short TLT, buy TBF. Yield falling → long TLT. Stop: 3% adverse move on position.

**FI-03 / TIPS Inflation Protection:**
When CPI month-over-month > 0.3% (above trend), buys TIPS (TIP ETF) and reduces nominal bond exposure. Rebalanced after each monthly CPI release.

**FI-04 / Municipal Bond Spread Play:**
When Muni/Treasury yield ratio > 0.85 (munis are cheap vs taxable equivalents), especially for investors in high tax brackets, systematically allocates a portion of bond exposure to MUB (municipal bond ETF). Tax-adjusted yield calculation used.

---

## 8. RISK MANAGEMENT & COMPLIANCE ENGINE

The `RiskManager` executes an ordered 15-step pipeline (`engine/risk/risk_manager.py`). Any failed check blocks the order, logs to `compliance_audit_log`, and returns a `RiskCheckResult(passed=False, reason=...)` to the caller.

---

### 8.1 Pre-Trade Risk Pipeline (15 Steps)

1. **System Halt:** Blocks if `control_flags["trading_enabled"] == "false"`.
2. **Shadow Mode:** Reroutes to MockBroker if `shadow_mode == "true"`.
3. **Emergency Halt:** Blocks ALL new entries if drawdown > 8% (CM-11 threshold).
4. **PDT Rule (FINRA 4210):** Counts FILLED trades with hold_time < 1 day in last 5 calendar days. Blocks 4th trade if total equity < $26,500. Offers `PDT_EQUITY_BUFFER` alert via notification center.
5. **Wash-Sale (IRC §1091):** Checks `wash_sale_blacklist`. Blocks BUYs if expiry > today. For loss SELLs: offers proxy swap scored by `proxy_score` (prefer proxies with score > 0.8).
6. **Position Concentration:** Resizes order if `order_value / total_equity > MAX_SINGLE_POSITION_PCT (0.10)`.
7. **Sector Concentration:** Blocks if sector exposure > `MAX_SECTOR_PCT (0.35)`. Uses Polygon symbol details for sector classification.
8. **Liquidity Filter:** Blocks if `order_qty * fill_price > 0.05 * avg_daily_volume_usd` (20-day ADTV).
9. **Portfolio Correlation:** Calculates 60-day Pearson correlation. Warns if > 0.75 with existing holdings. Blocks if > 0.90 (near-identical exposure).
10. **Asset Class Toggles:** Blocks CRYPTO if `crypto_enabled == "false"`, OPTION if `options_enabled == "false"`.
11. **Intraday Drawdown:** If > 2.0%: blocks new entries. If > 4.0%: liquidates all intraday positions.
12. **Leverage (Reg-T):** Blocks if `total_notional / total_equity > MAX_LEVERAGE (2.0x overnight, 4.0x intraday)`.
13. **Portfolio Greeks Limits (NEW):** Checks net portfolio Delta, Gamma, Theta, Vega against configurable limits. Blocks options trades that would push any Greek beyond its limit. Configurable: `MAX_NET_DELTA = ±0.3 * NAV_equivalent`.
14. **Margin Utilization (NEW):** Blocks orders if `margin_used / margin_available > 0.85` (15% safety buffer).
15. **Insider Trading Guardrail:** Cross-references with `insider_trading_watchlist` table. Blocks trading in tickers flagged by LLM-extracted SEC 8-K material events (or keyword-detected 8-Ks when LLM is off) for 72 hours.

---

### 8.2 Real-Time & Post-Trade Risk

- **ATR Trailing Stops:** Updated every 5 minutes during market hours. `stop = current_close - (ATR_MULTIPLIER * ATR-14)`. ATR multiplier: 2.0x by default; 1.5x in BEAR_TREND; 2.5x in BULL_TREND (give more room).
- **Profit-Lock Ratchet:** Position at +15% unrealized PnL: stop ratchets to +7%. At +25%: stop ratchets to +15%. At +40%: stop at +30%. Ensures locked profits compound.
- **Greeks Monitoring (NEW):** `greeks_monitor.py` runs every 5 minutes during market hours. Recalculates all portfolio Greeks. Sends WARN if any Greek approaches 80% of its limit. Sends ALERT at 95%.
- **Margin Optimizer (NEW):** `margin_optimizer.py` runs every 30 minutes. Ranks all leveraged positions by `(expected_pnl * probability) / margin_requirement`. Positions with the worst risk-adjusted margin efficiency are flagged for potential early closure when margin is constrained.
- **Reg SHO Locate:** Short-sale locate verification with prime broker API before any short entry.
- **MiFID II Best Execution Logging:** All venue quotes considered before routing are saved to `orders.venue_quotes_json`.

---

## 9. TAX OPTIMIZATION ENGINE

*(v1.0 fully retained; enhancements below)*

---

### 9.1 Enhanced Lot Selection Intelligence

*(v1.0 logic retained: FIFO, HIFO, LTCG_FIRST, LOSS_FIRST)*

**NEW — AMT Impact Assessor:** Before selecting HIFO or LOSS_FIRST methods, the engine checks whether the trader is subject to AMT (Alternative Minimum Tax) by estimating AMTI. ISO options exercise gains are included. If AMT exposure is projected, lot selection adjusts to avoid accelerating AMT preferences.

**NEW — Proxy Intelligence Scoring (`proxy_score`):** When a wash-sale proxy swap is required, the engine scores candidate proxies on:
- Price correlation with the sold security (60-day): 40%
- Sector match: 20%
- Beta similarity: 20%
- Liquidity (ADTV ratio): 20%
Proxies with score < 0.60 are rejected and the system holds cash instead (avoids a poor substitute driving unexpected P&L).

---

### 9.2 Tax-Loss Harvesting & Proxy Swaps

*(v1.0 logic retained; enhancements)*
- **TLH Trigger Threshold:** Lowered from -$500 to `-$300` in December (more aggressive year-end harvesting).
- **Opportunity Cost Analysis:** Before executing TLH, the engine calculates the *opportunity cost* of being out of the position for 31 days (wash-sale waiting period) using the symbol's average annual return / 12. Only executes TLH if `estimated_tax_saving > opportunity_cost * 1.2`.

---

### 9.3 Gain Deferral Optimizer

*(v1.0 logic retained; enhancements)*
- Enhanced to also consider the option to write an OTM covered call as an alternative to buying a protective put (lower cost, but with upside cap). Evaluates 3 strategies: (1) hold unhedged, (2) buy protective put, (3) write covered call. Selects the highest after-tax expected value.

---

### 9.4 Estimated Tax Payment Planner

**NEW.** The `tax_reporter.py` module maintains running estimates for quarterly tax obligations:
- Aggregates STCG, LTCG, dividends, and ordinary income from all closed positions YTD.
- Projects forward based on current open positions' unrealized gains/losses.
- Calculates safe harbor amount: `max(100% of prior year tax, 90% of current year projected tax)`.
- Alerts via notification center 10 days before each quarterly deadline (April 15, June 15, September 15, January 15).
- Tracks state tax separately (configurable state tax rate).

---

### 9.5 Reporting & Year-End Planning

*(v1.0 Form 8949, December Mode, Quarterly estimates — all retained)*

- **Form 8949 Export:** IRS-compatible CSV + optional PDF formatted for direct mailing. Generated on demand via UI "Download Form 8949" button or automatically on December 31.
- **December Mode Enhancement:** Aggressive TLH scan. Also triggers the Gain Deferral Optimizer for ALL positions in the 335–365 day window (not just those with large gains).
- **Year-End Report:** Generated December 31: full YTD PnL by strategy, tax alpha achieved vs FIFO baseline, harvested losses total, estimated Form 8949 summary. Exported as HTML + PDF to `data_cache/reports/year_end_{year}.pdf`.

---

## 10. DAILY CYCLE & TASK SCHEDULING

Orchestrated by APScheduler 3.10.4 (`AsyncIOScheduler`, `America/New_York` timezone). All times are ET.

---

### 10.1 The 24-Hour Schedule (`engine/scheduler/jobs.py`) — 14 Steps

**Step 1 — `overnight_data_refresh` (02:00 ET, Mon–Fri):**
- Downloads updated SEC filings, 13F amendments, and FRED macro data.
- Refreshes `supply_chain_graph.json` from latest SEC data.
- Runs incremental LightGBM update (`online_learner.py`) on prior day's closed trades.
- Backs up SQLite DB to `data_cache/backups/`.
- Runs DuckDB ETL sync (appends prior day's closed data to analytics DB).

**Step 2 — `pre_market_warmup` (04:00 ET, Mon–Fri):**
- Sets `engine_status = "PRE_MARKET"`.
- Refreshes all OAuth tokens; verifies broker balances and margin status.
- Fetches FRED macro data snapshot and economic calendar for the day.
- Runs `OpportunityScanner.run_premarket_scan()` (universe filter + tier-1 scoring).
- Starts FinBERT processing of overnight news headlines.
- If `llm_analysis_enabled = true`: runs `LLMAnalyst` on top 10 overnight news items.
- Calculates today's seasonality scores for all active symbols.

**Step 3 — `early_pre_market` (07:00 ET, Mon–Fri):**
- Scans for pre-market gap candidates (A10 strategy).
- Fetches options chain updates for positions expiring within 5 days.
- Updates short interest data (if market data provider has daily feed).
- Recalculates `options_sentiment_score` for universe.
- Refreshes Reddit/social media sentiment scores (D4).

**Step 4 — `macro_event_prep` (08:15 ET, Mon–Fri):**
- Checks `economic_events` table for same-day releases (NFP, CPI, PMI, FOMC, earnings).
- Adjusts position sizes pre-emptively for macro events (halves sizes if major release due).
- Queues relevant macro strategy signals (F3 FOMC, F4 CPI, F8 NFP, F18 Housing).
- Sends morning briefing to notification center: today's events, current regime, overnight market summary.

**Step 5 — `market_open_prep` (09:28 ET, Mon–Fri):**
- Sets `engine_status = "MARKET_HOURS"`.
- Places EQ-04 Flash Crash limit orders.
- Sets OCO brackets on ALL active positions.
- Calculates opening portfolio state; saves to `portfolio_snapshots`.
- Runs `SignalAggregator.clear_expired_signals()`.
- Updates Vol-Target scalar (CM-05).

**Step 6 — `main_trading_cycle` (09:35–16:01 ET, every 5 mins, Mon–Fri):**
- Checks `trading_enabled` flag.
- Calculates `portfolio_state` (equity, cash, positions_value, pnl, drawdown, Greeks).
- Runs `OpportunityScanner.run_full_scan()` — full tier-2 scoring on universe.
- Meta-Brain: updates regime probabilities, refreshes Thompson Sampling weights.
- For each enabled strategy in priority order: fetches data → calculates indicators → Kalman smooths signals → generates `SignalEvent`s.
- For signals with Kalman-smoothed strength > 0.35: passes to `RiskManager.run_pipeline()`.
- Approved orders → `ExecutionEngine` → `SmartOrderRouter`.
- `update_positions_prices()` → checks all stops and take-profits.
- `DailyPnLManager.lock_in_profits()` → updates profit-lock floor.
- Broadcasts `portfolio_tick` via WebSocket every cycle.

**Step 7 — `intraday_micro_cycle` (09:35–16:01 ET, every 1 min, Mon–Fri):**
- Runs only if `level2_enabled = true` or `intraday_strategies_enabled = true`.
- Checks A13 (Tape Reading), CM-09 (Delta Neutral), and CM-03 (Beta Hedge) on 1-min bars.
- Updates `bid_ask_imbalance` and `aggressor_ratio` from L2 feed.
- Triggers A12 (MOC Imbalance) monitoring logic.

**Step 8 — `options_management` (15:00 ET, Mon–Fri):**
- Closes all 0DTE options at MARKET.
- Closes any options at 50% profit (BTC).
- Closes any options at 200% loss (stops).
- Rolls any positions at 21 DTE that meet the roll criteria.
- Calculates end-of-day portfolio Greeks snapshot.

**Step 9 — `power_hour_scan` (15:30 ET, Mon–Fri):**
- Activates A9 (Power Hour Sweep) strategy.
- Checks MOC imbalance data (A12).
- Reviews all open positions for EOD exit decisions (intraday positions must be closed by 15:55).

**Step 10 — `daily_settlement` (15:55 ET, Mon–Fri):**
- Calls `DailyPnLManager.end_of_day_settlement()`.
- Updates `daily_cycle_log` and `profit_wallet`.
- Transitions to RECOVERY_MODE if daily PnL is negative.
- Marks any remaining intraday positions for market-close exit.
- Cancels EQ-04 Flash Crash orders if not triggered.

**Step 11 — `after_hours_routine` (16:15 ET, Mon–Fri):**
- Sets `engine_status = "AFTER_HOURS"`.
- Runs CM-01 Money Market Sweep.
- Updates ATR trailing stops for all swing positions.
- Runs `TaxAwarePortfolioManager.evaluate_all_positions()` (TLH scan + gain deferral).
- Calculates EOD VaR (Monte Carlo, 5,000 paths) and saves to `portfolio_snapshots`.
- Runs CM-10 (Maximum Diversification Rebalancer) check — flags imbalances for Saturday execution.

**Step 12 — `crypto_cycle` (17:00–09:00 ET, every 15 mins):**
- If `crypto_enabled = true`: runs CR-01 (trend), CR-06 (fear/greed), CR-07 (DeFi yield) strategies.
- Monitors BTC/ETH funding rates (CR-03).
- Checks Glassnode on-chain metrics (CR-04).

**Step 13 — `nightly_maintenance` (23:55 ET, Mon–Fri):**
- Generates daily performance report (HTML) → `data_cache/reports/`.
- Optuna hyperparameter tuning: if last tuning > 7 days old, tunes top 5 strategies on last 90 days.
- HMM retrain: if > 7 days since last full retrain.
- LightGBM regime classifier: incremental update via `online_learner.py`.
- Profit sweep log: alerts if cumulative profit_wallet > `PROFIT_SWEEP_THRESHOLD`.
- Sync DuckDB analytics tables.
- Verify all broker connections (heartbeat check).

**Step 14 — `weekend_review` (Sat 08:00 ET):**
- Full portfolio rebalance via CM-10 and PyPortfolioOpt.
- Updates all `strategy_performance` stats (win_rate, sharpe, max_dd, profit_factor).
- Clears expired wash-sale blacklist entries.
- Runs Walk-Forward validation on all active strategies (`backtest/walk_forward.py`).
- Generates weekly performance report: PnL attribution by strategy/regime, tax efficiency summary, upcoming economic events.
- Updates `supply_chain_graph.json` if any new SEC filings were processed.

**Always Running — `health_monitor` (every 60 seconds, 24/7):**
- Checks broker circuit breaker status.
- Monitors SQLite write latency (WARN if > 100ms).
- Checks APScheduler job health (CRITICAL alert if any job misses by > 2 minutes).
- Updates `engine_heartbeat` timestamp in `control_flags`.
- If Redis is enabled: publishes heartbeat to pub/sub channel.

---

## 11. CONTROL UI & OBSERVABILITY

The UI is a multi-tab, WebSocket-driven Single Page Application (SPA) served by FastAPI on port 8766. All data is fetched from the Engine API on port 8765 via REST and WebSocket. The frontend uses no build system — all JS is modular ES2022 with local imports, bundled into the `static/` directory.

---

### 11.1 Enhanced Engine API Endpoints

**Standard Endpoints (v1.0 retained):**
`GET /health`, `GET /portfolio`, `GET /positions`, `GET /trades`, `GET /signals`, `GET /strategies`, `GET /regime`, `GET /tax/summary`, `GET /tax/form8949`, `POST /control/flag`, `POST /control/strategy/{id}/toggle`, `POST /control/halt`, `POST /control/resume`.

**New Endpoints:**
- `GET /analytics/pnl_attribution`: Returns PnL broken down by strategy, regime, asset class, and time period.
- `GET /analytics/drawdown_history`: Returns drawdown series (current and historical peaks).
- `GET /analytics/factor_exposure`: Returns current portfolio factor loadings (Value, Momentum, Quality, Low-Vol, Size).
- `GET /analytics/correlation_matrix`: Returns current holdings correlation matrix (heatmap data).
- `GET /backtest/strategies`: Returns all backtest results from `backtest_results` table.
- `POST /backtest/run`: Triggers an async backtest job for a specified strategy and date range.
- `GET /scanner/live`: Returns current top 20 opportunities with full scores.
- `GET /scanner/options_flow`: Returns latest UOA signals.
- `GET /greeks/portfolio`: Returns live portfolio Greeks breakdown.
- `GET /notifications`: Returns unread alert log.
- `POST /notifications/dismiss/{id}`: Marks alert as read.
- `GET /performance/report/{date}`: Returns HTML daily report.
- `POST /control/override`: Applies a temporary parameter override (e.g., halve all position sizes for 1 hour).
- `GET /tax/estimated_payments`: Returns projected quarterly tax obligations.

**WebSocket Events (`ws://localhost:8765/ws`):**
- `portfolio_tick` (every 5s during market hours, 30s otherwise): Full `portfolio_state`.
- `trade_executed` (immediate on fill): Trade details + updated position.
- `signal_generated` (on every new signal): Strategy ID, symbol, direction, strength.
- `regime_change` (on state transition): Old/new regime, probability.
- `alert_fired` (immediate): Alert ID, severity (INFO/WARN/CRITICAL), message.
- `halt_triggered` (immediate): Reason, equity at halt, positions closed.

---

### 11.2 Dashboard UI — 9 Tabs

**Design System:**
- Dark theme: background `#0d1117`, surface `#161b22`, border `#30363d`.
- Accent: green `#3fb950` (profit), red `#f85149` (loss), yellow `#d29922` (warning), blue `#58a6ff` (neutral), purple `#bc8cff` (options).
- Typography: JetBrains Mono for all numeric data; Inter for labels and prose.
- Responsive: Full desktop layout (1920×1080 primary), tablet-friendly (1280px), minimal mobile view (480px — status and halt button only).
- Keyboard shortcuts: `H` = halt, `R` = resume, `1–9` = tab select, `Space` = refresh, `Esc` = dismiss alert.

---

#### Tab 1: Command Center (Overview)

*The default landing page. Designed for constant monitoring.*

**Header Bar (always visible, fixed top):**
- Live equity with ±$ and ±% from day open.
- Daily PnL (color-coded: green/red/yellow), with progress bar to Ideal target.
- Current drawdown % from ATH.
- Regime badge (colored per state: green = BULL_TREND, red = CRASH_RISK, etc.).
- Engine status badge (MARKET_HOURS / PRE_MARKET / AFTER_HOURS / HALTED).
- `■ HALT TRADING` button (red, prominent, requires 2-click confirmation).
- `▶ RESUME` button (only visible when halted).
- Live clock (ET).

**Daily Cycle Tracker (card):**
- Starting Capital ($10,000), Current Equity, Profit Lock Floor, Profit Wallet Cumulative.
- Profit target gauge: three concentric arcs (Minimum 1.5% / Ideal 3.0% / Stretch 5.0%).
- Cycle State badge: NORMAL / RECOVERY (with recovery day counter X/5) / COMPOUNDING (streak counter).
- Win streak counter (consecutive profitable days).

**Equity Curve (chart — Lightweight Charts):**
- 30-day equity curve vs SPY, QQQ, and BTC/USD (configurable benchmarks).
- Annotated with regime transitions (vertical dashed lines, colored by regime).
- Annotated with halt events (red markers).
- Click any point to see that day's trades in a tooltip.

**Opportunity Scanner Feed (live panel):**
- Top 10 live setups with: Rank, Symbol, Score (0–100), Strategy match, Direction, Regime compatibility icon.
- Color intensity proportional to composite score.
- Click a symbol → opens mini chart with signal annotations.

**Open Positions Table:**
- Columns: Symbol, Asset Class, Strategy, Entry, Current, P&L ($), P&L (%), Hold Period, Stop (🔴 if within 2%), Take-Profit (🟢 if within 3%), Size ($). 
- Expandable row: shows Greeks (if option), ATR trailing stop details, and a "Close Position" button.
- Color: row flashes on price change > 0.5%.

**Alert / Notification Center (sidebar panel):**
- Live feed of alerts (sorted by severity: CRITICAL → WARN → INFO).
- CRITICAL alerts appear as full-width banners that require dismissal.
- Each alert shows timestamp, strategy source, and action taken.

---

#### Tab 2: Strategy Matrix

*Control and performance monitoring for all active strategies.*

- **Strategy Table:** All strategies listed with: ID, Name, Family (Momentum/MeanRev/Arb/etc.), Status toggle (ON/OFF), 7d PnL, 30d PnL, Win Rate (30d), Sharpe (30d), Avg Hold, Thompson Weight (animated bar), Current Regime Compatibility (icon matrix: ✅/⚠/❌ for each of 6 regimes).
- **Filter Bar:** Filter by strategy family, regime compatibility, asset class, or PnL sign.
- **Bulk Controls:** Enable/disable all strategies in a family at once.
- **Strategy Detail Panel (click row):** Shows full performance history chart, parameter values, last 10 signals (with outcomes), and a "Run Backtest" button.
- **LLM Insights Panel (collapsible, only shown if `llm_analysis_enabled = true`):** Shows the latest LLM analysis summary: top 3 bullish stocks, top 3 bearish, current market summary. Labeled clearly as "Optional AI Analysis."

---

#### Tab 3: Positions & Orders

*Detailed trade management view.*

- **Positions Panel:** Full positions table with sortable columns. Includes unrealized PnL waterfall chart (ordered from largest winner to largest loser).
- **Orders Panel:** All orders (PENDING/FILLED/CANCELLED) from last 5 days. Shows broker, routing reason, execution algorithm, fill latency (ms), and slippage (bps).
- **Trade History:** Searchable, filterable history of all closed trades. Export to CSV.
- **P&L Calendar:** Monthly calendar showing daily PnL with color intensity. Red days show loss amount. Green days show profit. Hovering shows trade count and strategies used.

---

#### Tab 4: Performance Analytics

*Deep quantitative analysis of system performance.*

- **PnL Attribution Waterfall Chart (D3.js):** Shows which strategies contributed to the total PnL over the selected period. Strategies are bars; cumulative total is the final bar.
- **Drawdown Analysis:** Maximum drawdown chart with underwater equity curve. Shows recovery time from each drawdown event. Displays current drawdown depth and duration.
- **Rolling Sharpe / Sortino (30d):** Line chart showing rolling risk-adjusted performance. Horizontal target line at Sharpe = 3.0.
- **Win Rate Heatmap:** Strategy × Regime grid showing win rate (color: green = > 60%, yellow = 50–60%, red = < 50%). Helps identify which strategy-regime combos underperform.
- **Factor Exposure Chart:** Bar chart of current portfolio loadings on 5 factors (Value, Momentum, Quality, Low-Vol, Size). Shows both current and historical range.
- **Correlation Matrix Heatmap (D3.js):** Current holdings pairwise correlation. Red = high positive, blue = high negative, white = uncorrelated. Click cell for scatter plot of the pair.
- **Monte Carlo VaR Distribution:** Histogram of simulated 1-day portfolio returns (5,000 paths). Shows 99% VaR as a vertical line.
- **Strategy Performance Export:** Download complete strategy performance as CSV/JSON.

---

#### Tab 5: Options Dashboard

*Visible only when `options_enabled = true`.*

- **Portfolio Greeks Summary:** Net Delta, Gamma, Theta, Vega, Rho in large numerals with sparkline trend (today's changes). Color-coded: red if approaching limit.
- **Theta Decay Tracker:** P&L from theta decay today, week, month. Target: > 30% of total PnL. Progress towards target displayed as gauge.
- **IV Surface Heatmap:** 3D-style heatmap (D3.js) of current implied volatility surface: X-axis = strike, Y-axis = expiry, color = IV level. Click cell for options chain detail.
- **Open Options Positions Table:** Shows all options with columns for Delta, Gamma, Theta, Vega, DTE, IV at entry vs current, P&L, and break-even points.
- **Unusual Options Activity Feed:** Live scroll of UOA events from `options_flow_scanner.py`. Color-coded: green = bullish sweep, red = bearish sweep.
- **Options Strategy Builder:** Quick-launch buttons for OP-01 (Iron Condor), OP-08 (Jade Lizard), C9 (Wheel), OP-11 (Strangle) on any symbol in the scanner.

---

#### Tab 6: Live Scanner

*Opportunity discovery and signal monitoring.*

- **Universe Screener:** Real-time table of top 50 opportunities (refreshed every 5 minutes). Columns: Symbol, Score, Momentum, Volume, Trend, Catalyst, Regime Match, Options Flow, Recommended Strategy.
- **Dark Pool Feed (if `dark_pool_enabled = true`):** Scrolling list of dark pool prints with symbol, size, and accumulation/distribution classification.
- **Social Sentiment Panel:** Word cloud of top-trending symbols from Reddit with mention velocity and FinBERT score. Color = sentiment direction.
- **Insider/Congress Feed:** Chronological list of new filings from OpenInsider/housestockwatcher with size, role, and symbol. Highlights cluster buys.
- **Watchlist Manager:** User can pin specific symbols to a personal watchlist. Watchlist shows live price, daily change, and all active signals for that symbol.
- **Mini Chart View:** Click any symbol in the scanner to open a floating mini chart (Lightweight Charts) with RSI, MACD, and Bollinger Bands overlaid.

---

#### Tab 7: Tax Dashboard

- **YTD Summary Card:** STCG, LTCG, Dividends, Estimated Federal Tax Liability, Estimated State Tax Liability, Total Harvested Losses, Net Tax Alpha (after-tax PnL – pre-tax PnL assuming FIFO).
- **Tax Efficiency Timeline:** Monthly stacked bar showing STCG vs LTCG vs Harvested Losses per month YTD.
- **Wash Sale Monitor:** Active blacklist entries with expiration dates and proxy swap suggestions.
- **Gain Deferral Candidates:** Table of positions in the 335–365-day window with columns: Symbol, Current Unrealized Gain, Tax Saving if Deferred, Hedge Cost, Net Benefit, Recommended Action.
- **Quarterly Estimated Payments:** Card for each quarter showing: projected liability, safe harbor amount, due date, status (PROJECTED/DUE/PAID). Alert fires 10 days before due date.
- **Download Buttons:** "Download Form 8949 CSV", "Download Form 8949 PDF", "Download Full Year Tax Report".

---

#### Tab 8: Backtest Console

- **Strategy Selector:** Select any strategy (or all) and define a date range, capital, and parameter set (loaded from `strategy_performance` or custom-entered).
- **Run Backtest Button:** Calls `POST /backtest/run` and displays progress bar. Results appear in real-time as trades are simulated.
- **Results Dashboard:** Displays Sharpe, Sortino, Calmar, Max Drawdown, Win Rate, Profit Factor, Avg Hold, Total Return, Annualized Return, and comparison to SPY for the same period.
- **Equity Curve:** Backtest equity curve vs benchmark.
- **Trade Log:** Scrollable list of all backtest trades with entry/exit dates, signals, and PnL.
- **Walk-Forward Summary:** If walk-forward results are available (run on Saturday), shows in-sample vs out-of-sample performance comparison and an "Overfitting Score" (IS/OOS Sharpe ratio; > 0.70 is acceptable).
- **Parameter Sensitivity:** Heatmap showing how Sharpe ratio changes as 2 key parameters vary (e.g., RSI threshold 25–35 vs ATR multiplier 1.5–3.0).

---

#### Tab 9: Settings & Parameter Tuning

- **Live Parameter Overrides (no restart required):**
  - Daily Profit Target ($).
  - Maximum Daily Loss ($).
  - Position Size Multiplier (0.25x – 2.0x).
  - Risk Per Trade (% of equity).
  - Vol Target Annualized (%).
  - Soft/Hard Halt thresholds.
  - Recovery Mode multiplier.
  - All `control_flags` toggles (master switches for each system module).
- **Broker Configuration:** Displays current broker connection status, circuit breaker state, and last successful API call timestamp. "Reconnect" button per broker.
- **System Health Panel:**
  - APScheduler: list of all scheduled jobs with last run time, next run time, and status.
  - Database: SQLite write latency (ms), last backup timestamp, DB file size. DuckDB ETL last sync time.
  - Engine: CPU/RAM usage (via `psutil`), threads active, WebSocket connections, Redis status (if enabled).
  - LLM: current model, avg response time, fallback rate (% of calls that fell back to rule-based).
- **Notification Channels:** Configure desktop toasts (Windows Toast API), email (SMTP config), webhook URL (Slack/Discord), or SMS (Twilio API key). Configurable per alert severity.
- **Theme & Display:** Dark/Light theme toggle. Chart color scheme selection. Currency display format. Timezone display preference.

---

## 12. PERFORMANCE ANALYTICS & REPORTING

### 12.1 Daily Report (`data_cache/reports/daily_{date}.html`)

Auto-generated at 23:55 ET. Contains:
- Opening/closing equity, daily PnL ($ and %).
- PnL breakdown by strategy and asset class.
- All trades executed (symbol, strategy, entry, exit, P&L, hold period).
- Current open positions with unrealized P&L.
- Market regime state and transition notes.
- Risk metrics: drawdown, VaR, Greek exposures.
- Opportunity scanner top-10 for the day.
- Any alerts that fired during the day.
- Tax events (if any TLH executed, wash-sale entries added).

### 12.2 Weekly Report (`data_cache/reports/weekly_{date}.html`)

Generated Saturday morning after `weekend_review` job. Includes:
- 7-day performance summary vs prior week and rolling 30-day.
- Strategy performance ranking (sorted by Sharpe).
- PnL attribution waterfall.
- Portfolio composition and correlation matrix snapshot.
- Upcoming economic events (next 7 days).
- Tax summary (YTD harvested losses, projected annual liability).
- Walk-forward backtest summaries (in-sample vs out-of-sample for each strategy).

### 12.3 Prometheus Metrics (if `prometheus_enabled = true`)

Exposes the following metrics on `http://localhost:8765/metrics` for optional Grafana dashboarding:

| Metric | Type | Labels |
|---|---|---|
| `aqta_daily_pnl_usd` | Gauge | — |
| `aqta_portfolio_equity_usd` | Gauge | — |
| `aqta_drawdown_pct` | Gauge | — |
| `aqta_open_positions_count` | Gauge | asset_class |
| `aqta_trades_total` | Counter | strategy_id, direction |
| `aqta_signal_strength` | Histogram | strategy_id |
| `aqta_order_latency_ms` | Histogram | broker |
| `aqta_regime_state` | Gauge | state |
| `aqta_portfolio_delta` | Gauge | — |
| `aqta_portfolio_theta_daily` | Gauge | — |
| `aqta_risk_check_blocked` | Counter | rule_name |
| `aqta_llm_response_time_ms` | Histogram | model |

---

## 13. BACKTESTING & WALK-FORWARD VALIDATION

### 13.1 Backtester (`engine/backtest/backtester.py`)

- Loads OHLCV + indicator data from Parquet feature store (or fetches and caches on first run).
- Replays the trading cycle chronologically, firing strategy signals as they would have appeared.
- **Realistic Fills:** Market orders fill at `close + slippage`; limit orders at limit price only if low/high crossed.
- **Transaction Costs:** Configurable commission model (flat per trade, or per-share for IBKR).
- **Slippage Model:** `slippage = N(0, 0.0003) * sqrt(order_size / avg_daily_volume)` — larger orders have proportionally more market impact.
- **Survivorship Bias Control:** Uses a point-in-time universe membership file (`sp500_membership_history.parquet`) to avoid including companies that were added to the S&P 500 after the test period.

### 13.2 Walk-Forward Validation (`engine/backtest/walk_forward.py`)

- **Method:** Rolling window walk-forward. In-sample: 18 months. Out-of-sample: 3 months. Rolls forward by 3 months each iteration.
- **Overfitting Score:** `OOS_Sharpe / IS_Sharpe`. Score < 0.50 triggers a WARN (strategy may be overfit). Score < 0.30 triggers an automatic disable pending review.
- **Hyperparameter Optimization (Optuna):** In-sample period uses Optuna (TPE sampler) to find optimal parameter set. Out-of-sample tests the found parameters without any further fitting.
- Results stored in `backtest_results` table and visualized in the Backtest Console (Tab 8).

### 13.3 Monte Carlo Simulation (`engine/backtest/monte_carlo.py`)

- **Portfolio-Level Simulation:** 10,000 paths simulated using Cholesky decomposition of the current asset covariance matrix.
- Outputs: 1-day VaR (99%), 5-day VaR (95%), CVaR (Expected Shortfall), probability of drawdown exceeding 5%/8%/15%.
- Run nightly after `daily_settlement` and stored in `portfolio_snapshots`.

---

## 14. SYSTEM CONFIGURATION & DEPLOYMENT

### 14.1 Primary Configuration (`config/settings.toml`)

```toml
[system]
engine_port = 8765
ui_port = 8766
timezone = "America/New_York"
log_level = "INFO"  # DEBUG, INFO, WARN, ERROR

[capital]
daily_capital_base = 10000.0
min_profit_target_pct = 0.015
ideal_profit_target_pct = 0.030
stretch_profit_target_pct = 0.050
soft_halt_loss_pct = 0.015
hard_halt_loss_pct = 0.030
emergency_halt_loss_pct = 0.050
profit_protect_pct = 0.60
profit_sweep_threshold = 30000.0
recovery_max_days = 5
recovery_risk_multiplier = 0.5
compounding_streak_days = 5
compounding_size_multiplier = 1.2

[risk]
max_single_position_pct = 0.10
max_sector_pct = 0.35
max_correlation_threshold = 0.75
max_portfolio_leverage_overnight = 2.0
max_portfolio_leverage_intraday = 4.0
pdt_equity_buffer = 26500.0
kelly_fraction = 0.25
vol_target_annualized = 0.15
intraday_drawdown_soft_pct = 0.02
intraday_drawdown_hard_pct = 0.04
margin_utilization_warn_pct = 0.75
margin_utilization_halt_pct = 0.90

[data]
primary_data_provider = "polygon"  # polygon | yfinance
universe_min_adtv_usd = 5_000_000
universe_min_price = 1.0
universe_max_price = 5000.0
cache_ttl_daily_bars_hours = 24
cache_ttl_intraday_bars_hours = 1
feature_cache_dir = "data_cache/features"

[llm]
enabled = false  # Controlled by control_flags, not this file
local_model = "llama3.3"
ollama_base_url = "http://localhost:11434"
cloud_fallback_enabled = false
cloud_provider = "anthropic"  # anthropic | openai
max_cloud_calls_per_day = 20
finbert_model = "ProsusAI/finbert"
finbert_batch_size = 32
keyword_scorer_enabled = true  # Always-on rule-based fallback

[tax]
tlh_min_loss_threshold = -500.0
tlh_min_loss_threshold_december = -300.0
marginal_tax_rate = 0.35
ltcg_tax_rate = 0.20
state_tax_rate = 0.09  # Configure per user's state
gain_deferral_days_window_start = 335
gain_deferral_days_window_end = 365

[notifications]
desktop_notifications = true
email_enabled = false
smtp_server = ""
smtp_port = 587
webhook_enabled = false
webhook_url = ""
min_alert_level = "WARN"  # INFO | WARN | CRITICAL
```

---

### 14.2 Service Installation (Windows — NSSM)

```batch
:: Install engine as Windows service
nssm install AQTA_Engine "C:\Python311\python.exe" "C:\TradingSystem\engine\main.py"
nssm set AQTA_Engine AppDirectory "C:\TradingSystem"
nssm set AQTA_Engine AppStdout "C:\TradingSystem\logs\engine.log"
nssm set AQTA_Engine AppStderr "C:\TradingSystem\logs\engine_err.log"
nssm set AQTA_Engine Start SERVICE_AUTO_START
nssm set AQTA_Engine AppRestartDelay 5000

:: Install UI as Windows service
nssm install AQTA_UI "C:\Python311\python.exe" "C:\TradingSystem\ui\ui_server.py"
nssm set AQTA_UI AppDirectory "C:\TradingSystem"
nssm set AQTA_UI Start SERVICE_AUTO_START

:: Start both services
net start AQTA_Engine
net start AQTA_UI
```

---

### 14.3 Optional Components

| Component | Install Command | Enable Via |
|---|---|---|
| Redis (local, via WSL2) | `apt install redis-server` | `redis_enabled = true` |
| Prometheus | Download from prometheus.io | `prometheus_enabled = true` |
| Grafana | Download from grafana.com | Connect to Prometheus |
| Ollama (LLM) | Download from ollama.ai | `llm_analysis_enabled = true` |
| GPU Acceleration (FinBERT) | `pip install torch --index-url https://download.pytorch.org/whl/cu121` | Auto-detected |

---

### 14.4 First-Run Setup Checklist

1. Install Python 3.11+ and all requirements from `requirements.txt`.
2. Copy `config/broker_secrets.env.example` → `config/broker_secrets.env`. Fill in API keys and OAuth credentials.
3. Edit `config/settings.toml` — set capital base, tax rates, and notification preferences.
4. Run `python engine/database/migrations.py` to create SQLite schema and pre-populate `control_flags`.
5. Run `python engine/data/market_data.py --warmup` to download 2 years of historical data and train the HMM model.
6. Verify all brokers in shadow mode: `python engine/brokers/schwab_broker.py --test`.
7. Confirm `shadow_mode = true` in `control_flags`. Run the engine and monitor for one full trading day.
8. Review daily report in `data_cache/reports/`. If results are satisfactory, set `shadow_mode = false` via the UI Settings tab.

---

## APPENDIX A: STRATEGY FAMILY QUICK REFERENCE

| ID | Name | Family | Regime | LLM Req? | Options Req? |
|---|---|---|---|---|---|
| EQ-01 | Classic Trend Following | Momentum | BULL | No | No |
| EQ-03 | BB Mean Reversion | Mean Rev | SIDEWAYS | No | No |
| EQ-05 | Trend Acceleration (SAR) | Momentum | BULL | No | No |
| EQ-06 | Sector Momentum 30m | Momentum | BULL/SIDEWAYS | No | No |
| EQ-07 | Relative Volume Surge | Momentum | ANY | No | No |
| EQ-08 | First Hour Continuation | Momentum | BULL | No | No |
| EQ-09 | Power Hour Sweep | Momentum | BULL | No | No |
| EQ-10 | Breadth Divergence | Momentum | BULL | No | No |
| A1 | Opening Range Breakout | Momentum | BULL | No | No |
| A2 | VWAP Momentum | Momentum | BULL | No | No |
| A3 | Gap-and-Go | Momentum | ANY | Optional | No |
| A4 | Relative Strength Rotation | Momentum | ANY | No | No |
| A5 | EMA Ribbon Expansion | Momentum | BULL | No | No |
| A6 | 52-Week High Breakout | Momentum | BULL | No | No |
| A7 | Unusual Volume (No News) | Momentum | ANY | No | No |
| A8 | Multi-TF Confluence | Momentum | ANY | No | No |
| A9 | Options Flow → Equity | Momentum | BULL | No | Required |
| A10 | Pre-Market Scanner | Momentum | ANY | No | No |
| A11 | HALT Resume | Momentum | ANY | No | No |
| A12 | MOC Imbalance | Momentum | ANY | No | No |
| A13 | Tape Reading (L2) | Momentum | ANY | No | No |
| A14 | Intraday Sector Rotation | Momentum | BULL | No | No |
| A15 | Key Level Reversal | Mean Rev | ANY | No | No |
| A16 | News Catalyst (Rule-Based) | Momentum | ANY | No | No |
| A17 | Earnings Gap Continuation | Momentum | BULL | No | No |
| A18 | Dark Pool Accumulation | Momentum | ANY | No | No |
| B1 | BB Squeeze Breakout | Mean Rev | SIDEWAYS | No | No |
| B2 | RSI Divergence | Mean Rev | SIDEWAYS | No | No |
| B3 | Oversold Large-Cap Bounce | Mean Rev | ANY | No | No |
| B4 | Intraday VWAP Deviation | Mean Rev | ANY | No | No |
| B5 | Monday Gap Fade | Mean Rev | ANY | No | No |
| B6 | Z-Score Reversion | Mean Rev | SIDEWAYS | No | No |
| B7 | ETF Premium/Discount | Mean Rev | ANY | No | No |
| B8 | Post-Earnings Reversion | Mean Rev | ANY | No | No |
| B9 | Seasonal Calendar | Mean Rev | ANY | No | No |
| B10 | Overnight Gap Fade | Mean Rev | ANY | No | No |
| B11 | Anchored VWAP Reversion | Mean Rev | ANY | No | No |
| B12 | Multi-Day Oversold Accum. | Mean Rev | BULL/RECOVERY | No | No |
| B13 | Option-Implied Reversion | Mean Rev | SIDEWAYS | No | Optional |
| B14 | High-Beta Reversion | Mean Rev | SIDEWAYS_LOW | No | No |
| D1 | Congress Replication | Sentiment | ANY | No | No |
| D2 | Insider Cluster Buy | Sentiment | ANY | No | No |
| D3 | FinBERT Sentiment | Sentiment | ANY | No | No |
| D4 | WSB Reddit Momentum | Sentiment | ANY | No | No |
| D5 | Google Trends Catalyst | Sentiment | ANY | No | No |
| D6 | Dark Pool Flow | Sentiment | ANY | No | No |
| D7 | Institutional 13F | Sentiment | ANY | No | No |
| D8 | UOA → Equity Signal | Sentiment | ANY | No | Required |
| D9 | Form 4 Velocity | Sentiment | ANY | No | No |
| D10 | Short Squeeze Score | Sentiment | ANY | No | No |
| D11 | Analyst Upgrade Momentum | Sentiment | ANY | No | No |
| D12 | Social Sentiment Divergence | Sentiment | ANY | No | No |
| D13 | ETF Flow Signal | Sentiment | ANY | No | No |
| D14 | Earnings Whisper Gap | Sentiment | ANY | No | No |
| D15 | Block Trade Detector | Sentiment | ANY | No | No |
| D16 | Supply Chain Contagion | Sentiment | ANY | Optional | No |
| EQ-02 | Stat Arb Pairs | Quant/Arb | SIDEWAYS | No | No |
| E1 | 3-Leg Cointegration | Quant/Arb | SIDEWAYS | No | No |
| E2 | Vol Regime Switching | Quant/Arb | ANY | No | Optional |
| E3 | Cross-Asset Corr Break | Quant/Arb | ANY | No | No |
| E4 | ETF NAV Arb | Quant/Arb | ANY | No | No |
| E5 | 5-Factor Momentum | Quant/Arb | ANY | No | No |
| E6 | Lead-Lag Sector | Quant/Arb | BULL | No | No |
| E7 | Put-Call Parity Violation | Quant/Arb | ANY | No | Required |
| E8 | Calendar Spread Arb (VIX) | Quant/Arb | ANY | No | No |
| E9 | S&P 500 Rebalance Arb | Quant/Arb | ANY | No | No |
| E10 | Dispersion Trading | Quant/Arb | SIDEWAYS | No | Required |
| E11 | PCA Factor Breakout | Quant/Arb | ANY | No | No |
| E12 | Kalman Filter Pairs | Quant/Arb | SIDEWAYS | No | No |
| E13 | HMM State Transition Arb | Quant/Arb | TRANSITION | No | No |
| E14 | Vol Surface Arb (Skew) | Quant/Arb | ANY | No | Required |
| E15 | Correlation Regime Arb | Quant/Arb | TRANSITION | No | No |
| E16 | Multi-Asset Carry Harvest | Quant/Arb | ANY | No | No |
| F1 | Rate-Sensitive Rotation | Macro | ANY | No | No |
| F2 | VIX Mean Reversion | Macro | ANY | No | No |
| F3 | FOMC Calendar | Macro | ANY | No | No |
| F4 | CPI/PPI Reaction | Macro | ANY | No | No |
| F5 | Gold/Dollar Inverse | Macro | ANY | No | No |
| F6 | Commodity-to-Equity | Macro | ANY | No | No |
| F7 | Yield Curve Shape | Macro | ANY | No | No |
| F8 | NFP Reaction | Macro | ANY | No | No |
| F9 | PMI/ISM Signal | Macro | ANY | No | No |
| F10 | Geopolitical Risk | Macro | ANY | No | No |
| F11 | Earnings Season Rotation | Macro | BULL | No | No |
| F12 | Seasonal Macro Calendar | Macro | ANY | No | No |
| F13 | Credit Spread Signal | Macro | ANY | No | No |
| F14 | EM/DM Divergence | Macro | ANY | No | No |
| F15 | Inflation Regime | Macro | ANY | No | No |
| F16 | Central Bank Divergence | Macro | ANY | No | No |
| F17 | Commodity Roll Yield | Macro | ANY | No | No |
| F18 | Housing Data Sensitivity | Macro | ANY | No | No |
| CM-01 | Money Market Sweep | Cash/Hedge | ANY | No | No |
| CM-02 | Static Hedge Ladder | Cash/Hedge | ANY | No | Optional |
| CM-03 | Dynamic Beta Hedge | Cash/Hedge | ANY | No | No |
| CM-04 | VIX Term Structure Ladder | Cash/Hedge | ANY | No | No |
| CM-05 | Vol Target Overlay | Cash/Hedge | ANY | No | No |
| CM-06 | T-Bill Ladder Optimizer | Cash/Hedge | ANY | No | No |
| CM-07 | Tail Risk Protection | Cash/Hedge | BEAR/CRASH | No | Optional |
| CM-08 | Correlation Breakdown Hedge | Cash/Hedge | ANY | No | No |
| CM-09 | Delta-Neutral Cash Park | Cash/Hedge | ANY | No | Required |
| CM-10 | Max Diversification Rebal. | Cash/Hedge | ANY | No | No |
| CM-11 | Drawdown Circuit Breaker | Cash/Hedge | ANY | No | No |
| CM-12 | Margin Utilization Opt. | Cash/Hedge | ANY | No | No |
| EQ-04 | Flash Crash Buy Ladder | Cash/Hedge | CRASH | No | No |
| OP-01 | 0DTE Iron Condor | Options | SIDEWAYS | No | Required |
| OP-02 | Vol Skew Arb | Options | ANY | No | Required |
| OP-03 | Covered Call Yield | Options | ANY | No | Required |
| OP-04 | Protective Put | Options | ANY | No | Required |
| OP-06 | Earnings IV Crush | Options | ANY | No | Required |
| OP-07 | Iron Butterfly | Options | SIDEWAYS | No | Required |
| OP-08 | Jade Lizard | Options | BULL | No | Required |
| OP-09 | Calendar Spread | Options | SIDEWAYS | No | Required |
| OP-10 | Diagonal Spread | Options | BULL | No | Required |
| OP-11 | Pre-Event Strangle | Options | ANY | No | Required |
| OP-12 | Short Gamma Scalping | Options | SIDEWAYS_LOW | No | Required |
| C4 | Cash-Secured Put | Options | ANY | No | Required |
| C6 | Poor Man's Covered Call | Options | BULL | No | Required |
| C7 | Ratio Spread | Options | BULL | No | Required |
| C8 | Protective Collar | Options | ANY | No | Required |
| C9 | Wheel Strategy | Options | ANY | No | Required |
| CR-01 | Crypto Trend (4H) | Crypto | ANY | No | No |
| CR-02 | CEX/DEX Arb | Crypto | ANY | No | No |
| CR-03 | Funding Rate Harvest | Crypto | ANY | No | No |
| CR-04 | On-Chain Whale Alert | Crypto | ANY | No | No |
| CR-05 | BTC Halving Cycle | Crypto | ANY | No | No |
| CR-06 | Crypto Fear & Greed | Crypto | ANY | No | No |
| CR-07 | DeFi Yield Capture | Crypto | ANY | No | No |
| FX-01 | G10 Carry | FX | ANY | No | No |
| FX-02 | Dollar Strength Overlay | FX | ANY | No | No |
| FX-03 | Currency Momentum | FX | ANY | No | No |
| FX-04 | Carry + Momentum Combo | FX | ANY | No | No |
| FX-05 | Vol-Adjusted Carry | FX | ANY | No | No |
| FI-01 | Duration Ladder (T-Bills) | Fixed Inc | ANY | No | No |
| FI-02 | Treasury Yield Momentum | Fixed Inc | ANY | No | No |
| FI-03 | TIPS Inflation Protection | Fixed Inc | ANY | No | No |
| FI-04 | Municipal Bond Spread | Fixed Inc | ANY | No | No |

**Total Strategies: 133**

---

## APPENDIX B: KPI MONITORING REFERENCE

| KPI | Target | Alert Threshold | Alert Level |
|---|---|---|---|
| Daily PnL | > $150 | < -$150 (soft) / < -$300 (hard) | WARN / CRITICAL |
| Drawdown from ATH | < 8% | > 4% | WARN |
| Win Rate (90d) | > 55% | < 45% | WARN |
| Sharpe (30d rolling) | > 3.0 | < 1.5 | WARN |
| Options Theta Contribution | > 30% of PnL | < 10% | INFO |
| SOR Latency | < 5ms | > 20ms | WARN |
| System Uptime | > 99.5% | < 98% | CRITICAL |
| LLM Accuracy (if enabled) | > 65% | < 50% | WARN |
| Portfolio Beta | 0.85–1.05 (BULL) | > 1.3 or < 0.3 | WARN |
| Net Portfolio Delta | ±0.15 * NAV | ±0.30 * NAV | WARN |
| Margin Utilization | < 75% | > 85% | WARN |
| Avg Pairwise Correlation | < 0.30 | > 0.60 | WARN |
| Overfitting Score (OOS/IS) | > 0.70 | < 0.50 | WARN |

---

*AQTA Enhanced Specification v2.0 — Local Infrastructure Edition*
*Document generated for implementation reference. All timestamps UTC unless specified.*
