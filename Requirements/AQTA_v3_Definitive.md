# AUTONOMOUS QUANTITATIVE TRADING ARCHITECTURE (AQTA)
## Comprehensive System Specification & Master Blueprint — v3.0 (Definitive Local Edition)

> **Infrastructure:** Local Windows (Primary) / Linux (WSL2 / Native). Zero cloud dependency.
> **LLM:** Optional — 3-Tier NLP fallback guarantees 100% uptime without any LLM.
> **Strategy Count:** 160+ strategies across 10 families + Group G (Leveraged/High-Octane).
> **Cycle Interval:** Parameter-driven (1–10 minutes, default 5).
> **Settlement:** Dual — Preliminary 15:55 ET + Final 20:00 ET.
> **Targets:** Dynamically calculated from daily starting capital; user-overridable by % or $.

---

## MASTER CHANGE LOG vs v2.0

| Area | Change |
|---|---|
| Capital Framework | All targets now % of daily starting capital, dynamically calculated. User can override per-day with a fixed $ or % via UI without restart. |
| Cycle Interval | `MAIN_CYCLE_INTERVAL_MINUTES` parameter (1–10, default 5). Hot-reloadable from UI. Intraday micro-cycle is always 1-min and separate. |
| Settlement | Dual settlement: Preliminary at 15:55 ET (regular session), Final at 20:00 ET (after-hours). |
| NLP/LLM | 3-Tier NLP engine: Tier 1 LLM (Ollama/Cloud, optional), Tier 2 SLM (FinBERT/DistilRoBERTa via ONNX, default), Tier 3 VADER/NLTK (deterministic fallback). |
| Strategy Loader | Dynamic loader with `health_check()` per strategy; `DISABLED_ERROR` state with UI tooltip showing error + resolution steps. |
| Strategies | 160+ total; added Group G (G1–G4), CO-01/CO-02, VX-01/VX-02, AL-01/AL-02/AL-03, OP-05, A8–A13, B6–B9 (enhanced), D8–D11, E7–E10, F7–F10 (enhanced), CM-03/CM-04/CM-05/EQ-05. |
| Database | Added `llm_fallback_log`, `strategy_correlation_matrix`, `dark_pool_prints`, `options_positions`, `greeks_snapshots`, `crypto_positions`, `funding_rate_log` tables. |
| Risk Engine | Extended to 15-step pipeline: added Flash Crash Correlation (13), Liquidity Dry-Up Guard (14), Strategy Drawdown Halt (15). |
| Scheduler | Extended to 16 steps. Added `regular_market_open`, `moc_imbalance_scan`, `margin_minimizer`, `after_hours_transition`, `final_settlement`. |
| State Management | `StateCacheManager`: Redis 7 primary + asyncio native fallback. Auto-switches seamlessly. |
| Performance Math | Added `numba` JIT compilation for heavy quant routines. |
| UI | Added System Topology tab, NLP Engine Status panel, Trade Replay modal, Strategy health tooltips with resolution steps, inline strategy parameter tuning. |
| Compliance | Full regulatory compliance matrix (FINRA, IRC, SEC, MiFID II, IRS). |
| Implementation | 15-Phase copilot implementation prompts with acceptance criteria. |
| Deployment | Windows bat files, first-run setup script, health-check script, README template. |

---

## 1. SYSTEM OVERVIEW & OPERATING DOCTRINE

AQTA is a self-directed, multi-asset, multi-broker quantitative trading platform for continuous 24/7/365 autonomous operation on local infrastructure. It maximizes risk-adjusted, tax-aware, after-cost returns through a 160+ strategy arsenal, ML regime detection, smart order routing, and a strict daily capital cycle — all without requiring cloud services, LLM availability, or external data subscriptions.

---

### 1.1 Capital Framework & Daily Cycle Rules

All monetary targets are **dynamically computed as a percentage of `STARTING_CAPITAL_TODAY`** — the equity value at the opening portfolio snapshot each trading day. Users may override any target for the current day via the UI (Settings tab, Parameter Overrides) using either a fixed dollar amount or a percentage. Overrides are stored in `control_flags` and reset at the next day's open.

#### 1.1.1 Daily Capital Configuration

```toml
# config/settings.toml — [capital] section

# --- Base Capital ---
daily_capital_base = 10000.0          # Fallback if broker balance unavailable

# --- Profit Targets (% of STARTING_CAPITAL_TODAY) ---
min_profit_target_pct    = 1.5        # Default minimum: 1.5%
ideal_profit_target_pct  = 3.0        # Default ideal:   3.0%
stretch_profit_target_pct = 5.0       # Default stretch:  5.0%

# --- Profit Lock ---
profit_lock_trigger_pct  = 20.0       # Lock profits once intraday gain > 20% of ideal target
profit_protect_pct       = 0.60       # Lock 60% of gains above trigger
profit_lock_step2_pct    = 0.70       # At 2× ideal: lock 70%

# --- Loss Limits (% of STARTING_CAPITAL_TODAY) ---
soft_halt_loss_pct       = 1.5        # -1.5% → 50% size reduction
hard_halt_loss_pct       = 3.0        # -3.0% → full halt, cancel limits
emergency_halt_loss_pct  = 5.0        # -5.0% → emergency liquidation

# --- Exceptional Day ---
exceptional_day_pct      = 7.5        # ≥7.5% → shift to capital-preservation mode

# --- Capital Scaling ---
compounding_streak_days    = 5         # Consecutive profitable days to trigger scaling
compounding_multiplier     = 1.20      # Position size multiplier after streak
compounding_max_multiplier = 1.50      # Absolute ceiling on compounding multiplier
capital_base_scale_per_10d = 0.05      # Grow capital base 5% per 10-day profit streak
```

#### 1.1.2 Dynamic Target Calculation

At 09:28 ET each trading day, `DailyPnLManager.initialize_day()` runs:

```python
class DailyTargetConfig:
    """Resolved once per day. Stored in daily_cycle_log."""
    starting_capital: float        # Live broker equity at 09:28 ET
    min_target_usd: float          # = starting_capital * min_profit_target_pct / 100
    ideal_target_usd: float
    stretch_target_usd: float
    soft_halt_usd: float           # = starting_capital * soft_halt_loss_pct / 100
    hard_halt_usd: float
    emergency_halt_usd: float
    profit_lock_trigger_usd: float
    source: str                    # "DYNAMIC_PCT" | "OVERRIDE_PCT" | "OVERRIDE_USD"
    override_note: str | None      # Human-readable reason if overridden
```

**Override precedence** (checked in order):
1. `target_override_usd` in `control_flags` → Use exact dollar value; source = `"OVERRIDE_USD"`.
2. `target_override_pct` in `control_flags` → Compute `starting_capital × pct / 100`; source = `"OVERRIDE_PCT"`.
3. Neither set → Compute from `settings.toml` percentages; source = `"DYNAMIC_PCT"`.

Overrides reset to empty strings at 04:00 ET each day (pre-market routine). Users may set new overrides anytime intraday from the UI; they take effect on the **next** 5-minute cycle.

#### 1.1.3 Profit Extraction Rule
EOD equity > `starting_capital + min_target_usd` → extract excess to virtual `profit_wallet`. Real settled cash stays in brokerage until `PROFIT_SWEEP_THRESHOLD` is met or manually triggered.

#### 1.1.4 Profit Lock Mechanism
Once intraday profit ≥ `profit_lock_trigger_usd` (default 20% of ideal target):
- Lock `profit_protect_pct (60%)` of all gains above the trigger.
- At 2× ideal target: increase lock to 70% (`profit_lock_step2_pct`).
- Soft halt triggers if equity drops below locked floor.

---

### 1.2 Zero-Loss Protocol & Recovery Mode

- **Duration:** Up to `RECOVERY_MAX_DAYS = 5` trading days (configurable).
- **Target:** `recovery_target = abs(daily_pnl) × 1.1` (loss + 10% buffer).
- **Risk Adjustment:** Position sizes halved (`recovery_risk_multiplier = 0.5`).
- **Strategy Bias:** Mean Reversion, Cash Management, Hedging strategies get +40% allocation premium. Intraday and high-beta momentum capped at 20% of capital.
- **Recovery Acceleration:** If intraday profit > 50% of recovery target before noon, 1 additional momentum strategy may be carefully re-enabled.
- **Failure Escalation:** If recovery target not met after 5 days → **Capital Preservation Mode**: only Cash Management, Hedging, and theta-positive options strategies may trade until one full profitable day restores normal mode.

---

### 1.3 Capital State Machine

The `DailyPnLManager` maintains a state machine that governs overall system behavior:

```
States:
  NORMAL_OPERATION    → Daily targets, full strategy set, normal risk
  RECOVERY_MODE       → After loss day; conservative sizing, 5-day window
  COMPOUNDING_MODE    → 5+ consecutive profit days; scaled sizing (1.2x → 1.35x cap)
  SOFT_HALT           → Intraday loss > soft_halt_loss_pct; 50% sizing reduction
  HARD_HALT           → Intraday loss > hard_halt_loss_pct; trading stopped
  EMERGENCY_HALT      → Intraday loss > emergency_halt_loss_pct; liquidation
  CAPITAL_PRESERVATION → Recovery failed (5 days); defensive-only strategies
  OPPORTUNITY_SURGE   → Scanner finds > 5 HIGH-conviction setups simultaneously;
                         deployment ratio raised to 90%, position sizing +15%
  EXCEPTIONAL_DAY     → Gain ≥ exceptional_day_pct (7.5%); capital-preservation
                         mode activates for new entries, runners protected by ratchet stops

Transitions:
  NORMAL → SOFT_HALT          (intraday loss > soft threshold)
  NORMAL → COMPOUNDING        (5 consecutive profit days)
  NORMAL → OPPORTUNITY_SURGE  (scanner score ≥ 5 HIGH signals in one cycle)
  ANY    → HARD_HALT          (intraday loss > hard threshold)
  ANY    → EMERGENCY_HALT     (intraday loss > emergency threshold)
  NORMAL/COMPOUNDING → RECOVERY_MODE  (day closes negative)
  RECOVERY → NORMAL           (recovery_target met)
  RECOVERY → CAPITAL_PRESERVATION (5 days elapsed, target not met)
  CAPITAL_PRESERVATION → NORMAL  (one full profitable day)
```

---

### 1.4 Target KPIs & Performance Benchmarks

| KPI | Target | Window |
|---|---|---|
| Annualized Sharpe Ratio | > 3.0 | Monthly rolling |
| Sortino Ratio | > 4.5 | Monthly rolling |
| Calmar Ratio | > 2.5 | Annual |
| Maximum Drawdown | < 8% | Rolling 90 days |
| Win Rate (all strategies) | > 55% | Rolling 90 days |
| Average Hold Period | 2–15 days (equities) | Rolling 30 days |
| Options PnL (theta decay) | > 30% of total PnL | Weekly |
| Theta Decay Capture | > 80% of premium written | Per position |
| Execution Latency (SOR) | < 5ms | Per order |
| System Uptime | > 99.5% | Monthly |
| Tax Alpha (after-tax vs pre-tax) | > 0.5% annually | Quarterly |
| NLP Accuracy (LLM, if enabled) | > 65% directional accuracy | Rolling 30 days |
| Strategy Avg Pairwise Correlation | < 0.30 | Weekly |
| Daily Reporting | Delivered by 00:01 ET | Daily |
| Emergency Failover (local watchdog) | < 2 min to halt | Quarterly test |
| Crypto Yield (DeFi + funding) | > 8% APY on crypto allocation | Monthly |

---

### 1.5 Realistic Performance Expectations (on $10,000 Capital)

| Scenario | Daily Target | Win Rate | Strategies Active | Monthly Estimate |
|---|---|---|---|---|
| **Conservative** | $100–$150 (1.0–1.5%) | 62–68% | Mean-Reversion, Stat-Arb, Covered Calls, VWAP | ~$2,500–$4,000 |
| **Normal** | $150–$300 (1.5–3.0%) | 58–65% | All non-aggressive (20–30 strategies) | ~$4,000–$8,000 |
| **Aggressive** | $300–$500 (3.0–5.0%) | 55–62% | Full arsenal including leveraged ETFs, 0DTE | ~$8,000–$12,000 |

> These are expected values, not guarantees. 30–40% of trading days may be small losses (<1%). Recovery Mode handles loss days. Tax efficiency adds 15–20% to net returns vs gross. Start with 30 days shadow mode before any real money.

**Annual Projection (if $10k floor maintained, profits extracted):**
- Conservative: $30,000–$48,000 extracted annually.
- Realistic (all risks factored): 100–200% annual return on capital at risk is ambitious but achievable with a disciplined, diversified multi-strategy approach.

---

### 1.6 Market Regime Operating Modes (Strategy Allocation by Regime)

| Regime | Momentum | Mean Rev | Arb/Quant | Macro | Cash/Hedge | Leveraged |
|---|---|---|---|---|---|---|
| BULL_TREND | 35% | 10% | 20% | 20% | 10% | 5% |
| BEAR_TREND | 5% | 25% | 20% | 25% | 25% | 0% |
| SIDEWAYS_LOW_VOL | 10% | 30% | 30% | 10% | 20% | 0% |
| SIDEWAYS_HIGH_VOL | 10% | 20% | 20% | 15% | 35% | 0% |
| CRASH_RISK | 0% | 10% | 10% | 15% | 65% | 0% |
| RECOVERY | 20% | 30% | 20% | 15% | 15% | 0% |

---

## 2. ARCHITECTURE & TECHNOLOGY STACK

AQTA runs entirely on local Windows or Linux infrastructure. No cloud dependency is required for any core function. Optional components (Redis, Prometheus, Grafana, Ollama) enhance performance and observability but are never required for operation.

---

### 2.1 Local Deployment Stack

- **Runtime:** Python 3.11+ (asyncio-native). `uvloop` on Linux/WSL2 for near-native event loop performance.
- **Operational Database:** SQLite 3 (WAL mode: `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA cache_size=-64000; PRAGMA foreign_keys=ON`) + SQLAlchemy 2.0.30.
- **Analytics Database:** DuckDB 0.10+ (columnar, in-process). Zero network overhead. All read-heavy OLAP: strategy analytics, PnL attribution, tax reporting, backtest storage.
- **In-Memory State (`StateCacheManager`):**
  - **Primary:** Redis 7 (localhost). Used for tick data aggregation, rolling correlations, order book snapshots, pub/sub event routing, rate-limit counters.
  - **Fallback (Automatic):** If Redis is unreachable or crashes, `StateCacheManager` switches to native Python `asyncio` in-memory dicts and `asyncio.Queue`. The switch is transparent to all consumers.
  - **EOD Persistence:** At 23:55 ET, `StateCacheManager.flush_to_sqlite()` dumps all critical Redis state (rolling correlations, strategy performance metrics, ML feature arrays) to SQLite for next-day initialization.
- **Task Scheduling:** APScheduler 3.10.4 (`AsyncIOScheduler`, `America/New_York` timezone) running in the main asyncio event loop.
- **API & Engine:** FastAPI 0.111.0 + Uvicorn 0.30.0 (Engine :8765, UI :8766).
- **UI Frontend:** SPA in Vanilla HTML5/CSS3/ES2022. No Node/npm. Local-vendored Chart.js 4.x, D3.js 7.x, Lightweight Charts (TradingView). All JS files in `static/lib/`.
- **Process Management:** NSSM (Windows) / Systemd unit (Linux). Watchdog via `watchdog` Python library.
- **Observability (Optional):** Prometheus 2.x (metrics on `:8765/metrics`) + Grafana (`:3000`). Enabled via `prometheus_enabled = true`.
- **Performance Math:** `numba` JIT compilation for CPU-intensive quant routines (HMM training, Monte Carlo VaR, covariance computation). Falls back to pure NumPy if numba is unavailable.

---

### 2.2 NLP Engine — 3-Tier Architecture (LLM-Optional)

The system guarantees 100% operational continuity regardless of LLM availability through a 3-tier NLP fallback engine. The active tier is displayed prominently in the UI (System Health tab).

```
┌─────────────────────────────────────────────────────────────────┐
│                    NLP ENGINE TIERS                             │
├─────────────────────────────────────────────────────────────────┤
│  TIER 1: LLM (Optional)                                         │
│  ├── Local: Ollama (llama3.3, mistral-nemo, deepseek-r1:8b)    │
│  ├── Cloud Fallback: Anthropic Claude Sonnet / GPT-4o-mini      │
│  ├── Activation: llm_mode = "LOCAL" | "CLOUD"                  │
│  └── Use: Deep 10-K analysis, earnings call parsing, complex    │
│           multi-document synthesis, 10+ sentence context        │
├─────────────────────────────────────────────────────────────────┤
│  TIER 2: SLM — Small Language Models (Default)                  │
│  ├── FinBERT: ProsusAI/finbert (HuggingFace, local)            │
│  ├── DistilRoBERTa-financial: quantized, ONNX runtime          │
│  ├── Inference: < 50ms per headline, GPU or CPU                 │
│  ├── Activation: llm_mode = "DISABLED" or LLM timeout          │
│  └── Use: News sentiment, headline scoring, rapid signal gen    │
├─────────────────────────────────────────────────────────────────┤
│  TIER 3: Deterministic Fallback (Always Available)              │
│  ├── Sentiment: vaderSentiment (VADER)                         │
│  │     compound > 0.5 → BULLISH; < -0.5 → BEARISH             │
│  ├── Earnings: Finnhub/AlphaVantage actual_eps vs estimate_eps  │
│  │     percentage surprise calculated numerically               │
│  ├── SEC Filings: Regex keyword extraction                      │
│  │     Counts: "bankruptcy", "subpoena", "delisting",           │
│  │     "material weakness", "going concern", "fraud"           │
│  ├── Activation: SLM models fail to load                       │
│  └── Use: Keyword scoring, EPS surprise, regulatory flags      │
└─────────────────────────────────────────────────────────────────┘
```

**Tier Selection Logic (automatic, at startup and on each analysis call):**
```python
class NLPEngine:
    def analyze(self, text: str, symbol: str) -> NLPResult:
        if self.llm_available and self.config.llm_mode != "DISABLED":
            try:
                return self._tier1_llm(text, symbol)
            except (TimeoutError, ConnectionError):
                self._log_fallback(symbol, tier=1)
        if self.slm_available:
            try:
                return self._tier2_slm(text, symbol)   # FinBERT/ONNX
            except Exception:
                self._log_fallback(symbol, tier=2)
        return self._tier3_vader(text, symbol)           # Always works
```

All fallbacks are logged to `llm_fallback_log` table. The `llm_mode` control flag is hot-switchable from the UI Settings tab.

---

### 2.3 Core Python Libraries

**Data & Math:**
`pandas 2.2.2`, `numpy 1.26.4`, `scipy 1.13.0`, `pandas-ta 0.3.14b`, `ta-lib` (compiled), `duckdb 0.10+`, `pyarrow 16.0`, `numba 0.59+`.

**ML & Quant:**
`scikit-learn 1.5.0`, `hmmlearn 0.3.2`, `statsmodels 0.14.2`, `pyportfolioopt 1.5.5`, `riskfolio-lib 5.x`, `cvxpy 1.5`, `filterpy 1.4.5` (Kalman), `arch 6.x` (GARCH), `lightgbm 4.x`, `optuna 3.6`.

**NLP — Tier 2 (SLM, Default):**
`transformers 4.40+`, `onnxruntime 1.18+`, `optimum[onnxruntime]` (model export), `sentence-transformers`.

**NLP — Tier 1 (LLM, Optional):**
`ollama 0.2.1`, `anthropic`, `openai`.

**NLP — Tier 3 (Always-On Fallback):**
`nltk`, `vaderSentiment`.

**Options:**
`py_vollib_vectorized 0.1.2`, `QuantLib-Python 1.33`.

**Brokers & Market Data:**
`schwab-py 1.2.0`, `robin_stocks 3.0.4`, `ib_insync 0.9.86`, `alpaca-trade-api 3.x`, `ccxt 4.x`, `web3 6.x`, `yfinance 0.2.x`, `polygon-api-client 1.x`, `finnhub-python`, `pytrends`, `praw`, `finvizfinance`, `nasdaqdatalink`, `alpha_vantage`, `sec-edgar-downloader`.

**State & Infra:**
`redis 5.x`, `aioredis 2.x`, `aiohttp 3.9.5`, `aiofiles`, `websockets 12.0`, `httpx`, `tenacity`, `structlog`, `prometheus-client`, `pydantic 2.7`, `pyotp`, `watchdog`.

**Dev & QA:**
`mypy 1.10.0`, `ruff 0.4.7`, `pytest 8.2.2`, `pytest-asyncio 0.23.7`, `hypothesis`.

---

### 2.4 Free API & Broker Inventory (Zero-Cost Principle)

> **Rule:** NEVER pay for data. Paid API? Find the free equivalent. Cache everything: if data was fetched today, use cached version for remaining calls.
> **Fallback chain:** `Schwab API → Robinhood API → yfinance → scrape → cache`

| Source | What It Provides | Free Limit | Library |
|---|---|---|---|
| **Robinhood** | Quotes, options chain, crypto, fractional, 24/7 | Unlimited (personal) | `robin_stocks` |
| **Schwab** | Quotes, Level 2, options, equity orders, account | Unlimited (personal) | `schwab-py` |
| **Yahoo Finance** | OHLCV history 20yr+, fundamentals, earnings calendar | Unlimited | `yfinance` |
| **FRED (St. Louis Fed)** | 800k macro series: rates, CPI, GDP, employment | Unlimited | `fredapi` |
| **SEC EDGAR** | All 10-K, 10-Q, 8-K, Form 4, 13F filings | Unlimited | `sec-edgar-downloader` |
| **CBOE** | VIX data, options settlement, historical IV | Unlimited (public) | `requests` scrape |
| **US Treasury** | Daily yield curve (2Y, 5Y, 10Y, 30Y) | Unlimited | `requests` JSON |
| **CFTC** | Commitment of Traders (COT) weekly positioning | Unlimited | `requests` JSON |
| **OpenInsider** | Form 4 insider buying/selling | Unlimited (scrape) | `requests+bs4` |
| **housestockwatcher.com** | Congressional trade disclosures | Unlimited (scrape) | `requests+bs4` |
| **Finviz** | Stock screener, sector maps, news | Unlimited (scrape) | `finvizfinance` |
| **StockAnalysis.com** | Earnings, revenue, short interest, IPO calendar | Unlimited (scrape) | `requests+bs4` |
| **Reddit (PRAW)** | WSB, stocks, investing sentiment | Unlimited | `praw` |
| **Google Trends** | Search volume for tickers/products | Unlimited | `pytrends` |
| **NewsAPI.org** | Financial news headlines | 100 req/day free | `newsapi-python` |
| **GNews API** | News search | 100 req/day free | `requests` |
| **Unusual Whales (free)** | Options flow public feed (partial) | Limited free | `requests` |
| **FINRA ATS (dark pools)** | Off-exchange trade reporting, T+1 | Unlimited (public) | `requests` |
| **CryptoCompare** | Crypto OHLCV, social sentiment | 100k calls/month | `cryptocompare` |
| **Binance Public API** | Crypto prices, order book, funding rates | Unlimited (no key) | `python-binance` |
| **Coinbase Advanced** | Crypto spot prices, order book | Unlimited (no key) | `requests` |
| **Alpha Vantage** | Equity, forex, crypto | 25 req/day free | `alpha_vantage` |
| **Glassnode (free tier)** | BTC/ETH on-chain basics | Limited free | `requests` |
| **EIA.gov** | Energy inventory reports (weekly crude/gas) | Unlimited | `requests` JSON |
| **alternative.me** | Crypto Fear & Greed Index | Unlimited | `requests` |
| **StockTwits** | Cashtag message velocity | Unlimited (scrape) | `requests+bs4` |
| **Estimize** | Crowd EPS vs Street consensus | Limited free scrape | `requests+bs4` |
| **Ollama (local)** | LLM inference | Unlimited (local) | `ollama` |
| **HuggingFace (local)** | FinBERT, DistilRoBERTa via ONNX | Unlimited (local) | `transformers`, `onnxruntime` |

---

### 2.5 Enhanced Directory Structure

```
C:\TradingSystem\
├── engine\
│   ├── api\
│   │   ├── engine_api.py           # FastAPI on :8765
│   │   ├── websocket_manager.py    # WebSocket broadcast hub
│   │   └── metrics.py              # Prometheus metrics definitions
│   ├── brain\
│   │   ├── opportunity_ranker.py
│   │   ├── daily_pnl_manager.py    # DailyPnLManager + DailyTargetConfig
│   │   ├── capital_allocator.py
│   │   ├── signal_aggregator.py    # Cross-strategy dedup
│   │   └── state_cache_manager.py  # Redis primary / asyncio fallback
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
│   │   ├── level2_data.py
│   │   ├── dark_pool_data.py
│   │   ├── on_chain_data.py
│   │   └── news_stream.py          # Real-time news WebSocket feed
│   ├── database\
│   │   ├── models.py               # SQLAlchemy ORM (SQLite) — 18 tables
│   │   ├── analytics_db.py         # DuckDB analytics layer
│   │   ├── session.py
│   │   └── migrations.py
│   ├── execution\
│   │   ├── order_router.py
│   │   ├── execution_engine.py
│   │   └── algo_orders.py
│   ├── meta_brain\
│   │   ├── regime_detector.py      # HMM + LightGBM ensemble
│   │   ├── allocator.py            # Thompson Sampling + strategy correlation penalty
│   │   ├── nlp_engine.py           # 3-Tier NLP dispatcher
│   │   ├── llm_analyst.py          # Tier 1 (optional)
│   │   ├── slm_scorer.py           # Tier 2 FinBERT/ONNX (default)
│   │   ├── keyword_scorer.py       # Tier 3 VADER/NLTK (fallback)
│   │   ├── portfolio_optimizer.py
│   │   ├── kalman_smoother.py
│   │   └── online_learner.py
│   ├── risk\
│   │   ├── risk_manager.py         # 15-step pipeline
│   │   ├── compliance.py
│   │   ├── greeks_monitor.py
│   │   └── margin_optimizer.py
│   ├── scanner\
│   │   ├── opportunity_scanner.py
│   │   ├── stock_screener.py
│   │   ├── options_flow_scanner.py
│   │   └── dark_pool_scanner.py
│   ├── scheduler\
│   │   └── jobs.py                 # 16-step 24-hour schedule
│   ├── strategies\
│   │   ├── base_strategy.py        # BaseStrategy ABC + StrategyLoader
│   │   ├── equity\
│   │   │   ├── momentum\           # EQ-01, A1–A13
│   │   │   └── mean_reversion\     # EQ-03, B1–B14
│   │   ├── options\                # OP-01–OP-12, C4, C6–C9
│   │   ├── crypto\                 # CR-01–CR-07
│   │   ├── macro\                  # F1–F18
│   │   ├── quant\                  # EQ-02, E1–E16
│   │   ├── sentiment\              # D1–D16
│   │   ├── cash_hedging\           # CM-01–CM-12, EQ-04/EQ-05
│   │   ├── leveraged\              # G1–G4
│   │   ├── commodities\            # CO-01, CO-02
│   │   ├── volatility\             # VX-01, VX-02
│   │   ├── alternatives\           # AL-01, AL-02, AL-03
│   │   └── fx_fi\                  # FX-01–FX-05, FI-01–FI-04
│   ├── tax\
│   │   ├── tax_engine.py
│   │   ├── tax_optimizer.py
│   │   └── tax_reporter.py
│   ├── backtest\
│   │   ├── backtester.py
│   │   ├── walk_forward.py
│   │   ├── monte_carlo.py
│   │   └── performance_stats.py
│   ├── notifications\
│   │   ├── alert_manager.py
│   │   └── channels.py
│   ├── main.py
│   └── config.py
├── ui\
│   ├── ui_server.py
│   └── static\
│       ├── index.html
│       ├── app.js
│       ├── tabs\
│       │   ├── overview.js         # Tab 1: Command Center
│       │   ├── strategies.js       # Tab 2: Strategy Command Center
│       │   ├── positions.js        # Tab 3: Positions & Orders
│       │   ├── analytics.js        # Tab 4: Performance Analytics
│       │   ├── options.js          # Tab 5: Options Dashboard
│       │   ├── scanner.js          # Tab 6: Live Scanner
│       │   ├── tax.js              # Tab 7: Tax & Ledger
│       │   ├── backtest.js         # Tab 8: Backtest Console
│       │   ├── health.js           # Tab 9: System Health
│       │   └── settings.js         # Tab 10: Settings & Tuning
│       ├── components\
│       │   ├── chart_equity.js
│       │   ├── chart_heatmap.js
│       │   ├── chart_greeks.js
│       │   ├── trade_replay.js     # Trade Replay modal
│       │   ├── notification_center.js
│       │   └── nlp_insights.js
│       ├── lib\                    # Locally vendored Chart.js, D3, LW-Charts
│       └── styles.css
├── shared\
│   ├── trading.db
│   └── analytics.duckdb
├── logs\
│   ├── engine.jsonl
│   ├── trades.jsonl
│   └── errors.jsonl
├── data_cache\
│   ├── features\
│   ├── models\
│   ├── backups\
│   └── reports\
├── config\
│   ├── settings.toml
│   ├── broker_secrets.env
│   └── proxy_swap_map.json
├── scripts\                        # Utility scripts
│   ├── fetch_history.py            # Warm historical data cache
│   ├── first_run_setup.py          # Interactive first-run wizard
│   ├── export_model.py             # Export FinBERT to ONNX format
│   └── check_health.bat / .sh
├── run_engine.bat
├── run_ui.bat
├── install_service.bat
├── install_dependencies.bat
└── tests\
    ├── unit\
    ├── integration\
    └── strategy_simulations\
```

---

## 3. DATABASE SCHEMA & STATE MANAGEMENT

AQTA uses a **dual-database architecture**: SQLite (WAL mode) for real-time operational writes, DuckDB for analytical reads. The `StateCacheManager` handles all fast in-memory state using Redis (primary) or asyncio (fallback).

### 3.1 SQLite Operational Tables (18 Tables)

**Core Trading (unchanged from v2):**
`trades`, `positions`, `orders`, `signals_queue` — see v2.0 schema with additions noted below.

**`trades` additions:** `algo_type`, `algo_params_json`, `settlement_session` (`REGULAR` | `AFTER_HOURS`).

**`positions` additions:** `rho`, `portfolio_delta_contribution`, `iv_at_entry`, `iv_current`, `trailing_stop_pct`.

**Tax & Compliance (unchanged from v2):**
`tax_lots`, `wash_sale_blacklist`, `estimated_tax_payments`, `tax_harvest_log`, `compliance_audit_log`, `tax_optimization_decisions`.

**`tax_lots` additions:** `amt_adjustment` (float).
**`wash_sale_blacklist` additions:** `proxy_score` (float, 0–1).

**Intelligence & ML (unchanged from v2):**
`strategy_performance`, `market_regime_log`, `alpha_signals_log`, `opportunity_scans`, `alternative_signals`, `feature_store`, `backtest_results`.

**Capital & System State (unchanged from v2):**
`portfolio_snapshots`, `daily_cycle_log`, `profit_wallet`, `recovery_sessions`, `control_flags`, `hedge_positions`.

**`daily_cycle_log` additions:** `preliminary_pnl` (float, regular session only), `final_pnl` (float, after after-hours), `after_hours_pnl` (float), `settlement_timestamp_preliminary` (str), `settlement_timestamp_final` (str).

**`control_flags` — Complete Default Rows:**

| Key | Default | Description |
|---|---|---|
| `trading_enabled` | `true` | Master kill switch |
| `shadow_mode` | `true` | Paper trading (SAFETY — always start here) |
| `llm_mode` | `DISABLED` | `DISABLED` / `LOCAL` / `CLOUD` |
| `llm_cloud_fallback` | `false` | Allow cloud LLM if local unavailable |
| `tlh_enabled` | `true` | Tax-loss harvesting |
| `crypto_enabled` | `false` | Crypto strategies |
| `options_enabled` | `false` | Options strategies |
| `meta_brain_enabled` | `true` | HMM + regime detection |
| `redis_enabled` | `false` | Redis state cache |
| `prometheus_enabled` | `false` | Metrics endpoint |
| `dark_pool_enabled` | `false` | Dark pool scanning |
| `level2_enabled` | `false` | L2 order book feed |
| `intraday_strategies_enabled` | `true` | Intraday sub-strategies |
| `macro_strategies_enabled` | `true` | Macro/thematic strategies |
| `leveraged_strategies_enabled` | `false` | Group G strategies (BULL only) |
| `after_hours_strategies_enabled` | `false` | A13, B9 after-hours strategies |
| `volatility_targeting_enabled` | `true` | CM-05 vol-target overlay |
| `auto_rebalance_enabled` | `true` | Weekend portfolio rebalance |
| `engine_status` | `STOPPED` | Runtime state |
| `main_cycle_interval_minutes` | `5` | Cycle interval (1–10) |
| `target_override_usd` | `` | Empty = use dynamic % calc |
| `target_override_pct` | `` | Empty = use settings.toml |
| `max_open_positions` | `10` | Concurrent position limit |
| `halt_reason` | `` | Set on halt |
| `engine_heartbeat` | `` | Updated every 60s by health_monitor |

---

### 3.2 New Tables (v3 Additions)

**`llm_fallback_log`:** Tracks every NLP tier downgrade.
`id` (PK), `timestamp`, `symbol`, `data_source`, `tier_attempted` (1/2/3), `tier_used` (2/3), `fallback_reason`, `vader_score` (float), `finbert_score` (float), `regex_hit_count` (int), `action_taken`.

**`strategy_correlation_matrix`:** Daily rolling strategy correlation.
`id` (PK), `date` (Unique), `matrix_json` (full N×N matrix of Pearson correlations between all active strategies' daily P&L). Updated nightly by `online_learner.py`.

**`dark_pool_prints`:** Off-exchange dark pool print log.
`id` (PK), `timestamp`, `symbol`, `price`, `volume`, `notional_value`, `is_sweep` (bool), `exchange_code`, `direction_inferred` (BUY/SELL/NEUTRAL), `5m_candle_direction` (POST-PRINT follow-up).

**`options_positions`:** Dedicated options tracking (supplements `positions`).
`id` (PK), `underlying`, `expiry`, `strike`, `option_type` (CALL/PUT), `qty`, `premium_paid`, `delta`, `gamma`, `theta`, `vega`, `rho`, `iv`, `days_to_expiry`, `broker`, `strategy_id`, `opened_at`, `closed_at`, `realized_pnl`.

**`greeks_snapshots`:** Hourly portfolio Greeks snapshots.
`id` (PK), `snapshot_time`, `net_delta`, `net_gamma`, `net_theta`, `net_vega`, `net_rho`, `positions_count`, `portfolio_nav`.

**`crypto_positions`:** DeFi and on-chain positions.
`id` (PK), `token`, `network`, `wallet_address`, `qty`, `avg_cost`, `protocol_staked`, `apy`, `last_harvest`, `current_value`.

**`funding_rate_log`:** Crypto perpetual funding rates.
`id` (PK), `symbol`, `exchange`, `rate` (float, /8h), `timestamp`, `cumulative_8h_periods`.

---

### 3.3 DuckDB Analytics Schema

DuckDB stores denormalized, read-optimized copies of closed trades and signals. ETL runs nightly at 23:55 ET. Key tables: `fact_trades`, `fact_signals`, `dim_strategy`, `dim_regime`, `agg_daily_pnl`, `agg_tax_summary`, `agg_strategy_correlation`.

---

## 4. DATA INGESTION & ALTERNATIVE DATA ENGINE

All data fetching is asynchronous. Blocking libraries wrapped in `run_in_executor`. Local Parquet cache with TTL enforcement. Rate limits enforced by `asyncio.Semaphore` per API provider.

### 4.1 Market Data Enhancements (v3)

**Multi-Timeframe Data:** Simultaneously fetches 1m, 5m, 15m, 30m, 1h, and daily bars for intraday strategies. `MultiTimeframeData` dataclass aggregates timeframes.

**Additional Indicators:** KAMA(10,2,30), VWAP (intraday rolling), Parabolic SAR, Ichimoku Cloud (tenkan, kijun, senkou A/B, chikou), Donchian Channels(20), Keltner Channels(20,2), Heikin Ashi, Connors RSI (CRSI using RSI + Streak RSI + ROC), Volume Profile (POC, VAH, VAL per intraday session), T-WAP (time-weighted average price from session open).

**Real-Time News Stream (`news_stream.py`):** Subscribes to Benzinga/Polygon real-time news WebSocket (if API key available). Feeds headlines directly to `NLPEngine` via asyncio queue. Strategy D11 (SLM News Flash) consumes this queue for sub-50ms signal generation.

**Pre-Market Scanning (04:00–09:30 ET):** Runs every 5 minutes. Detects stocks gapping >5% with volume >100k shares. Identifies pre-market VWAP for A12 (Pre-Market Catalyst Drift) entries.

**After-Hours Quote Feed:** Continuous quote monitoring from 16:00–20:00 ET via Robinhood or Alpaca extended hours feed. Powers strategies A13 and B9.

**EIA Energy Reports:** Weekly Wednesday scrape of `eia.gov` crude/gas inventory data. Parsed and stored in `alternative_signals` with source=`EIA_INVENTORY`. Powers F8.

**Global Session Monitor:** Tracks Nikkei 225 (^N225), FTSE 100 (^FTSE), DAX (^GDAXI) via yfinance. At 03:00 ET (Asian close) and 09:00 ET (European mid-session), calculates session return. Powers F10.

### 4.2 Opportunity Scanner — Complete Architecture

```
LEVEL 1 — MARKET REGIME ENGINE (HMM + LightGBM)
  Input: SPY 2yr daily, VIX, Yield Curve, Put/Call Ratio, Breadth
  Output: {regime_state, bull_prob, crash_prob, vol_regime, ensemble_agreement}
  Frequency: Every 30 minutes

LEVEL 2 — OPPORTUNITY RANKER
  Input: All 1,500+ symbols across universe
  Process: Tier 1 filters → Tier 2 scoring → rank
  Output: Top 25 opportunities with composite scores
  Frequency: Every MAIN_CYCLE_INTERVAL_MINUTES minutes

LEVEL 3 — STRATEGY MATCHER
  Input: {opportunity, regime_state, portfolio_state, capital_available}
  Process: For each opportunity → find compatible strategies → score fit
  Output: (opportunity, strategy, priority_score) tuples
  Frequency: Per opportunity, every cycle

LEVEL 4 — PORTFOLIO CONSTRUCTOR
  Input: All (opportunity, strategy) pairs
  Process:
    - Correlation check with existing positions
    - Apply Kelly sizing × regime multiplier × state multiplier
    - Check total risk budget (max 6% portfolio at risk simultaneously)
    - Check max_open_positions limit
    - Apply strategy correlation matrix penalty (if two strategies
      have correlation > 0.8, penalize lower-performing weight)
    - OPPORTUNITY_SURGE: if ≥5 HIGH-conviction setups, raise deployment to 90%
  Output: Final approved trade list with sizes
  Frequency: Per cycle, final approval gate

LEVEL 5 — RISK GATE (15-Step Pipeline, NEVER bypassed)

LEVEL 6 — TAX-AWARE ORDER BUILDER
  Before any sell: check lot ages → wash-sale → net after-tax gain
  If net after-tax gain < threshold → delay sale, hedge with options instead
  Output: Final orders with lot-level tax optimization
```

**Opportunity Types Detectable:**

```
MOMENTUM PLAYS:
  - Breakout: price above 52-week high with volume surge
  - Gap-and-Go: pre-market gap > 3%, holding VWAP at open
  - Trend Continuation: ADX > 30, pullback to EMA-21, resuming
  - Opening Drive: top 1% volume in first 5 minutes
  - Pre-Market Catalyst: > 5% gap on volume > 100k pre-market

MEAN REVERSION:
  - Oversold Bounce: RSI < 28, price at lower Bollinger Band, reversal candle
  - Gap Fill: gap up/down, filling back toward prior close
  - VWAP Reversion: deviation > 1.5% from VWAP
  - POC Reversion: drift > 1% from intraday Point of Control
  - Extended Hours Spike: fat-finger or panic spike > 3% in thin AH market

CATALYST PLAYS:
  - Pre-Earnings Drift: 3 days before earnings, strong NLP sentiment
  - Post-Earnings Surprise: beat + raised guidance + positive NLP score
  - Insider Cluster Buy: 3+ officers buying same week (Form 4)
  - C-Suite Conviction: CEO/CFO open-market buy > $250k
  - Congress Trade Follow: senator bought → replicate within 48h
  - After-Hours Beat: EPS > 10% beat + raised guidance at 16:01 ET

VOLATILITY / OPTIONS PLAYS:
  - IV Crush: sell straddle before earnings
  - VIX Spike: VIX > 25 → buy volatility products
  - Low IV Expansion: straddles when IV rank < 15%
  - Tail Risk: VIX < 12 + SPY at ATH → VIX calls

ARBITRAGE / STRUCTURAL:
  - ETF Pairs: SPY vs IVV, QQQ vs ONEQ
  - S&P 500 Inclusion: announced addition before effective date
  - ETF Component Dispersion: SPY vs constituent basket
  - Overnight Index Arb: SPY vs ES futures overnight drift
  - Leveraged ETF Decay: TQQQ vs QQQ

CRYPTO:
  - BTC Funding Rate: positive → short bias; negative → long
  - Crypto-Equity Correlation Break: BTC diverging from NASDAQ
  - Fear & Greed Extreme: < 20 accumulate; > 80 reduce

DARK POOL / FLOW:
  - Large Off-Exchange Print: > 5% of daily average volume
  - Bullish Options Sweep: volume > OI × 2, net premium > $100k
  - Dark Pool Accumulation: dark_pool_pct > 40% for 3 days, flat price
```

---

## 5. BROKER INTEGRATION & SMART ORDER ROUTING

*(Core v2.0 architecture retained; additions below)*

### 5.1 Universal Broker Interface — v3 Additions

New abstract methods: `get_level2_snapshot(symbol)`, `get_options_chain_greeks(symbol, expiry)`, `get_margin_status()`, `get_after_hours_quote(symbol)`.

**Circuit Breaker Enhancement:** Transient network errors (5xx, timeout) retry with exponential backoff (1s, 2s, 4s + jitter, max 5 retries). Authentication errors (401, 403) trigger immediate re-auth flow without circuit-open. Both circuit state and error counts reset after 5 minutes of clean calls.

### 5.2 Smart Order Router — v3 (8 Rules)

1. Shadow Mode → `MockBroker`.
2. Emergency/Halt liquidation → `IBKRBroker` (fastest fills).
3. After-Hours (A13, B9) → `RobinhoodBroker` or `AlpacaBroker` (extended hours).
4. CRYPTO → `CoinbaseBroker` (primary), `RobinhoodBroker` (fallback).
5. OPTION → `SchwabBroker` (primary), `IBKRBroker` (complex, >2 legs).
6. Notional > $100k → `IBKRBroker`.
7. Fractional (qty < 1.0) → `RobinhoodBroker`.
8. Standard equity → Best bid/ask across `SchwabBroker` + `AlpacaBroker`; default `SchwabBroker`.

### 5.3 Execution Algorithms

| Algorithm | Use Case | Logic |
|---|---|---|
| MARKET | Urgency: stop triggers, halt liquidation, News Flash (D11) | Direct market order |
| LIMIT | Standard entry/exit | Joins bid/ask midpoint; chases at configurable tick increments |
| TWAP | Large orders over time | Equal slices over configurable window (default 20 min) |
| VWAP | Market-impact minimization | Slices per 5-min historical volume profile |
| ICEBERG | Conceal order size | Shows 10% to market; auto-refills |
| POV | Track market volume % | Targets 15–20% of real-time volume |
| SNIPER | Short-lived momentum (D11, A9) | IOC at ask + 1 tick; cancels if unfilled in 200ms |
| CLOSE_ONLY | MOC/LOC orders | Market-on-close or limit-on-close before 15:55 ET |
| AH_LIMIT | After-hours (A13, B9) | Limit at mid-price with wide tolerance; no market orders AH |

---

## 6. THE META-BRAIN (AI & QUANT CORE)

### 6.1 Market Regime Detector — HMM + LightGBM Ensemble

**Model A — GaussianHMM:** `n_components=6, covariance_type="full", n_iter=500`. Features: 2 years SPY daily. `X = [daily_return, log_volume, vix_norm, atr_norm, macd_hist_norm, yield_spread_10y2y, put_call_ratio, obv_change_norm, adv_decline_ratio, pct_above_200d_ma]`.

**Model B — LightGBM Classifier:** 5 years of labeled regimes. Features: all HMM inputs + credit spreads (HYG/TLT ratio), VIX term structure slope (VIX9D/VIX3M). Outputs 6-class probability distribution.

**Ensemble:** Weights HMM=0.45, LightGBM=0.55. `ensemble_agreement = max(probability_vector)`. If < 0.45: regime = `UNCERTAIN`, all position sizes reduced 25%.

**Regime Multipliers (per strategy family):**

| Regime | Trend | MeanRev | Arb | Macro | Hedge | LLM/Sentiment |
|---|---|---|---|---|---|---|
| BULL_TREND | 1.5 | 0.5 | 1.0 | 1.2 | 0.5 | 1.2 |
| BEAR_TREND | 0.2 | 1.3 | 1.0 | 1.3 | 1.5 | 0.8 |
| SIDEWAYS_LOW | 0.3 | 1.5 | 1.5 | 0.8 | 1.2 | 1.0 |
| SIDEWAYS_HIGH | 0.5 | 1.2 | 1.2 | 1.0 | 1.5 | 0.9 |
| CRASH_RISK | 0.0 | 0.0 | 0.5 | 0.5 | 2.0 | 0.0 |
| RECOVERY | 0.7 | 1.3 | 1.0 | 0.8 | 1.0 | 0.7 |

### 6.2 Contextual Thompson Sampling Allocator

```python
class ContextualThompsonSampler:
    """
    Each (strategy_id, regime, time_of_day_bucket) has its own Beta(alpha, beta).
    Time-of-day buckets: PRE_MARKET, OPEN_HOUR, MID_MORNING, LUNCH, AFTERNOON,
                         POWER_HOUR, AFTER_HOURS.

    Bayesian Update (magnitude-weighted):
      Win → alpha += 1 + (pnl_pct / avg_win_pct)
      Loss → beta  += 1 + abs(pnl_pct / avg_loss_pct)

    Strategy Correlation Penalty:
      Reads strategy_correlation_matrix for today.
      If two strategies have correlation > 0.8, penalizes the weight of the
      lower-performing one by multiplying its score by (1 - (r - 0.8) / 0.2),
      ensuring true diversification even when Thompson Sampling converges on
      correlated winners.

    Anti-Concentration: No strategy > 30% allocation.
    Floor: Each enabled strategy receives minimum 5% allocation.
    """
```

### 6.3 Dynamic Strategy Loader (`base_strategy.py`)

Every strategy must implement `health_check() -> HealthStatus`:

```python
@dataclass
class HealthStatus:
    ok: bool
    status: str          # "HEALTHY" | "DISABLED_USER" | "DISABLED_ERROR"
    error_message: str | None
    resolution_steps: list[str]  # Human-readable fix instructions shown in UI tooltip
    data_dependencies: list[str] # APIs/data this strategy requires

# Example HealthStatus for a strategy that needs Polygon.io:
HealthStatus(
    ok=False,
    status="DISABLED_ERROR",
    error_message="Polygon API timeout after 3 attempts",
    resolution_steps=[
        "Check POLYGON_KEY in config/broker_secrets.env",
        "Test: curl https://api.polygon.io/v2/aggs/... —key YOUR_KEY",
        "Or run: python scripts/test_polygon.py",
        "Fallback: Set data_provider=yfinance in settings.toml"
    ],
    data_dependencies=["polygon.io", "options_chain"]
)
```

**Loader behavior:**
- At startup, `StrategyLoader` runs `health_check()` on all 160+ strategies concurrently.
- Failed strategies → `STATUS = "DISABLED_ERROR"` in `strategy_performance` table; engine continues.
- UI (Tab 2: Strategy Command Center) shows a red dot with hover tooltip displaying error and resolution.
- Retry: health checks re-run every 30 minutes; strategies auto-re-enable if their `health_check()` passes.

### 6.4 NLP Engine — Full Dispatch Logic

```
analyze_news(symbol, headlines) →
  Tier 1 (LLM, if llm_mode != DISABLED and available):
    Returns: {sentiment_score: 0-100, direction: BULLISH/BEARISH/NEUTRAL,
              confidence: 0.0-1.0, time_horizon: INTRADAY/SWING/LONG_TERM}
    Cached for 4 hours in alpha_signals_log metadata.
    Logged to llm_fallback_log with tier=1.

  Tier 2 (SLM — FinBERT/ONNX, if model loaded):
    Batch tokenize all headlines → ONNX inference → positive/negative/neutral
    Returns: {sentiment_score: 0-100, direction, confidence}
    Inference time: <50ms per batch.
    Logged to llm_fallback_log with tier=2.

  Tier 3 (VADER/NLTK, always available):
    VADER compound score → BULLISH (>0.5) / BEARISH (<-0.5) / NEUTRAL
    Returns: {sentiment_score: 0-100, direction, confidence: 0.6 fixed}
    Logged to llm_fallback_log with tier=3.

analyze_earnings(symbol, transcript_or_eps_data) →
  Tier 1: {guidance_revision, surprise_factor, management_confidence, tone_score}
  Tier 2: FinBERT on transcript text
  Tier 3: Numerical EPS surprise = (actual - estimate) / abs(estimate) × 100

analyze_sec_filing(symbol, filing_text) →
  Tier 1: {risk_score, key_risks, trend_vs_prior_year}
  Tier 2: DistilRoBERTa-financial
  Tier 3: Regex count of risk keywords → risk_score = count × 10 (capped at 100)
```

### 6.5 Portfolio Optimizer

*(v2.0 retained: MVO, CVaR-MVO, HRP, regime-conditional covariance, transaction cost penalty)*

**v3 Addition — Stress Test Scenarios:** Run nightly after settlement. Tests current portfolio against: 2008 Financial Crisis, 2020 COVID Crash, 2022 Rate Shock. Results stored in `portfolio_snapshots.stress_test_json`. Alerts if any scenario produces > 15% portfolio drawdown.

---

## 7. STRATEGY ARSENAL (160+ STRATEGIES)

All strategies inherit from `BaseStrategy(ABC)` and implement `generate_signals()`, `calculate_position_size()`, `_rule_based_fallback()`, and `health_check()`.

**Default Sizing:** Kelly Criterion `f = (win_rate/avg_loss − (1−win_rate)/avg_win) × 0.25`, capped at 10% of equity.

---

### 7.1 Equity Momentum & Intraday — PRIMARY (EQ-01 to EQ-10, A1–A18)

*(All strategies from v2.0 retained; additions below)*

**A8 / VWAP MACD Crossover (1-min intraday):**
Runs on the 1-minute micro-cycle. BUY when 1-min MACD histogram crosses above zero line while price is above the session VWAP. Confirmation: VWAP slope positive, volume above 5-min average. Stop: VWAP − 0.3× ATR. Hold: 20–60 minutes. Small size (0.4× Kelly). Requires `intraday_strategies_enabled = true`.

**A9 / Opening Drive Momentum:**
Detects extreme volume in the first 5 minutes (top 1% of historical 5-min volume for that symbol). Enters in the direction of the 5-minute candle at 9:35 AM. Tight trailing stop (0.5× ATR). Targets measured move equal to the opening 5-min range. If no fill by 9:40 AM, cancel. Hold: 30–90 minutes.

**A10 / EOD Imbalance Fade:**
At 15:50 ET, reads NYSE MOC imbalance data (Polygon or IBKR feed). If imbalance is a net BUY > $500M for a single stock, enters a SHORT position at 15:55 ET anticipating a reversion from the forced buy-imbalance close price. Exits via MOC sell at 16:00 ET. Small size (0.35× Kelly). Opposite strategy for net SELL imbalance > $500M.

**A11 / T-WAP Trend Follow:**
Calculates a dynamic TWAP from session open. Buys pullbacks to the TWAP line if: (1) TWAP is sloping upward, (2) SPY tick index (NYSE uptick − downtick count) > +500. Stop: below TWAP − 0.25× ATR. Target: prior intraday resistance. Requires `level2_enabled = true` for tick index; falls back to A/D ratio if unavailable.

**A12 / Pre-Market Catalyst Drift (04:00–09:30 ET):**
Scans for stocks gapping > 5% in pre-market with volume > 100k shares, confirmed by positive NLP sentiment score > 0.6. Buys pullbacks to the pre-market VWAP (calculated from 04:00 ET open). Stop: pre-market low. Target: +3% from pre-market VWAP. Uses after-hours broker routing (Robinhood/Alpaca). Size: 0.4× Kelly. Signals expire at 09:30 ET.

**A13 / After-Hours Earnings Momentum (16:00–20:00 ET):**
Parses EPS/Revenue results at 16:01 ET using SLM (FinBERT/ONNX) or Tier 3 numerical EPS surprise. If beat > 10% AND guidance raised (detected via NLP or Tier 3 Finnhub data): enters BUY in after-hours session. Uses `AH_LIMIT` algo order at mid-price. Stop: 3% below entry. Target: +5%. Requires `after_hours_strategies_enabled = true`. Size: 0.4× Kelly.

---

### 7.2 Equity Mean Reversion — PRIMARY (EQ-03, B1–B14)

*(All strategies from v2.0 retained; additions below)*

**B6 / Connors RSI Pullback:**
Connors RSI (CRSI) combines: RSI(3) + Streak RSI (RSI of consecutive win/loss days) + 100-day ROC percentile. BUY when CRSI < 10 on a stock that is ABOVE its 200-day SMA (still in long-term uptrend). The 200-day filter prevents buying in structural downtrends. Stop: 2× ATR below entry. Target: CRSI > 50 (momentum restored). Hold: 2–5 days.

**B7 / Standard Deviation Channel Fade:**
Calculates a 60-day linear regression channel with ±2 standard deviation bands. Enters SHORT when price touches or exceeds the +2 StdDev upper band with a bearish 5-minute reversal candle. Enters LONG at −2 StdDev lower band with a bullish candle. Stop: channel band + 0.5× ATR. Target: channel midline (regression line). Hold: 2–7 days. Regime: SIDEWAYS.

**B8 / Volume Profile POC Reversion:**
Calculates the intraday Point of Control (price level with the highest traded volume, updated rolling every 30 minutes). If price drifts > 1% from POC on below-average volume (less than 0.7× 20-period average), fades the deviation back toward POC. Stop: 1.5% adverse from entry. Target: POC retest. Hold: 30–120 minutes. Requires live intraday OHLCV bars.

**B9 / Extended Hours Liquidity Fade:**
Active 16:00–20:00 ET. Detects massive, low-liquidity price spikes in after-hours session — often caused by algorithmic overreaction, thin book, or retail panic. Trigger: price move > 3% in 5 minutes with volume < 20% of regular session average for that stock. Fades back to the 16:00 ET closing price. Uses `AH_LIMIT` algo. Stop: spike high + 0.5% (for shorts) or spike low − 0.5% (for longs). Very small size (0.3× Kelly). Requires `after_hours_strategies_enabled = true`.

---

### 7.3 Copy Trading & Sentiment — PRIMARY (D1–D16)

*(All strategies from v2.0 retained; additions below)*

**D8 / Social Media Cashtag Velocity:**
Scrapes StockTwits public feed and X (Twitter) for cashtag mentions via keyword search. Calculates `message_velocity = (current_hour_count − avg_last_7d_hour_count) / avg_last_7d_hour_count`. Trigger: velocity > 500% in 1 hour (5× average pace) with positive VADER sentiment (compound > 0.5). Requires stock to also have a positive technical setup (RSI 50–65, price above EMA-21). Size: 0.4× Kelly. Stop: 6%.

**D9 / C-Suite Conviction Buy:**
Specific filter from OpenInsider: CEO or CFO open-market purchase (not options exercise) exceeding $250,000. Receives double weight allocation compared to standard D2 insider cluster (2× Kelly fraction). Signal persists for 15 trading days. Priority over D2 when both fire on same symbol. Hold: 30–60 days.

**D10 / Dark Pool Print Tracking:**
Monitors FINRA TRF (Trade Reporting Facility) data. If a single off-exchange print exceeds 5% of the symbol's daily average volume in a single transaction: records in `dark_pool_prints`. Follows the direction of the subsequent 5-minute candle (confirms institutional intent). Requires `dark_pool_enabled = true`. Stop: prior candle high/low. Hold: 1–3 days.

**D11 / SLM News Flash:**
The fastest strategy in the system. Subscribes to real-time news WebSocket feed (Benzinga or Polygon). On each new headline: feeds directly into local ONNX FinBERT (Tier 2). If `sentiment > 0.9` AND `confidence > 0.95` AND stock is liquid (ADTV > $20M): executes a SNIPER order (IOC at ask + 1 tick) within 50ms of headline receipt, front-running retail reaction. Stop: 2% adverse. Target: 1.5% within 15 minutes. Very small size (0.3× Kelly). Logs latency: `headline_receipt_ns → order_submitted_ns`.

---

### 7.4 Quantitative & Statistical Arbitrage — PRIMARY (EQ-02, E1–E16)

*(All strategies from v2.0 retained; additions below)*

**E7 / Index Rebalancing Arbitrage (S&P 500 Inclusion):**
S&P 500 additions are publicly announced ~5 trading days before the effective rebalancing date. All passive index funds (trillions of AUM) must buy the stock at or before the effective date close. Strategy: buy the announced stock within 1 hour of announcement, hold until effective date. Target: effective date closing price (passive funds must buy here). Sell on the effective date via MOC order. Historical win rate > 70% with average gain 3–8%.

**E8 / ETF Component Dispersion Arbitrage:**
Calculates the implied price of SPY based on its top 50 holdings (weighted by index weight, using live quotes). If SPY spot price deviates > 0.1% from its calculated basket value: buys the cheaper instrument (SPY or basket) and shorts the expensive one. For the basket side, executes a mini-portfolio of 5 largest holdings (by weight) as a proxy. Day-trade only (closes by 15:55 ET). Requires low-latency quotes for all 50 holdings simultaneously. Size: 0.5× Kelly per leg.

**E9 / Kalman Filter Price Estimation:**
Uses a Kalman filter (via `filterpy`) to estimate the "true" underlying price of a noisy asset by tracking its state (price) and measurement noise (bid-ask spread, tick variance). When the actual trade price drops significantly below (or above) the Kalman-estimated state — more than 2 standard deviations of measurement noise — enters a position expecting reversion to the filter's estimated value. Stop: 3× the Kalman measurement noise band. Hold: 1–5 days. Pairs well with E12 (Kalman Filter Dynamic Pairs).

**E10 / Overnight Index Arbitrage:**
Compares the SPY closing price at 20:00 ET with the continuous ES futures (S&P 500 Futures, ticker: `ES=F`) price during overnight trading. If ES drifts > 0.5% overnight from the SPY 20:00 ET close without a corresponding macro news catalyst (checked via keyword scan): queues a SPY limit order for the 04:00 ET pre-market open to capture the convergence between futures and the underlying ETF. Stop: 1%. Target: 0.4% convergence (partial profit). Hold: 4:00 AM to 9:35 AM only.

---

### 7.5 Macro & Thematic Strategies — PRIMARY (F1–F18)

*(All strategies from v2.0 retained; additions below)*

**F7 / Yield Curve Inversion Play:**
Tracks 2Y/10Y Treasury yield spread via FRED (DGS2, DGS10). If the inversion deepens (spread becomes more negative by > 10 bps over 5 days): shorts Russell 2000 (IWM) — small caps are most vulnerable in a credit crunch — and buys Mega-Cap Tech (QQQ) — benefits from falling long-term rates implied by inversion. Reverse when spread un-inverts rapidly (spreads widen > 20 bps in 5 days → buy cyclicals). Hold: 10–20 days.

**F8 / Energy Inventory Surprise:**
Every Wednesday at 10:30 AM ET, EIA publishes weekly crude oil inventory report. Strategy: at 10:15 AM, fetches consensus estimate from EIA.gov or Bloomberg-free alternative. At 10:30 AM, parses the actual draw/build. If the draw is ≥ 2× larger than consensus (significantly bullish for oil prices): immediately buys USO (crude oil ETF) and XLE (energy equities) via SNIPER order. If build is ≥ 2× larger than consensus (bearish): shorts USO. Stop: 2% adverse. Target: 3%. Hold: 1–3 days.

**F9 / Currency-Hedged Equity Rotation:**
Monitors DXY (US Dollar Index via UUP ETF proxy) trend strength. If UUP ADX > 30 (strong dollar uptrend): international equity holders suffer currency drag — rotates international ETF exposure from unhedged (EFA, EEM) to currency-hedged equivalents (HEFA for developed markets, HEWJ for Japan). When ADX < 20 (weak dollar trend): rotates back to unhedged for currency tailwind. Rebalances weekly. Hold: 10–30 days.

**F10 / Global Session Handoff:**
Runs at 03:00 ET (Asian session close check) and 09:00 ET (European mid-session check). If BOTH Nikkei 225 and FTSE/DAX are up > 1.5% in the same session, applies a `global_bullish_multiplier = 1.3` to all US pre-market momentum strategy signal strengths (A3, A10, A12) for the day's opening hour. Reverse: if both down > 1.5%, reduces all opening-hour momentum signals by 30%. Does not generate independent trades; purely a multiplier on other strategies' sizing.

---

### 7.6 Cash Management & Hedging — PRIMARY (CM-01–CM-12, EQ-04, EQ-05)

*(All strategies from v2.0 retained; additions below)*

**CM-03 / T-Bill Laddering:**
Automatically allocates 30% of idle cash (cash not used by active strategies) to 4-week Treasury bills via IBKR's treasury direct access or secondary market ETF (BIL, SGOV). Rolls at maturity. Provides risk-free yield (~5% APY) without locking up capital for more than 4 weeks. Signals redemption 2 trading days before maturity to ensure cash is available. Coordinates with CM-01 (Money Market Sweep) to avoid double-deploying the same cash.

**CM-04 / Dividend Capture:**
Scans for high-yield stocks (dividend yield > 3%) 1 trading day before their ex-dividend date. Buys stock at the close of the pre-ex-dividend day. Sells ATM covered call on the same day to hedge delta (capture dividend with reduced directional risk). Unwinds the equity + call position within 3 days post-ex-dividend date. Net capture: dividend − call premium cost − slippage. Requires `options_enabled = true` for the hedge leg; equity-only version available if options disabled (lower efficiency).

**EQ-05 / Tail Risk Convexity:**
When VIX < 12 AND SPY is at or above its 52-week high (complacency + ATH): allocates 0.5% of portfolio to 60-DTE VIX call options at the 15 strike (currently far OTM). These are cheap long-volatility contracts that provide convex payoff in a market shock (VIX spikes to 30+ = 2× or 3× return on the position). Repurchased each month. Acts as portfolio insurance against black swan events. Requires `options_enabled = true`.

**CM-05 / Margin Interest Minimizer (15:55 ET Daily):**
Runs as a scheduled job at 15:55 ET daily. Checks current intraday leverage usage. If any margin (above Reg-T equity) was used during the day, automatically identifies the lowest-conviction open positions (by Kalman-smoothed signal strength) and reduces or closes them to ensure the overnight cash balance is positive, avoiding broker margin interest charges. Priority: liquidate leveraged positions before options before equity.

---

### 7.7 Group G — Leveraged & High-Octane Strategies (G1–G4)

> **WARNING:** Maximum position size: 5% of portfolio. Regime gate: BULL_TREND only (except G4). Requires `leveraged_strategies_enabled = true`. All stops strict. These strategies amplify both gains and losses.

**G1 / Leveraged ETF Trend Follow:**
In BULL_TREND regime only: enters TQQQ (3× NASDAQ) on MACD histogram crossover while EMA-9 > EMA-21 > EMA-50 on the TQQQ daily chart. Or SOXL (3× Semiconductors) when semiconductor sector (SOXX) shows similar alignment. Position: max 5% of portfolio. Strict stop: −5% from entry (leveraged ETFs can move 10%+ intraday). Exit: MACD histogram turns negative or regime leaves BULL_TREND. Hold: 2–10 days.

**G2 / Gamma Squeeze Detector:**
Detects stocks with short interest > 20% of float AND rapidly rising call option open interest (OI increasing > 50% in 5 days). When these conditions coincide: dealer delta hedging creates mechanical upward price pressure. Enters a small position in the stock (0.75× Kelly) OR near-dated call options at 0.30 delta (if options_enabled). Exit immediately at first sign of squeeze exhaustion: volume drop > 50%, MACD cross-down, or RSI > 80. Stop: −8%.

**G3 / Crypto Momentum Burst:**
BTC or ETH makes a > 3% price move in 1 hour (source: CryptoCompare free or Binance public API). Enters in the same direction with 2% portfolio allocation via Robinhood crypto. Stop: −1.5% from entry. Target: +3% (1:2 R:R). Exit if momentum stalls > 30 minutes (intraday crypto momentum is short-lived; mean-reversion kicks in after first hour). Requires `crypto_enabled = true`. Hold: 30 minutes–2 hours.

**G4 / Short Volatility Carry (SVXY):**
When VIX futures term structure is in steep contango (front-month VIX < back-month VIX3M by > 5%): the daily roll yield from holding SVXY (ProShares Short VIX ETF) is positive. Enters SVXY position (3% max portfolio). Exit: if VIX spikes > 20% in a single day (regime change; contango collapses). Stop: −10% on SVXY position. Annual return from contango in calm markets: 20–40%. Regime: any except BEAR_TREND or CRASH_RISK.

---

### 7.8 Commodities (CO-01, CO-02)

**CO-01 / Gold & Oil Momentum + CoT Report:**
Combines price momentum with CFTC Commitment of Traders (COT) report. Buys GLD if: (1) 20-day MA > 50-day MA, AND (2) CFTC net non-commercial (speculative) long position for gold futures (COMEX) > 200,000 contracts (bullish positioning). Buys USO for oil using same structure with WTI futures (NYMEX) COT data. COT data released Fridays; strategy updates positioning Monday morning. Hold: 2–4 weeks.

**CO-02 / Commodity Futures Roll Yield:**
When a commodity (Oil via USO, Natural Gas via UNG, Copper via COPX, Gold via GLD) is in **backwardation** (spot price > futures price = positive roll yield for long holders): enters long ETF position. When in **extreme contango** (spot < futures significantly = negative roll yield): avoids or shorts the ETF. Monitors term structure via yfinance futures tickers (CL=F, NG=F, GC=F, HG=F). Hold: 15–30 days, rolled.

---

### 7.9 Volatility Strategies (VX-01, VX-02)

**VX-01 / VIX Futures Term Structure (Short VIX Contango):**
When VIX futures term structure is in contango > 5% (front-month VIX < back-month VIX3M), the VIX futures roll down as time passes — providing a persistent short-vol carry. Implemented via SVXY (short VIX ETF) or by shorting VXX. Entry: contango > 5%. Exit: contango collapses (VIX spike > 20% intraday), or VIX3M/VIX ratio falls below 1.02. Position: 3% max. Annual carry: 20–40% in normal markets.

**VX-02 / Realized Vol Surface Fitting (Delta-Hedged Gamma):**
Fits a parametric volatility surface (cubic spline across strike × expiry) to the current options chain. Identifies where implied vol is significantly above realized vol (cheapest theta per dollar of vega). Sells a delta-neutral straddle at those strikes and delta-hedges the equity exposure using the underlying (or SPY for index plays). Dynamic rehedge every 0.10 delta move. Requires `options_enabled = true`. Most capital-intensive options strategy. Profit from: theta decay > cost of delta hedging.

---

### 7.10 Alternative & Structural Strategies (AL-01 to AL-03)

**AL-01 / REIT Dividend Capture + Mean Reversion:**
REITs are required to distribute 90%+ of taxable income as dividends. Strategy combines: (1) Income: buys high-yield REITs (dividend yield > 4%) near ex-dividend date (similar to CM-04 but REIT-specific with longer hold), and (2) Momentum/Reversion: trades REIT sector ETF (XLRE, VNQ) using RSI mean-reversion on 5-day timeframe. Regime: any (REITs are somewhat defensive). Hold: dividend capture 3–5 days; REIT mean-reversion 5–15 days.

**AL-02 / SPACs — NAV Floor Arbitrage:**
SPACs (Special Purpose Acquisition Companies) trade at a floor of ~$10 (their trust NAV per share) even if the market prices them higher or lower before a deal is announced. Strategy: buys SPACs trading at a discount to NAV (price < $9.90) — the NAV floor provides near risk-free downside protection while any deal announcement provides upside. Scans SPAC universe weekly via SEC EDGAR (S-1 filings). Position: 1% NAV per SPAC, max 5 concurrent SPACs. Hold: until deal announcement or NAV+2% target.

**AL-03 / Convertible Bond Arbitrage:**
Convertible bonds contain an embedded equity option. When the bond price is below its "fair value" (calculated as straight bond value + Black-Scholes value of the conversion option), there is a mispricing. Buys the convertible bond and hedges the equity delta by shorting the underlying stock. Profits from: (1) coupon income, (2) positive carry, (3) gamma (non-linear payoff). Requires IBKR (fixed income access) and `options_enabled = true` (for delta calculation). Very small allocation (0.5% NAV). Hold: 30–180 days.

---

### 7.11 Options Strategies — v3 Additions

*(All OP-01 to OP-12, C4, C6–C9 from v2.0 retained)*

**OP-05 / LEAPS Bull Spread (Sector ETFs):**
Buys a 12-month bull call spread on leading sector ETF (XLK, XLF, XLE, XLV). Structure: buy ITM call (0.70 delta, 12-month expiry) + sell OTM call (0.35 delta, same expiry). Net debit approximately 20–25% of the width between strikes. Targets 3:1 reward-to-risk ratio. Entry: sector shows BULL_TREND momentum with ADX > 25. Hold: 3–6 months (close at 50% of max profit or roll at 60 DTE remaining). Requires `options_enabled = true`.

---

### 7.12 Crypto Strategies — v3 Additions

*(All CR-01 to CR-07 from v2.0 retained)*

**CR-05 / BTC Halving Cycle Model** — unchanged from v2.
**CR-06 / Crypto Fear & Greed Contrarian** — enhanced: uses `alternative.me` API directly.
**CR-07 / DeFi Yield Capture** — unchanged from v2.

---

### 7.13 FX & Fixed Income — v3 Additions

*(All FX-01 to FX-05, FI-01 to FI-04 from v2.0 retained)*

---

### 7.14 Strategy-Regime Compatibility Matrix (Visual Reference)

```
                    BULL  BEAR  SIDE_LO  SIDE_HI  CRASH  RECOVERY
EQ-01 TREND_FOLLOW   ✓✓    ✗      ✗        ✗        ✗       ✓
A1 ORB               ✓✓    ✓      ✓✓       ✓✓       ✗       ✓
A2 VWAP_MOMO         ✓✓    ✗      ✓        ✓        ✗       ✓
A3 GAP_AND_GO        ✓✓    ✓      ✗        ✓✓       ✗       ✓
A8 VWAP_MACD         ✓✓    ✗      ✓        ✓        ✗       ✓
A9 OPENING_DRIVE     ✓✓    ✓      ✓✓       ✓✓       ✗       ✓
A10 EOD_IMBALANCE    ✓     ✓      ✓✓       ✓        ✗       ✓
A11 TWAP_TREND       ✓✓    ✗      ✓        ✓        ✗       ✓
A13 AH_EARNINGS      ✓✓    ✓      ✓        ✓✓       ✗       ✓
EQ-03 MEAN_REV       ✓     ✓      ✓✓       ✓✓       ✗       ✓✓
B6 CONNORS_RSI       ✓     ✓✓     ✓✓       ✓        ✗       ✓✓
B7 STDDEV_CHANNEL    ✗     ✓      ✓✓       ✓✓       ✗       ✓
B8 POC_REVERSION     ✓     ✓      ✓✓       ✓        ✗       ✓
B9 AH_LIQUIDITY_FADE ✓     ✓      ✓✓       ✓✓       ✗       ✓
EQ-02 STAT_ARB       ✓     ✓✓     ✓✓       ✓        ✓       ✓✓
E7 INDEX_REBAL_ARB   ✓✓    ✓      ✓✓       ✓        ✗       ✓
E8 ETF_DISPERSION    ✓     ✓      ✓✓       ✓        ✗       ✓
E9 KALMAN_PRICE      ✓     ✓✓     ✓✓       ✓        ✗       ✓✓
E10 OVERNIGHT_ARB    ✓     ✓      ✓✓       ✓        ✗       ✓
D1 CONGRESS_COPY     ✓✓    ✗      ✓        ✗        ✗       ✓
D2 INSIDER_CLUSTER   ✓✓    ✗      ✓        ✗        ✗       ✓
D9 CSUITE_CONVICTION ✓✓    ✗      ✓        ✗        ✗       ✓
D10 DARK_POOL_PRINT  ✓     ✓      ✓✓       ✓✓       ✗       ✓
D11 SLM_NEWSFLASH    ✓     ✓      ✓        ✓        ✗       ✓
F7 YIELD_CURVE_INV   ✗     ✓✓     ✓        ✓        ✓✓      ✓
F8 ENERGY_INVENTORY  ✓     ✓      ✓✓       ✓        ✗       ✓
F10 GLOBAL_HANDOFF   ✓✓    ✗      ✓        ✓        ✗       ✓
CM-01 SWEEP          ✓✓    ✓✓     ✓✓       ✓✓       ✓✓      ✓✓
CM-05 MARGIN_MIN     ✓✓    ✓✓     ✓✓       ✓✓       ✓✓      ✓✓
G1 LEVERAGED_ETF     ✓✓    ✗      ✗        ✗        ✗       ✗
G2 GAMMA_SQUEEZE     ✓✓    ✗      ✗        ✓✓       ✗       ✗
G4 SHORT_VOL_CARRY   ✓     ✓      ✓✓       ✓        ✗       ✓
VX-01 VIX_TERM_STRUCT✓     ✓      ✓✓       ✓        ✗       ✓
AL-01 REIT_CAPTURE   ✓     ✓      ✓✓       ✓        ✗       ✓✓
AL-02 SPAC_NAV_ARB   ✓     ✓✓     ✓✓       ✓        ✓       ✓✓

Legend: ✓✓ = strongly favoured  ✓ = compatible  ✗ = disabled in this regime
```

---

## 8. RISK MANAGEMENT & COMPLIANCE ENGINE

The `RiskManager` runs a strict 15-step pipeline on every proposed order. Any failed check immediately blocks the order, logs a row to `compliance_audit_log`, and returns `RiskCheckResult(passed=False, reason=..., rule=...)` to the caller. The pipeline is **never bypassed** — not in shadow mode (which simply reroutes to MockBroker after step 2), not during recovery, not during opportunity surge.

---

### 8.1 Pre-Trade Risk Pipeline (15 Steps)

**Step 1 — System Halt Guard:**
Blocks if `control_flags["trading_enabled"] == "false"`. Also blocks if `engine_status` is `HARD_HALT` or `EMERGENCY_HALT`. In `SOFT_HALT` state, allows the order through but halves the requested quantity (applied here, not in sizing).

**Step 2 — Shadow Mode Router:**
If `shadow_mode == "true"`, overrides the broker field to `MockBroker` and continues. All other checks still run normally in shadow mode (for accurate compliance testing).

**Step 3 — Emergency Halt Guard:**
Reads `DailyPnLManager.current_state`. If state is `EMERGENCY_HALT`: blocks ALL new entries. Allows only reducing orders (sells of long positions, buys of short positions) and options expiry management. If state is `HARD_HALT`: same restriction plus sends a notification that halt must be manually resumed.

**Step 4 — Intraday Drawdown Check:**
`intraday_drawdown = (starting_capital - current_equity) / starting_capital`. If > `intraday_drawdown_soft_pct (2%)`: blocks new entries (no reduction in sizing — just no new opens). If > `intraday_drawdown_hard_pct (4%)`: blocks new entries AND queues a liquidation sweep for all intraday-tagged positions (hold_type == "INTRADAY"). ATH-based drawdown (CM-11) is the rolling version; this step handles intraday.

**Step 5 — PDT Rule (FINRA Rule 4210):**
Counts all FILLED trades where `hold_time < 1 calendar day` within the last 5 rolling calendar days. Blocks the trade if this count would reach 4 AND `total_equity < PDT_EQUITY_BUFFER ($26,500)`. On block: logs `PDT_WOULD_TRIGGER` alert with today's count, the 5-day window used, and the equity gap to the $25,000 threshold. Strategy-level PDT tracking: marks each strategy as `pdt_risky` if it typically produces < 1-day holds; these strategies are automatically disabled when PDT count is at 3.

**Step 6 — Wash-Sale (IRC §1091):**
For BUY orders: checks `wash_sale_blacklist` for the exact symbol (and any substantially identical securities in `proxy_swap_map.json`). Blocks if an unexpired wash-sale entry exists. For SELL orders that would realize a loss: checks if a replacement purchase within 30 days (before or after) exists. If so, triggers the proxy swap logic: scores available proxies by `proxy_score` and offers the highest-scoring proxy (score > 0.80 required; else holds cash). Logs the full decision chain to `tax_optimization_decisions`.

**Step 7 — Position Concentration:**
`proposed_exposure = order_value / total_equity`. If > `MAX_SINGLE_POSITION_PCT (10%)`: automatically resizes the order down to 10% of equity. Does not block — resizes. Logs the resize with original and adjusted quantities. For leveraged strategies (Group G): applies a tighter cap of `MAX_SINGLE_POSITION_PCT_LEVERAGED (5%)`.

**Step 8 — Sector Concentration:**
Looks up the symbol's GICS sector via Polygon symbol details (cached in `feature_store`). Calculates `current_sector_exposure + order_value`. If the total would exceed `MAX_SECTOR_PCT (35%)`: blocks. Logs current sector distribution. Exception: Cash Management and Hedging strategies (CM-*, EQ-04, EQ-05) are exempt from sector concentration limits.

**Step 9 — Liquidity Filter:**
`order_impact = (order_qty × fill_price) / avg_daily_volume_usd_20d`. Blocks if > 5% (would represent too large a fraction of daily volume). For intraday strategies that target thin periods (A11 T-WAP, A13 After-Hours): uses the session-specific average volume (e.g., AH session ADTV), not the full-day figure.

**Step 10 — Portfolio Correlation Check:**
Loads the `strategy_correlation_matrix` from Redis (or computes from `positions` table if cache miss). Calculates the 60-day Pearson correlation between the proposed symbol and all existing holdings. `WARN` if any existing position has correlation > 0.75. `BLOCK` if correlation > 0.90 (near-identical exposure, no diversification benefit). Correlation block can be overridden per-order from the UI with a manual confirmation (logged).

**Step 11 — Asset Class Toggle Check:**
Checks the relevant `control_flags` per asset class. Blocks CRYPTO if `crypto_enabled == "false"`. Blocks OPTION if `options_enabled == "false"`. Blocks LEVERAGED (Group G) if `leveraged_strategies_enabled == "false"`. Blocks after-hours orders (A13, B9) if `after_hours_strategies_enabled == "false"`.

**Step 12 — Leverage (Reg-T):**
Calculates `total_notional / total_equity`. Blocks if > `MAX_LEVERAGE_OVERNIGHT (2.0×)` for overnight hold orders. Allows up to `MAX_LEVERAGE_INTRADAY (4.0×)` for orders tagged as `hold_type = "INTRADAY"`, consistent with Regulation T daytime trading margin rules. Options premium is included at full notional (not delta-adjusted) for conservatism.

**Step 13 — Flash Crash Correlation Spike (NEW):**
Calculates the rolling 1-hour pairwise correlation across all open positions using 1-minute bar data (from Redis tick cache or StateCacheManager). If the average correlation spikes above 0.85 (all positions moving together = hidden systemic risk), blocks any new long entries regardless of strategy. This condition triggers: `alert_manager.fire("CORRELATION_SPIKE", severity="CRITICAL")`. Resolution: close 2 most correlated positions before resuming new entries.

**Step 14 — Liquidity Dry-Up Guard (NEW):**
Monitors the bid-ask spread as a proxy for liquidity. For each order: fetches the current bid-ask spread and compares to the 20-day average spread for that symbol. If `current_spread > 5 × avg_spread` (liquidity drought — wide spread signals thin market): blocks the order to prevent excessive slippage. Common during circuit breakers, news halts, and overnight. Logs `LIQUIDITY_DRY_UP` with current vs average spread.

**Step 15 — Strategy Drawdown Halt (NEW):**
Tracks per-strategy drawdown independently of the portfolio-level halt. `strategy_drawdown = (strategy_peak_equity - strategy_current_equity) / strategy_peak_equity` where equity is the running P&L for that strategy. If any single strategy's drawdown exceeds `MAX_STRATEGY_DRAWDOWN (25%)` on its rolling 30-day capital allocation: that strategy is automatically set to `DISABLED_ERROR` status with `error_message = "Auto-halted: exceeded 25% strategy drawdown"`. The rest of the portfolio continues normally. Strategy auto-re-enables on the next Saturday `weekend_review` after a full review.

---

### 8.2 Real-Time & Post-Trade Risk Controls

**ATR Trailing Stops (every 5 minutes during market hours):**
`stop = max(prior_stop, current_close - ATR_MULTIPLIER × ATR(14))`.
ATR multipliers by regime: BULL_TREND = 2.5×, SIDEWAYS = 2.0×, BEAR_TREND = 1.5×, CRASH_RISK = 1.0× (very tight).
After-hours positions (A13, B9): fixed 3% stop from entry, not ATR-based (too volatile for ATR in thin markets).

**Profit-Lock Ratchet:**
Position at +15% unrealized: stop ratchets to break-even + 5%.
At +25%: stop ratchets to +15%.
At +40%: stop at +30%.
At +60%: stop at +45%.
Each ratchet is a one-way move — the stop never moves backward.

**Portfolio Greeks Limits (every 5 minutes during market hours):**
`greeks_monitor.py` recalculates net portfolio Delta, Gamma, Theta, Vega every 5 minutes.
Default limits (configurable in Settings tab):

| Greek | Soft Warn | Hard Block |
|---|---|---|
| Net Delta | ±0.20 × NAV | ±0.30 × NAV |
| Net Gamma | 0.015 × NAV | 0.025 × NAV |
| Net Theta | −$200/day | −$300/day |
| Net Vega | ±$500/1% IV move | ±$800/1% IV move |

On WARN: sends UI notification. On BLOCK: blocks all NEW options orders until Greek is back within limits. Portfolio snapshots in `greeks_snapshots` table every hour.

**Margin Utilization Optimizer (every 30 minutes):**
`margin_optimizer.py` ranks all leveraged positions by `(expected_pnl × win_probability) / margin_requirement`. Positions with `rank_score < 0.25` (poor risk-adjusted margin efficiency) are flagged. If `margin_used / margin_available > 0.85 (WARN)`: generates alert + flags worst positions. If > 0.90 (BLOCK): immediately closes the 2 worst-ranked positions to restore margin headroom.

**Reg SHO Short Locate:**
Short-sale locate verification via prime broker API before any short entry. If locate unavailable: blocks short, queues for retry in 5 minutes (locate may free up). Logs all locate attempts.

**MiFID II Best Execution Logging:**
All venue quotes considered before routing are saved to `orders.venue_quotes_json`. Retained 5 years (configurable). Required for regulatory compliance for EU-accessible brokers.

---

### 8.3 Regulatory Compliance Matrix

| Regulation | Rule | AQTA Implementation |
|---|---|---|
| **FINRA Rule 4210 (PDT)** | < 4 day trades in 5 days if equity < $25k | Step 5 pipeline check; strategy PDT flags; alert at count=3 |
| **IRC §1091 (Wash-Sale)** | No loss deduction if substantially identical security bought within 30 days | Step 6; proxy swap scoring; TLH engine; `wash_sale_blacklist` |
| **Reg T (Margin)** | 50% initial margin overnight; 25% maintenance | Step 12; `MAX_LEVERAGE_OVERNIGHT = 2.0×` |
| **SEC Rule 201 (Short Sale Circuit Breaker)** | No short sales at or below NBB if stock down > 10% on day | Pre-short check in Reg SHO locate + intraday price filter |
| **FINRA Rule 5320 (Front-Running)** | Cannot trade ahead of customer orders | N/A (retail only; documented) |
| **MiFID II (Best Execution)** | Document best execution for each order | `orders.venue_quotes_json` saved per order |
| **IRS §1256 (Section 1256 Contracts)** | 60/40 LTCG/STCG split for futures/options | `tax_lots.asset_class` = "SECTION_1256"; separate lot selection |
| **IRS §1092 (Straddle Rules)** | Cannot harvest losses on straddle legs in same tax year | Straddle detection in `tax_engine.py`; paired positions flagged |
| **CFTC Position Limits** | Speculative position limits in regulated futures | N/A (ETF proxies used; no direct futures trading) |
| **Pattern Day Trader Rule** | $25,000 minimum equity for PDT accounts | Step 5; PDT_EQUITY_BUFFER = $26,500 |
| **Regulation SHO (Short Sales)** | Locate requirement before shorting | `compliance.py:verify_short_locate()` before every short |

---

## 9. TAX OPTIMIZATION ENGINE

### 9.1 Tax Lot Management — 4 Methods

AQTA tracks all open lots in the `tax_lots` table. The `TaxAwarePortfolioManager` selects the optimal method per sale:

- **FIFO (First In, First Out):** Default IRS method. Used when other methods offer no advantage or when avoiding wash-sale complications with many lots.
- **HIFO (Highest Cost First):** Minimizes realized gain by selling the most expensive lots first. Used when all lots are short-term (no LTCG benefit possible).
- **LTCG_FIRST:** Sells lots held > 365 days first to classify gains at the lower 0%/15%/20% long-term rate. Used when the account has a mix of short-term and long-term lots and the gain is unavoidable.
- **LOSS_FIRST (Tax-Loss Harvesting):** Sells lots with unrealized losses first to generate tax offsets. Used proactively when losses exceed `TLH_MIN_LOSS_THRESHOLD`.

**AMT Impact Assessor (NEW):** Before selecting HIFO or LOSS_FIRST, checks whether the trader is projected to owe AMT (Alternative Minimum Tax). If AMTI projection exceeds AMT exemption phase-out threshold: HIFO is avoided to prevent accelerating AMT preference items. ISO exercise gains are flagged separately.

**Selection Logic:**
```python
def select_lot_method(symbol, side, portfolio_state, tax_config) -> LotMethod:
    lots = get_open_lots(symbol)
    ltcg_lots = [l for l in lots if l.hold_days >= 365]
    loss_lots  = [l for l in lots if l.unrealized_pnl < TLH_THRESHOLD]

    if tax_config.amt_exposure_projected:
        return LotMethod.FIFO           # Avoid accelerating AMT items

    if loss_lots and tax_config.tlh_enabled:
        opportunity_cost = estimate_30d_opportunity_cost(symbol)
        tax_saving = abs(sum(l.unrealized_pnl for l in loss_lots)) * tax_config.marginal_rate
        if tax_saving > opportunity_cost * 1.2:
            return LotMethod.LOSS_FIRST

    if ltcg_lots and portfolio_state.stcg_ytd > 0:
        return LotMethod.LTCG_FIRST

    if portfolio_state.marginal_rate > 0.30:
        return LotMethod.HIFO

    return LotMethod.FIFO
```

---

### 9.2 Proxy Intelligence Scoring

When a loss harvest triggers a wash-sale waiting period (31 days), AQTA uses the `proxy_swap_map.json` to find a suitable replacement that maintains similar market exposure without triggering §1091.

**Proxy Score Formula:**
```
proxy_score = (
  0.40 × price_correlation_60d(sold, candidate) +
  0.20 × (1 if sector_match else 0) +
  0.20 × (1 - abs(beta_sold - beta_candidate) / beta_sold) +
  0.20 × min(candidate_adtv / sold_adtv, 1.0)
)
```

- `proxy_score ≥ 0.80`: Excellent substitute. Execute swap immediately.
- `0.60 ≤ score < 0.80`: Acceptable substitute. Flag for user review in Tax Dashboard.
- `score < 0.60`: Poor substitute. Hold cash for 31 days instead of deploying to a weak proxy.

**Built-in Proxy Map Examples:**

| Sold | Best Proxy | Score | Notes |
|---|---|---|---|
| SPY | IVV or VOO | 0.99 | Nearly identical; different issuer |
| QQQ | ONEQ or QQQM | 0.98 | Same NASDAQ-100; different share class |
| IWM | VTWO or CALF | 0.92 | Russell 2000 equivalents |
| GLD | IAU or SGOL | 0.97 | Same gold exposure; different custodian |
| AAPL | QQQ (partial) | 0.72 | Tech sector proxy only |
| XLF | VFH or KBE | 0.85 | Financial sector ETFs |

---

### 9.3 Tax-Loss Harvesting (TLH) Engine

**Scan Frequency:** Every trading day in `after_hours_routine` (16:15 ET). Enhanced December scan: every trading day in December.

**Trigger Thresholds:**
- January–November: `TLH_MIN_LOSS_THRESHOLD = −$500` (configurable).
- December: `TLH_MIN_LOSS_THRESHOLD_DECEMBER = −$300` (more aggressive year-end harvesting).

**Opportunity Cost Check (before executing TLH):**
```python
opportunity_cost_30d = symbol_annual_return / 12 × position_value
tax_saving = abs(unrealized_loss) × marginal_rate
if tax_saving > opportunity_cost_30d × 1.2:
    execute_harvest()   # Net positive: harvest
else:
    defer_harvest()     # Not worth the cost of being out of position
```

**Gain Deferral Optimizer (positions aged 335–365 days):**
For each position in the 335–365-day window with significant unrealized gains:
1. Calculate gain if sold today (STCG tax).
2. Calculate gain if deferred past day 365 (LTCG tax). Saving = `gain × (stcg_rate - ltcg_rate)`.
3. Hedge cost for the deferral period: evaluate 3 approaches:
   - Hold unhedged (no cost; full market risk).
   - Buy protective put (cost = put premium; full upside preserved).
   - Write covered call (income − upside cap).
4. Select approach with highest after-tax expected value. Log decision to `tax_optimization_decisions`.
5. Alerts UI (Tab 7) for user awareness of each decision.

---

### 9.4 Estimated Tax Payment Planner

**Quarterly Payment Calendar:**

| Quarter | Period | Due Date |
|---|---|---|
| Q1 | Jan 1 – Mar 31 | April 15 |
| Q2 | Apr 1 – May 31 | June 15 |
| Q3 | Jun 1 – Aug 31 | September 15 |
| Q4 | Sep 1 – Dec 31 | January 15 (next year) |

**Projection Method:**
- YTD Realized: Sum all `tax_lots` closed this year → STCG, LTCG, dividends, ordinary income.
- Forward Projection: For each open position, estimate `expected_close_gain = unrealized_pnl × win_probability` (from Thompson Sampling stats).
- Safe Harbor: `max(100% of prior year total tax, 90% of current year projected total tax)`.
- State Tax: Calculated separately using `state_tax_rate` from `settings.toml`.

**Alerts:** 10-day advance warning to Notification Center before each due date. Tax dashboard (Tab 7) shows a "PAYMENT DUE SOON" banner with the calculated amount and payment method instructions.

---

### 9.5 IRS Form 8949 & Year-End Reporting

- **Form 8949 (CSV):** IRS-compatible export. Columns: Description, Date Acquired, Date Sold, Proceeds, Cost, Adjustment Code, Adjustment Amount, Gain/Loss. Grouped by: Box A (Short-term, reported on 1099-B), Box B (Short-term, not on 1099-B), Box D (Long-term, on 1099-B).
- **Form 8949 (PDF):** Auto-formatted PDF ready for printing/mailing. Generated on demand or auto-generated December 31.
- **Year-End Report (HTML + PDF):** Full YTD PnL by strategy and asset class; tax alpha vs FIFO baseline; harvested losses total; highest-gain and highest-loss strategies; upcoming Q4 estimated payment summary. Exported to `data_cache/reports/year_end_{year}.html`.
- **Section 1256 Contracts:** `tax_lots` where `asset_class = "SECTION_1256"` (futures ETFs: VXX, UVXY, USO, UNG in some structures) are marked-to-market at year-end and split 60% LTCG / 40% STCG regardless of actual hold period, per IRS §1256.
- **Straddle Detection (IRS §1092):** The tax engine scans `options_positions` for offsetting put/call pairs on the same underlying opened within 30 days of each other. Flags these as straddles; defers loss recognition on the loss leg until the gain leg is also closed.
- **December Aggressive Mode:** For the entire month of December, `TaxEngine.december_mode = True`. This activates: lower TLH threshold ($300), more aggressive gain deferral analysis, and a weekly "Year-End Tax Review" report with the estimated tax cost of not harvesting each remaining loss position.

---

## 10. DAILY CYCLE & TASK SCHEDULING — 16 STEPS

Orchestrated by APScheduler 3.10.4 (`AsyncIOScheduler`, `America/New_York` timezone). Dual settlement design: **Preliminary at 15:55 ET** closes the regular session; **Final at 20:00 ET** captures after-hours P&L before overnight reporting.

### 10.1 Parameter-Driven Main Cycle

```toml
# config/settings.toml — [scheduler] section
main_cycle_interval_minutes = 5   # Valid: 1–10 integer. Hot-reloadable from UI.
# At runtime: MAIN_CYCLE_INTERVAL_MINUTES = max(1, min(10, int(value)))
# UI validation: slider 1–10, integer steps only, labeled 1 / 2 / 5 / 10 mins.
# Intraday micro-cycle is ALWAYS 1 minute; this parameter only affects the
# main strategy evaluation cycle (Step 8 below).
```

APScheduler job for the main cycle is registered with `minutes=MAIN_CYCLE_INTERVAL_MINUTES` at startup. When the UI changes the parameter (via `POST /control/flag`):
1. `config.py` validates the new value is an integer in [1, 10].
2. Reschedules the APScheduler job with the new interval (no restart required).
3. Logs the change to `compliance_audit_log` with old/new interval and the operator identity.

---

### 10.2 The Complete 24-Hour Schedule

**Step 1 — `overnight_data_refresh` (02:00 ET, Mon–Fri)**
- Downloads updated SEC filings (Form 4, 13F amendments, 8-K) via `sec-edgar-downloader`.
- Refreshes FRED macro data (DGS2, DGS10, DGS30, FEDFUNDS, CPIAUCSL, UNRATE, GDP, UMCSENT).
- Refreshes `supply_chain_graph.json` from latest SEC EDGAR relationships data.
- Runs incremental LightGBM regime classifier update (`online_learner.py`) on prior day's closed trades.
- Syncs SQLite → DuckDB analytics ETL (`analytics_db.py:sync_to_duckdb()`).
- Backs up SQLite DB to `data_cache/backups/trading_{date}.db` (7-zip compressed, 30-day retention).
- Backs up DuckDB checkpoint to Parquet in `data_cache/backups/analytics_{date}/`.
- Updates `short_interest_data` table from StockAnalysis.com scrape (weekly data, Mon only).
- Updates `cot_positions` table from CFTC COT report (weekly release, Mon only).
- Updates `spac_universe` from SEC EDGAR S-1 filings (Mon only, for AL-02 strategy).

**Step 2 — `pre_market_warmup` (04:00 ET, Mon–Fri)**
- Sets `engine_status = "PRE_MARKET"`.
- Resets daily `target_override_usd` and `target_override_pct` to empty strings.
- Refreshes all OAuth tokens (Schwab, Robinhood, IBKR, Alpaca). Verifies broker balances and margin status.
- Runs `StrategyLoader.health_check_all()` — concurrent health checks on all 160+ strategies.
- Starts `NLPEngine` in Tier 2 SLM mode (FinBERT ONNX warm-up pass on dummy text to pre-load model weights into memory).
- Fetches FRED macro data snapshot for the day.
- Fetches economic calendar from `economic_events` table; builds today's event timeline.
- Runs `OpportunityScanner.run_premarket_scan()` — universe filter (ADTV, price range) and Tier 1 composite scoring.
- Runs FinBERT processing on overnight news headlines (batch, last 6 hours of NewsAPI articles).
- If `llm_mode == "LOCAL"` or `llm_mode == "CLOUD"`: runs LLMAnalyst on top 10 overnight items.
- Calculates seasonality scores for all active symbols (B9 strategy data).
- Pre-computes intraday VWAP anchor start prices for all watchlist symbols.
- Generates pre-market briefing event → WebSocket broadcast → Notification Center.

**Step 3 — `early_pre_market` (07:00 ET, Mon–Fri)**
- Scans for pre-market gap candidates (A10/A12 strategies): stocks gapping > 5%, volume > 100k, NLP score check.
- Fetches options chain updates for positions expiring within 5 days (Greeks refresh).
- Updates `short_interest_data` if Tuesday (FINRA publishes twice-monthly; mid-month update).
- Recalculates `options_sentiment_score` (put/call ratio + 25-delta skew + UOA direction) for full universe.
- Refreshes Reddit/StockTwits cashtag velocity scores (D4, D8 strategy inputs).
- Fetches pre-market quotes for all top-20 scanner candidates via Robinhood/Alpaca.
- Runs F10 Global Session Handoff pre-check: fetches Nikkei 225, FTSE 100, DAX session returns.
- Applies F10 `global_bullish_multiplier` (or reduction) to opening-hour strategy config.

**Step 4 — `macro_event_prep` (08:15 ET, Mon–Fri)**
- Checks `economic_events` for same-day releases: NFP (1st Fri), CPI/PPI, ISM, FOMC, earnings (from `economic_events.event_type`).
- For any TIER-1 macro release today (NFP, CPI, FOMC): reduces all open swing position sizes by 50% via `pre_event_size_reduction()`. Generates `PRE_MACRO_REDUCE` alert.
- Queues macro strategy signals: F3 (FOMC, if applicable), F4 (CPI/PPI), F8 (NFP), F18 (Housing).
- Fetches EIA energy inventory consensus estimate if Wednesday (for F8 enhancement via CO-01).
- Sends morning briefing via all enabled notification channels:
  ```
  Morning Briefing [date]:
  ─ Regime: BULL_TREND (HMM 71%, LGB 68%, agreement: HIGH)
  ─ Overnight: SPY flat, BTC -1.2%, Gold +0.4%
  ─ Events: CPI at 08:30 (consensus: +0.3%), FOMC minutes at 14:00
  ─ Pre-market leaders: NVDA +4.2% (earnings beat), TSLA -2.1%
  ─ Top 3 setups: A3 NVDA (score 87), A9 MSFT (score 74), B3 AAPL (score 71)
  ─ Capital state: NORMAL ($10,240 equity). Targets: Min=$154 / Ideal=$307 / Stretch=$512
  ```

**Step 5 — `market_open_prep` (09:28 ET, Mon–Fri)**
- Sets `engine_status = "MARKET_HOURS"`.
- Calls `DailyPnLManager.initialize_day()`:
  - Fetches live broker equity as `STARTING_CAPITAL_TODAY`.
  - Resolves `DailyTargetConfig` (override check → dynamic % calc, as described in §1.1.2).
  - Stores resolved targets in `daily_cycle_log`.
  - Broadcasts `daily_targets_set` WebSocket event with all resolved values.
- Places EQ-04 Flash Crash limit orders (5 GTC orders for SPY/QQQ at −5%, −8%, −12%, −16%, −20%).
- Sets OCO (One-Cancels-Other) bracket orders on ALL swing positions (entry stop + take-profit).
- Saves opening `portfolio_snapshots` row.
- Clears expired signals from `signals_queue` (older than 30 min for INTRADAY; 2 days for SWING).
- Updates `volatility_target_scalar` (CM-05 vol-target overlay) using prior 20-day realized vol.
- Runs `StateCacheManager.restore_from_sqlite()` to reload overnight Redis-flushed state.
- Starts `NLPEngine` real-time news stream subscription.

**Step 6 — `regular_market_open` (09:30–09:45 ET)**
A dedicated short window for opening-specific strategies only. Runs once at 09:30 ET.
- Executes A9 (Opening Drive Momentum): evaluates first-minute volume.
- Executes A1 (ORB): starts recording 9:30–9:45 opening range.
- Finalizes A3 (Gap-and-Go) entry signals queued from A10/A12 pre-market scan.
- Broadcasts `market_open` WebSocket event to all connected UI clients.

**Step 7 — `intraday_micro_cycle` (09:30–20:00 ET, every 1 minute)**
Always runs every 60 seconds regardless of `main_cycle_interval_minutes`. Handles only the fastest-responding strategies:
- A8 (VWAP MACD 1-min): evaluates 1-min MACD vs VWAP.
- A11 (T-WAP Trend): checks T-WAP deviation + NYSE tick index.
- A13 (After-Hours, 16:00–20:00): monitors AH price action.
- B8 (POC Reversion): updates POC from 30-min rolling volume profile.
- B9 (AH Liquidity Fade, 16:00–20:00): monitors AH price spikes.
- CM-09 (Delta-Neutral): checks net portfolio delta vs threshold; fires delta hedge if needed.
- CM-03 (Beta Hedge): checks portfolio beta vs target; resizes if outside band.
- D11 (SLM News Flash): checks news queue for new real-time headlines; SNIPER orders.
- Updates `bid_ask_imbalance` and `aggressor_ratio` from L2 feed (if `level2_enabled`).

**Step 8 — `main_trading_cycle` (09:35–15:55 ET, every `MAIN_CYCLE_INTERVAL_MINUTES`)**
The primary strategy evaluation loop.
- Checks `trading_enabled` flag.
- Calculates full `portfolio_state`: equity, cash, positions_value, pnl, drawdown, Greeks, beta.
- Runs `OpportunityScanner.run_full_scan()`: full Tier-2 composite scoring on universe.
- Updates regime probabilities (HMM + LightGBM ensemble), refreshes Thompson Sampling weights.
- For each enabled strategy (in Thompson Sampling priority order):
  - Fetches multi-timeframe data for its watchlist symbols.
  - Calculates indicators.
  - Applies Kalman filter smoothing to raw signal strengths.
  - Calls `generate_signals()` → returns `list[SignalEvent]`.
  - For signals with Kalman-smoothed strength > 0.35: passes to `RiskManager.run_pipeline()`.
  - Approved orders → `ExecutionEngine.route()` → `SmartOrderRouter`.
- Runs `SignalAggregator.dedup()`: merges redundant signals on same symbol+direction.
- Calls `update_positions_prices()`: refreshes all position last_prices; checks stops and TPs.
- Calls `DailyPnLManager.lock_in_profits()`: updates profit-lock floor if new high reached.
- Broadcasts `portfolio_tick` WebSocket event with full current state (every cycle).
- Checks `OPPORTUNITY_SURGE` condition: if ≥5 HIGH-conviction signals this cycle, fires `OPPORTUNITY_SURGE` state transition.

**Step 9 — `options_management` (11:00 ET and 15:00 ET)**
Runs twice daily — at market midpoint and pre-close.
- 11:00 ET: Rolls any positions at 21 DTE that meet roll criteria (sufficient credit received for roll).
- 11:00 ET: Adjusts delta hedges for VX-02 (Short Gamma Scalping) if delta has drifted.
- 15:00 ET: Closes all 0DTE options at MARKET (any remaining 0DTE).
- 15:00 ET: Closes any options at 50% profit (standard BTC rule).
- 15:00 ET: Closes any options at 200% loss (hard stop).
- Calculates and saves end-of-afternoon portfolio Greeks snapshot to `greeks_snapshots`.

**Step 10 — `moc_imbalance_scan` (15:40–15:50 ET, every 2 minutes)**
- Fetches NYSE MOC imbalance data (Polygon or IBKR feed, when available).
- If net BUY imbalance > $500M for any stock: queues A10 (EOD Imbalance Fade) short signal.
- If net SELL imbalance > $500M: queues A10 long signal.
- All A10 orders marked for MOC execution (fill at the 16:00 ET closing price).

**Step 11 — `power_hour_scan` (15:30 ET)**
- Activates A9 power hour window: re-checks volume and intraday highs for power-hour breakouts.
- Reviews all open positions for EOD exit decisions: any intraday-tagged position not yet closed.
- Flags intraday positions for 15:55 ET liquidation if they haven't hit their target.

**Step 12 — `preliminary_settlement` (15:55 ET, Mon–Fri)** ← REGULAR SESSION CLOSE
- Sets `session = "REGULAR_SESSION_CLOSE"`.
- Cancels EQ-04 Flash Crash orders if not triggered.
- Liquidates ALL positions tagged `hold_type = "INTRADAY"` via MARKET orders.
- Calls `DailyPnLManager.settle_regular_session()`:
  - Calculates `preliminary_pnl` = current equity − starting_capital.
  - Checks preliminary_pnl vs soft/hard/emergency halt thresholds.
  - Updates capital state machine (NORMAL → RECOVERY, NORMAL → COMPOUNDING, etc.).
  - Stores `preliminary_pnl` and `settlement_timestamp_preliminary` in `daily_cycle_log`.
  - Logs `PRELIMINARY_SETTLEMENT` event to all notification channels.
  - Broadcasts `settlement_preliminary` WebSocket event.
- DOES NOT finalize profit_wallet or trigger profit sweep (deferred to Step 16 Final Settlement).
- All swing and after-hours positions remain open.

**Step 13 — `after_hours_transition` (16:01 ET, Mon–Fri)**
- Sets `engine_status = "AFTER_HOURS"`.
- If `after_hours_strategies_enabled = true`: begins monitoring A13, B9, E10 strategies.
- Starts CM-01 money market sweep evaluation (runs at 16:15 ET).
- Begins post-market earnings processing: fetches any 16:01+ earnings releases via Finnhub/AlphaVantage.
- Feeds earnings results to NLPEngine for A13 signal generation.

**Step 14 — `after_hours_routine` (16:15 ET, Mon–Fri)**
- Runs CM-01 (Money Market Sweep): if cash > $1,500, buys highest-yielding money market fund.
- Updates ATR trailing stops for ALL swing positions (using regular-session close prices).
- Runs `TaxAwarePortfolioManager.evaluate_all_positions()`:
  - TLH scan on all positions with unrealized losses.
  - Gain deferral analysis for 335–365-day positions.
  - Wash-sale blacklist expiry cleanup.
- Calculates EOD VaR (Monte Carlo, 10,000 paths) and stress tests; stores in `portfolio_snapshots`.
- Runs CM-10 (Maximum Diversification Rebalancer) check — flags for Saturday execution.
- Updates `strategy_correlation_matrix` daily row in both SQLite and Redis.
- Runs CM-12 (Margin Utilization Optimizer): if margin > 85%, flags positions for early close.

**Step 15 — `margin_minimizer` (19:30 ET, Mon–Fri)**
- Runs CM-05 (Margin Interest Minimizer): closes any remaining margin-using positions to achieve a flat or cash-positive overnight balance, avoiding broker margin interest.
- Verifies after-hours positions are within risk limits.
- Final options check: any options positions with < 2 DTE that should not be held overnight.

**Step 16 — `final_settlement` (20:00 ET, Mon–Fri)** ← AFTER-HOURS SESSION CLOSE
- Sets `session = "FINAL_SETTLEMENT"`.
- Calls `DailyPnLManager.settle_final()`:
  - Fetches final equity (including all after-hours fills).
  - Calculates `after_hours_pnl = final_equity − preliminary_equity`.
  - Calculates `final_pnl = final_equity − starting_capital`.
  - Compares final_pnl vs targets: determines if day is WIN / LOSS / FLAT.
  - On WIN: updates compounding streak counter; updates profit_wallet; triggers profit sweep check.
  - On LOSS: activates RECOVERY_MODE; sets recovery_target; logs recovery session start.
  - Updates `daily_cycle_log` with all final values and both settlement timestamps.
  - Stores final `portfolio_snapshots` row.
  - Broadcasts `settlement_final` WebSocket event with full PnL breakdown.
  - Sends final daily summary to all notification channels:
    ```
    ✅ Daily Report [date] — FINAL SETTLEMENT
    ─ Starting Capital:   $10,240.00
    ─ Regular PnL:        +$287.50  (+2.81%)
    ─ After-Hours PnL:    +$24.10   (+0.24%)
    ─ FINAL PnL:          +$311.60  (+3.04%)  ← IDEAL TARGET MET ✓
    ─ Capital State:      NORMAL → COMPOUNDING (Day 3/5)
    ─ Profit Wallet:      $2,847.50 (↑ from $2,535.90)
    ─ Strategies Fired:   14 entries, 11 exits, 3 still open
    ─ Win Rate Today:     11/14 = 78.6%
    ```

**Step 17 — `crypto_cycle` (17:00–09:00 ET, every 15 minutes)**
- If `crypto_enabled = true`: runs CR-01 (trend), CR-06 (fear/greed), CR-07 (DeFi yield), G3 (momentum burst).
- Monitors BTC/ETH funding rates (CR-03); logs to `funding_rate_log`.
- Checks Glassnode on-chain metrics (CR-04).
- Updates `crypto_positions` table with current on-chain holdings.

**Step 18 — `nightly_maintenance` (23:55 ET, Mon–Fri)**
- Generates daily performance HTML report → `data_cache/reports/daily_{date}.html`.
- Sends report path to Notification Center; broadcasts `daily_report_ready` WebSocket event.
- Optuna hyperparameter tuning: if last tuning > 7 days old, tunes top 5 strategies by Sharpe on last 90 days of data.
- HMM full retrain: if > 7 days since last retrain OR ensemble disagreement > 3 consecutive days.
- LightGBM incremental update: `online_learner.py` on prior day's closed trades.
- `StateCacheManager.flush_to_sqlite()`: persists all Redis cache to SQLite for overnight.
- Profit sweep alert: if `profit_wallet > PROFIT_SWEEP_THRESHOLD ($30,000)`.
- Verifies all broker connections (heartbeat check).
- Saves `greeks_snapshots` end-of-day row.
- Cleans up `signals_queue`: archives all expired signals to `alpha_signals_log`.

**Step 19 — `weekend_review` (Saturday 08:00 ET)**
- Full portfolio rebalance via CM-10 (Max Diversification) and portfolio_optimizer.
- Updates all `strategy_performance` metrics: win_rate, Sharpe, Sortino, max_drawdown, profit_factor, avg_hold_days, avg_entry_score.
- Clears expired `wash_sale_blacklist` entries.
- Clears `DISABLED_ERROR` strategies that have been down > 7 days — sends notification asking for manual review.
- Runs walk-forward validation on all active strategies (`backtest/walk_forward.py`). Stores OOS/IS comparison in `backtest_results`.
- Checks strategy drawdown: auto-enables any strategy that was auto-halted by Step 15 (strategy drawdown halt) and whose recent data looks clean. Logs decision.
- Generates weekly performance HTML report: PnL attribution by strategy/regime, tax efficiency summary, walk-forward OOS scores, upcoming week events.
- Sends weekly report to all notification channels.
- Re-runs `StrategyLoader.health_check_all()` and updates strategy status in `strategy_performance`.
- Updates `supply_chain_graph.json` from latest week's SEC filings.

**Always Running — `health_monitor` (every 60 seconds, 24/7)**
- Checks all broker circuit breaker states; fires alert if any broker is CIRCUIT_OPEN.
- Monitors SQLite write latency (WARN if > 100ms; CRITICAL if > 500ms).
- Monitors Redis availability; if Redis drops, switches `StateCacheManager` to asyncio fallback (silent to strategies).
- Checks APScheduler job health: CRITICAL alert if any scheduled step misses by > 2 minutes.
- Monitors NLP engine tier: if Tier 2 SLM fails, logs switch to Tier 3 and fires INFO alert.
- Verifies `engine_heartbeat` is updating in `control_flags`.
- If `prometheus_enabled = true`: updates all Prometheus gauge metrics.
- Monitors disk space: WARN if `data_cache/` > 50GB; auto-purge oldest Parquet feature files if > 80GB.

---

## 11. CONTROL UI & OBSERVABILITY

The UI is a 10-tab WebSocket-driven Single-Page Application served by FastAPI on port 8766. No build system. All JS in modular ES2022 with local vendored libraries. Keyboard shortcuts, dark theme, and real-time updates on all tabs.

---

### 11.1 Engine API — Complete Endpoint Reference

**System Control:**
`GET /health`, `GET /status`, `POST /control/flag` (hot-config any key), `POST /control/halt`, `POST /control/resume`, `POST /control/override` (temporary parameter), `POST /control/strategy/{id}/toggle`, `GET /control/flags/all`.

**Portfolio & Positions:**
`GET /portfolio`, `GET /positions`, `GET /positions/{symbol}`, `GET /trades`, `GET /trades/{id}`, `GET /orders`, `GET /signals/pending`, `GET /signals/history`.

**Analytics & Performance:**
`GET /analytics/pnl_attribution?period=7d`, `GET /analytics/drawdown_history`, `GET /analytics/factor_exposure`, `GET /analytics/correlation_matrix`, `GET /analytics/strategy_heatmap`, `GET /analytics/monthly_calendar`.

**Options:**
`GET /options/portfolio_greeks`, `GET /options/positions`, `GET /options/iv_surface/{symbol}`, `GET /options/flow/recent`.

**Scanner:**
`GET /scanner/live?limit=25`, `GET /scanner/darkpool`, `GET /scanner/insider_feed`, `GET /scanner/social_sentiment`.

**Backtest:**
`GET /backtest/results`, `POST /backtest/run` (async, returns `{job_id}`), `GET /backtest/status/{job_id}`, `GET /backtest/report/{run_id}`.

**Tax:**
`GET /tax/summary`, `GET /tax/lots`, `GET /tax/wash_sales`, `GET /tax/form8949/csv`, `GET /tax/form8949/pdf`, `GET /tax/estimated_payments`, `GET /tax/gain_deferral_candidates`, `GET /tax/year_end_report/{year}`.

**Notifications:**
`GET /notifications?unread=true`, `POST /notifications/dismiss/{id}`, `POST /notifications/dismiss/all`, `GET /notifications/history`.

**System & Reports:**
`GET /system/topology`, `GET /system/health_checks`, `GET /system/nlp_status`, `GET /system/scheduler/jobs`, `GET /performance/report/{date}`, `GET /performance/report/weekly/{date}`.

**WebSocket Events (`ws://localhost:8765/ws`):**
- `portfolio_tick` (every cycle): Full `portfolio_state` snapshot.
- `trade_executed` (immediate): Trade details + updated position.
- `signal_generated` (per signal): strategy, symbol, direction, strength, tier.
- `regime_change` (on transition): old/new regime, probabilities, ensemble agreement.
- `alert_fired` (immediate): ID, severity, message, action_taken.
- `halt_triggered` (immediate): Reason, equity at halt, positions affected.
- `daily_targets_set` (09:28 ET): Resolved DailyTargetConfig for the day.
- `settlement_preliminary` (15:55 ET): Regular session close summary.
- `settlement_final` (20:00 ET): Full day summary with AH PnL.
- `strategy_health_update` (on health_check): Strategy ID, new status, error/resolution.
- `nlp_tier_change` (on fallback): Old tier, new tier, reason.
- `daily_report_ready` (23:55 ET): Report file path.

---

### 11.2 Dashboard UI — 10 Tabs

**Design System:**
- Background `#0d1117`, surface `#161b22`, elevated `#1c2128`, border `#30363d`.
- Accent: `#3fb950` (profit), `#f85149` (loss), `#d29922` (warning), `#58a6ff` (info), `#bc8cff` (options), `#79c0ff` (crypto).
- Typography: JetBrains Mono for all numbers and code; Inter for all labels, headings, prose.
- Responsive: 1920×1080 primary; 1280px tablet; 480px mobile (halt button + status only).
- Keyboard shortcuts: `H` = halt, `R` = resume, `1–9` = tab select, `0` = System Health, `Space` = force refresh, `Esc` = dismiss alert, `P` = toggle shadow mode, `Ctrl+B` = toggle sidebar.

---

#### Tab 1: Command Center (Overview)

**Persistent Header Bar (fixed, always visible on all tabs):**
- Live equity in large font with `±$ / ±%` vs day open.
- Daily PnL (color-coded green/red/yellow).
- Three-arc progress gauge: Minimum / Ideal / Stretch targets.
- `source` badge: `DYNAMIC` / `OVERRIDE$` / `OVERRIDE%` (shows how today's targets were set).
- Drawdown % from ATH with micro-sparkline (last 10 days).
- Regime badge (colored: 🟢 BULL, 🔴 BEAR, 🟡 SIDEWAYS, ⚫ CRASH, 🔵 RECOVERY).
- Engine status badge (MARKET / PRE-MARKET / AFTER-HOURS / HALTED / SHADOW).
- NLP Tier badge: `LLM` / `FinBERT` / `VADER` (shows active NLP tier).
- Main cycle interval indicator: e.g., `⟳ 5min`.
- `■ HALT` button (red, requires click + 2s hold to prevent misfire).
- `▶ RESUME` (only visible when halted).
- Live ET clock.

**Dual Settlement Status Row:**
Shows two settlement cards side-by-side:
```
┌─────────────────────────────┐   ┌─────────────────────────────┐
│  PRELIMINARY (15:55 ET)     │   │  FINAL (20:00 ET)           │
│  Status: COMPLETED          │   │  Status: PENDING (3h 42m)   │
│  Regular PnL: +$287.50      │   │  AH PnL: — (in progress)   │
│  +2.81% of $10,240          │   │  Final PnL: TBD             │
└─────────────────────────────┘   └─────────────────────────────┘
```

**Capital State Machine Widget:**
- Current state badge (NORMAL / RECOVERY / COMPOUNDING / SOFT_HALT / HARD_HALT / EMERGENCY / CAPITAL_PRESERVATION / OPPORTUNITY_SURGE / EXCEPTIONAL_DAY).
- In RECOVERY: progress bar showing `recovery_progress / recovery_target` with day counter (e.g., "Day 2 of 5").
- In COMPOUNDING: streak counter with size multiplier (e.g., "🔥 Day 4 | 1.20× size").
- Starting Capital, Current Equity, Profit Lock Floor, Profit Wallet cumulative.

**Equity Curve (Lightweight Charts):**
- 30-day equity vs SPY, QQQ, BTC (selectable benchmarks).
- Regime transition lines (vertical, colored per regime).
- Halt events (red triangles, clickable for reason).
- Settlement markers: hollow circle = preliminary, solid circle = final.
- Click any day → Trade List modal for that day.

**Resolved Daily Targets Panel:**
Shows the resolved values from `DailyTargetConfig` for today:
```
Target Source: DYNAMIC (1.5% / 3.0% / 5.0% of $10,240 starting capital)
Minimum:   $153.60  [████████░░░░░░░░] $287.50 current ✓ MET
Ideal:     $307.20  [███████████████░] $287.50 → $19.70 to go
Stretch:   $512.00  ──────────────────
Emergency: -$512.00 (floor)
[Override for Today] button → opens inline override modal
```

**Override Modal (opens inline on click):**
```
Override Today's Targets
─ Method: ● Dynamic (current)  ○ Fixed %  ○ Fixed $
  If %:   Minimum [1.5]%  Ideal [3.0]%  Stretch [5.0]%
  If $:   Minimum [$____] Ideal [$____] Stretch [$____]
  Reason: [________________________] (optional note)
[Apply — Effective Next Cycle]  [Cancel]
```

**Open Positions Table, Opportunity Scanner Feed, Alert Center** — as described in v2.0, with additions:
- Positions table now has `Session` column (REGULAR / AFTER-HOURS).
- Scanner feed shows NLP tier used for each signal (LLM/FinBERT/VADER icon).

---

#### Tab 2: Strategy Command Center

- **Strategy Table (all 160+ strategies):** ID, Name, Family, Status (toggle), 7d PnL, 30d PnL, Win Rate (30d), Sharpe (30d), Avg Hold, Thompson Weight (animated bar), Regime Compatibility matrix (✅/⚠/❌ for each of 6 regimes), Health Indicator (🟢 HEALTHY / 🟡 WARN / 🔴 ERROR / ⚫ DISABLED_USER).
- **Health Tooltip (hover red dot):** Shows `error_message` + each step in `resolution_steps` as a numbered checklist. Shows `data_dependencies` required. "Retry Now" button to force re-run health_check.
- **Filter Bar:** Filter by family, regime, asset class, PnL sign, health status.
- **Bulk Controls:** Enable/disable all strategies in a family with one click. Enable/disable all strategies that share a data dependency (e.g., disable all Polygon-dependent strategies during API outage).
- **Strategy Detail Panel (click row):**
  - Full performance history chart (Sharpe, drawdown, win rate over time).
  - Current parameter values with inline editing (hot-reloaded on save).
  - Last 10 signals with outcomes (entry price, exit price, P&L, NLP tier used).
  - "Run Backtest" button → triggers backtest job, results in Tab 8.
  - Strategy-level drawdown gauge (vs 25% auto-halt threshold).
- **NLP Insights Panel (collapsible):** Shows latest NLP analysis by tier. Clearly labeled: "LLM Analysis (Tier 1)" or "FinBERT Analysis (Tier 2)" or "VADER Fallback (Tier 3)". Includes `fallback_rate` for last 24h (% of analyses that fell back from preferred tier).
- **Cycle Interval Control:** Slider input (1–10, integer steps). Shows label: "1 min (fastest, highest CPU)" to "10 min (slowest, lowest CPU)". Confirmation dialog on change. Applies immediately without restart.

---

#### Tab 3: Positions & Orders

- **Positions Panel:** Full sortable table. Unrealized PnL waterfall chart. Session column (REGULAR/AH).
- **Orders Panel:** All orders with broker, routing reason, execution algorithm, fill latency (ms), slippage (bps), session tag.
- **Trade Replay Modal (NEW):** Click any closed trade → full replay visualization:
  - 5-minute chart of the symbol spanning hold period.
  - Annotated entry and exit points with strategy signal details.
  - NLP score at entry (which tier was used, what score was produced).
  - Kalman-smoothed signal strength at entry vs raw.
  - Regime at time of trade. Actual vs expected P&L.
- **Trade History:** Searchable, filterable. Export to CSV/JSON.
- **P&L Calendar:** Monthly calendar showing daily PnL with color intensity. Click day → trade list. Shows both preliminary and final PnL on each day (two small values per cell for AH days).

---

#### Tab 4: Performance Analytics

- **PnL Attribution Waterfall (D3.js):** Strategy contribution to total PnL, ranked.
- **Drawdown Analysis:** Underwater equity curve. ATH-based and intraday comparison. Recovery time histogram.
- **Dual Settlement Chart:** For each trading day, shows two P&L values: regular session (bar) and after-hours addon (stacked segment). Visually shows which strategies contributed to AH gains.
- **Rolling Sharpe/Sortino (30d):** Line chart, target line at Sharpe = 3.0.
- **Win Rate Heatmap:** Strategy × Regime grid. Color: green > 60%, yellow 50–60%, red < 50%.
- **Factor Exposure Chart:** Current portfolio loadings on 5 factors. Historical range shading.
- **Correlation Matrix Heatmap (D3.js):** All holdings pairwise. Click cell for scatter plot. Flash-red cells > 0.85 (Step 13 risk trigger).
- **NLP Tier Usage Chart:** Pie chart of Tier 1/2/3 usage for last 30 days. Fallback trend line.
- **Monte Carlo VaR:** Histogram of 10,000 simulated 1-day returns. 99% VaR vertical line.
- **Capital State Timeline:** Gantt-style chart showing NORMAL / RECOVERY / COMPOUNDING periods over last 90 days. Recovery periods colored red, compounding green.

---

#### Tab 5: Options Dashboard

*(Visible only when `options_enabled = true`)*

All content from v2.0 retained. Additions:
- **After-Hours Options Monitor:** Shows options positions that remain active after 16:00 ET, with live AH underlying prices for rough Greek recalculation.
- **Straddle Pair Detector (IRS §1092):** Tax status panel showing any detected straddle pairs in the current positions, with their deferred loss status.
- **LEAPS Tracker (OP-05):** Dedicated row for long-dated bull spreads showing days to expiry, current delta, and annualized return to max profit.

---

#### Tab 6: Live Scanner

All content from v2.0 retained. Additions:
- **Pre-Market Catalyst Feed (04:00–09:30 ET):** Shows stocks gapping > 5% in pre-market with NLP score, volume, and the primary catalyst reason.
- **After-Hours Earnings Feed (16:00–20:00 ET):** Real-time EPS actual vs estimate. Beat/miss color-coded. NLP tier and score shown. A13 signal status for each ticker.
- **COT Positioning Panel:** Weekly CFTC Commitment of Traders data for Gold, Oil, Copper. Shows net speculative positioning as a %ile rank (useful for CO-01 strategy).
- **Global Session Panel:** Current returns for Nikkei, FTSE, DAX with F10 multiplier status (🟢 Bullish multiplier applied / ⚫ Neutral / 🔴 Bearish reduction applied).

---

#### Tab 7: Tax & Ledger

All content from v2.0 retained. Additions:
- **Section 1256 Tracker:** Separate panel for futures-derived ETF positions (USO, UNG, VXX structures if applicable) showing the 60/40 long/short-term split treatment.
- **Straddle Pairs (§1092):** Active straddle pairs, which leg is in a deferred loss, estimated deferred amount.
- **AMT Exposure Estimator:** Simple projection of AMTI and whether current year choices risk triggering AMT. WARN banner if AMT is projected.
- **Dual Settlement Tax Impact:** Shows how after-hours P&L affects the current day's tax lot selection and TLH decisions.

---

#### Tab 8: Backtest Console

All content from v2.0 retained. Additions:
- **Multi-Strategy Comparison:** Run backtests for multiple strategies simultaneously and overlay their equity curves on one chart.
- **Regime-Conditional Backtest:** Shows performance statistics separately for each regime period within the backtest window. Identifies which strategies degrade in specific regimes.
- **NLP Sensitivity Analysis (NEW):** For strategies that use NLP signals: replays the backtest with Tier 1 vs Tier 2 vs Tier 3 NLP and shows the performance difference. Quantifies the "LLM alpha" vs the FinBERT baseline.

---

#### Tab 9: System Health (NEW Tab)

A dedicated diagnostic and monitoring dashboard.

**Engine Topology Map (D3.js force-directed graph):**
Shows all system components as nodes (Engine, Brokers, Data Providers, Meta-Brain, NLP Engine, Redis, DuckDB, SQLite) with live connection status (green = connected, red = failing, yellow = degraded). Edge labels show latency (ms) for active connections. Click a node for detailed status.

**NLP Engine Status Panel:**
```
NLP ENGINE
─ Current Tier: TIER 2 (FinBERT/ONNX)
─ Tier 1 (LLM): DISABLED [Enable]  ← link to Settings
─ Tier 2 (SLM): ● HEALTHY  Model: FinBERT | Inference: 42ms avg
─ Tier 3 (VADER): ● HEALTHY (always available)
─ Last 24h: 847 analyses | T1: 0% | T2: 94% | T3: 6%
─ Fallback Events Today: 51 (ONNX timeout → VADER)
[View Fallback Log] [Export NLP Performance CSV]
```

**Strategy Health Grid:**
- All 160+ strategies shown as colored tiles: 🟢 HEALTHY, 🟡 WARN, 🔴 ERROR, ⚫ DISABLED.
- Hover tile: shows error message and resolution steps.
- "Retry All Failed" button: re-runs health_check on all DISABLED_ERROR strategies.
- "Download Health Report" button: exports current health state as JSON.

**Scheduler Status Panel:**
- Table of all 19 scheduled steps + health_monitor.
- Columns: Job Name, Schedule, Last Run, Last Duration, Next Run, Status (OK / LATE / FAILED).
- LATE or FAILED jobs highlighted in red with elapsed-since-due counter.
- "Trigger Now" button per job (for manual runs during testing or recovery).

**Database Health:**
- SQLite: write latency (ms) sparkline, WAL file size, last backup timestamp, total rows per major table.
- DuckDB: last ETL sync time, Parquet export status, query latency for last analytics query.
- Redis: `PING` latency (ms), memory usage, keys count, last flush-to-SQLite time; "REDIS UNAVAILABLE — using asyncio fallback" banner when down.

**System Metrics:**
- CPU %: engine process vs system total. Sparkline last 60 minutes.
- RAM: engine process usage in MB. Alert if > 4GB.
- Disk: `data_cache/` and `logs/` usage with growth rate.
- Network: bytes in/out per minute (shows API call load).
- WebSocket clients: number of currently connected UI sessions.

**Main Cycle Performance:**
- Per-cycle timing: avg time to complete one main_trading_cycle (ms).
- Breakdown: data fetch, indicator calc, signal gen, risk pipeline, execution.
- Alerts if any phase regularly exceeds `cycle_interval / 2` (cycle is taking too long).
- "Adjust Cycle Interval" quick-link → opens cycle interval slider from Settings.

---

#### Tab 10: Settings & Parameter Tuning

**Daily Target Override Panel:**
```
Today's Targets (Source: DYNAMIC — 1.5% / 3.0% / 5.0% of $10,240)
  Resolved: Min $153.60 | Ideal $307.20 | Stretch $512.00
Override Method: ● None  ○ Fixed %  ○ Fixed $
  [Apply Override — Effective Next Cycle]
```

**Live Parameter Controls (no restart required):**
- Main Cycle Interval: Slider 1–10 minutes (integer only). Current: 5.
- Max Open Positions (1–50): Current: 10.
- Risk Per Trade (% of equity): 0.5%–10%.
- Position Size Multiplier (0.25×–2.0×): applies globally.
- Kelly Fraction (0.10–0.50): Default 0.25.
- Vol Target Annualized (%): Default 15%.
- Soft Halt Loss (%): Default 1.5%.
- Hard Halt Loss (%): Default 3.0%.
- Recovery Risk Multiplier (0.25–1.0): Default 0.5.
- Max Single Position (% equity): Default 10%.
- All `control_flags` toggles (master switches).

**NLP Engine Controls:**
```
LLM Mode:  ● DISABLED  ○ LOCAL (Ollama)  ○ CLOUD
  LOCAL → Ollama Model: [llama3.3 ▼]
  CLOUD → Provider: [Anthropic ▼]  Daily Limit: [20] calls
  Fallback Override: ● Auto  ○ Always Tier 2  ○ Always Tier 3
```

**Broker Configuration:** Connection status, circuit breaker state, last API call, "Reconnect" button per broker, "Test All Brokers" button.

**Notification Channels:** Desktop Toast (Windows API), Email (SMTP config), Webhook (Slack/Discord URL), SMS (Twilio config). Per-channel minimum severity level.

**Backup & Maintenance:** "Run Backup Now", "Export DuckDB Parquet", "Purge Old Logs (>30d)", "Rebuild Feature Cache", "Force Strategy Health Check All", "Force HMM Retrain".

---

## 12. PERFORMANCE ANALYTICS & REPORTING

### 12.1 Daily Report (23:55 ET)

`data_cache/reports/daily_{date}.html` — HTML with embedded Chart.js charts.

Sections:
1. **Day Summary:** Starting capital, targets (source), preliminary PnL, after-hours PnL, final PnL, capital state transition.
2. **Trade Log:** All trades (entry, exit, P&L, hold time, strategy, NLP tier used, regime at entry).
3. **Open Positions:** Unrealized P&L, stop distances, Greeks.
4. **Strategy Performance:** Today's P&L contribution by strategy. Win/loss per strategy.
5. **Regime Log:** Regime transitions during the day.
6. **Risk Events:** Any halt triggers, risk check blocks, margin warnings.
7. **NLP Activity:** Tier breakdown today. Fallback events.
8. **Tax Events:** Any TLH executed, wash-sale entries added, lot method choices.
9. **Scanner Highlights:** Top 5 opportunities identified today (whether traded or not).

### 12.2 Weekly Report (Saturday)

`data_cache/reports/weekly_{YYYY-WW}.html`

Adds to daily content:
- 7-day PnL vs prior week and rolling 30-day.
- Strategy ranking by Sharpe (top 5 and bottom 5).
- PnL attribution waterfall.
- Portfolio correlation matrix snapshot.
- NLP tier usage trend over 7 days.
- Walk-forward OOS/IS Sharpe scores for all strategies.
- Tax efficiency: YTD harvested losses, projected annual liability, estimated quarterly payment due dates.
- Upcoming economic events (next 7 days, with strategy triggers noted).

### 12.3 Prometheus Metrics (if `prometheus_enabled = true`)

Endpoint: `http://localhost:8765/metrics`

| Metric | Type | Labels |
|---|---|---|
| `aqta_daily_pnl_usd` | Gauge | `session` (preliminary/final) |
| `aqta_daily_targets_usd` | Gauge | `type` (min/ideal/stretch), `source` |
| `aqta_portfolio_equity_usd` | Gauge | — |
| `aqta_drawdown_pct` | Gauge | `type` (intraday/ath) |
| `aqta_capital_state` | Gauge (enum) | `state` |
| `aqta_open_positions_count` | Gauge | `asset_class` |
| `aqta_trades_total` | Counter | `strategy_id`, `direction` |
| `aqta_signal_strength` | Histogram | `strategy_id`, `nlp_tier` |
| `aqta_order_latency_ms` | Histogram | `broker`, `algo` |
| `aqta_regime_state` | Gauge | `state` |
| `aqta_portfolio_delta` | Gauge | — |
| `aqta_portfolio_theta_daily` | Gauge | — |
| `aqta_risk_check_blocked` | Counter | `rule_name` |
| `aqta_nlp_tier` | Gauge | `active_tier` |
| `aqta_nlp_inference_ms` | Histogram | `tier` |
| `aqta_main_cycle_duration_ms` | Histogram | — |
| `aqta_strategy_win_rate` | Gauge | `strategy_id`, `regime` |
| `aqta_strategy_drawdown_pct` | Gauge | `strategy_id` |
| `aqta_compounding_streak` | Gauge | — |
| `aqta_recovery_day` | Gauge | — |
| `aqta_margin_utilization_pct` | Gauge | — |

---

## 13. BACKTESTING & WALK-FORWARD VALIDATION

### 13.1 Backtester (`engine/backtest/backtester.py`)

**Data Sourcing:** Loads OHLCV + full indicator set from Parquet feature store (`data_cache/features/`). On first run for a symbol/period, fetches from the free API chain (yfinance primary) and caches. Survivorship bias control: uses `sp500_membership_history.parquet` (point-in-time index membership).

**Realistic Fill Model:**
- Market orders: fill at `close × (1 + slippage)` for buys, `close × (1 − slippage)` for sells.
- Limit orders: only filled if `low ≤ limit_price` (buys) or `high ≥ limit_price` (sells).
- Slippage model: `slippage = N(0, 0.0003) × sqrt(order_size / avg_daily_volume)`.
- Commission model: configurable (flat-per-trade default `$0.00`; per-share `$0.005` for IBKR model; percentage `0.01%` for Schwab model).

**After-Hours Backtest Support:** For strategies A13 and B9, uses after-hours OHLCV data (available via Polygon paid tier; degrades gracefully if unavailable, skips AH-specific strategies).

**NLP Backtesting:** For strategies using NLP signals, replays historical news headlines through the current NLP tier. Can also run in "retrospective mode" with pre-cached FinBERT scores for historical dates.

### 13.2 Walk-Forward Validation (`engine/backtest/walk_forward.py`)

- **Method:** Rolling window. In-sample: 18 months. Out-of-sample: 3 months. Rolls forward 3 months each iteration.
- **Overfitting Score:** `OOS_Sharpe / IS_Sharpe`. Score < 0.50 → WARN (possible overfit). Score < 0.30 → AUTO_DISABLE (pending review). Scores stored per run in `backtest_results.walk_forward_is_oos`.
- **Hyperparameter Optimization (Optuna):** TPE sampler on in-sample period. Parameter search space defined per-strategy in `strategy_config.toml`. OOS validates found parameters without re-fitting.
- **NLP Ablation:** Walk-forward runs with and without NLP signals; stores delta Sharpe in `backtest_results` to quantify NLP contribution per strategy.

### 13.3 Monte Carlo Simulation (`engine/backtest/monte_carlo.py`)

- **10,000 paths** using Cholesky decomposition of current asset covariance matrix.
- Uses `numba` JIT compilation for performance (50× speedup vs pure NumPy for 10k paths).
- Outputs: 1-day VaR (99%), 5-day VaR (95%), CVaR (Expected Shortfall at 99%), probability of drawdown > 5% / 8% / 15% over next 30 days.
- Stored in `portfolio_snapshots.monte_carlo_json` nightly.

### 13.4 Stress Test Scenarios

Historical crisis scenarios replayed against current portfolio composition:
- **2008 Financial Crisis (Oct–Dec 2008):** −40% equity peak-to-trough.
- **2020 COVID Crash (Feb–Mar 2020):** −34% in 23 trading days.
- **2022 Rate Shock (Jan–Oct 2022):** −25% equity, −14% bonds simultaneously.
- **2010 Flash Crash (May 6, 2010):** −9.2% intraday in 36 minutes.
Results stored in `portfolio_snapshots.stress_test_json`. Alert if any scenario > 15% projected drawdown.

---

## 14. SYSTEM CONFIGURATION & DEPLOYMENT

### 14.1 Complete `config/settings.toml`

```toml
[system]
engine_port = 8765
ui_port = 8766
timezone = "America/New_York"
log_level = "INFO"          # DEBUG | INFO | WARN | ERROR
log_rotation_days = 30
log_format = "json"         # json | text

[capital]
daily_capital_base = 10000.0
min_profit_target_pct = 1.5
ideal_profit_target_pct = 3.0
stretch_profit_target_pct = 5.0
exceptional_day_pct = 7.5
profit_lock_trigger_pct = 20.0   # % of ideal target
profit_protect_pct = 0.60
profit_lock_step2_pct = 0.70
soft_halt_loss_pct = 1.5
hard_halt_loss_pct = 3.0
emergency_halt_loss_pct = 5.0
profit_sweep_threshold = 30000.0
recovery_max_days = 5
recovery_risk_multiplier = 0.5
compounding_streak_days = 5
compounding_size_multiplier = 1.20
compounding_max_multiplier = 1.50
capital_base_scale_per_10d = 0.05

[scheduler]
main_cycle_interval_minutes = 5    # Valid: 1–10 integer
crypto_cycle_interval_minutes = 15

[risk]
max_single_position_pct = 0.10
max_single_position_leveraged_pct = 0.05
max_sector_pct = 0.35
max_correlation_threshold = 0.75
correlation_block_threshold = 0.90
max_portfolio_leverage_overnight = 2.0
max_portfolio_leverage_intraday = 4.0
pdt_equity_buffer = 26500.0
kelly_fraction = 0.25
vol_target_annualized = 0.15
intraday_drawdown_soft_pct = 0.02
intraday_drawdown_hard_pct = 0.04
max_strategy_drawdown_pct = 0.25
margin_utilization_warn_pct = 0.75
margin_utilization_halt_pct = 0.90
max_open_positions = 10
total_portfolio_at_risk_pct = 0.06  # Max 6% of equity at risk simultaneously

[greeks_limits]
net_delta_warn = 0.20          # × NAV
net_delta_block = 0.30
net_gamma_warn = 0.015         # × NAV
net_gamma_block = 0.025
net_theta_warn = -200.0        # $/day
net_theta_block = -300.0
net_vega_warn = 500.0          # $ per 1% IV move
net_vega_block = 800.0

[data]
primary_data_provider = "yfinance"   # yfinance | polygon
universe_min_adtv_usd = 5_000_000
universe_min_price = 1.0
universe_max_price = 5000.0
cache_ttl_daily_bars_hours = 24
cache_ttl_intraday_bars_hours = 1
feature_cache_dir = "data_cache/features"
max_cache_size_gb = 50.0

[nlp]
llm_mode = "DISABLED"              # DISABLED | LOCAL | CLOUD
local_model = "llama3.3"
ollama_base_url = "http://localhost:11434"
cloud_fallback_enabled = false
cloud_provider = "anthropic"       # anthropic | openai
max_cloud_calls_per_day = 20
finbert_model = "ProsusAI/finbert"
finbert_onnx_path = "data_cache/models/finbert.onnx"
finbert_batch_size = 32
vader_enabled = true               # Tier 3 always on

[tax]
tlh_min_loss_threshold = -500.0
tlh_min_loss_threshold_december = -300.0
marginal_tax_rate = 0.35
ltcg_tax_rate = 0.20
state_tax_rate = 0.09
gain_deferral_window_start_days = 335
gain_deferral_window_end_days = 365
amt_check_enabled = true

[backtest]
survivorship_bias_control = true
default_commission = 0.0
default_slippage_bps = 3.0
mc_simulation_paths = 10000
walk_forward_is_months = 18
walk_forward_oos_months = 3
auto_disable_oos_threshold = 0.30
warn_oos_threshold = 0.50

[notifications]
desktop_notifications = true
email_enabled = false
smtp_server = ""
smtp_port = 587
smtp_username = ""
webhook_enabled = false
webhook_url = ""
sms_enabled = false
twilio_sid = ""
twilio_token = ""
min_alert_level = "WARN"           # INFO | WARN | CRITICAL

[crypto]
default_exchange = "coinbase"      # coinbase | binance | robinhood
defi_enabled = false               # web3 DeFi interactions
funding_rate_monitor = true
fear_greed_check_hours = 4

[redis]
host = "localhost"
port = 6379
db = 0
max_memory_mb = 512

[backup]
enabled = true
retention_days = 30
compress = true
path = "data_cache/backups"
```

---

### 14.2 `config/broker_secrets.env` Template

```env
# SCHWAB
SCHWAB_CLIENT_ID=
SCHWAB_CLIENT_SECRET=
SCHWAB_REDIRECT_URI=https://127.0.0.1:8080

# ROBINHOOD
ROBINHOOD_USERNAME=
ROBINHOOD_PASSWORD=
ROBINHOOD_MFA_CODE=     # or set up TOTP via pyotp

# IBKR (Interactive Brokers)
IBKR_HOST=127.0.0.1
IBKR_PORT=7497          # 7497 = paper, 7496 = live
IBKR_CLIENT_ID=1

# ALPACA
ALPACA_API_KEY=
ALPACA_SECRET_KEY=
ALPACA_BASE_URL=https://api.alpaca.markets  # or paper URL

# COINBASE
COINBASE_API_KEY=
COINBASE_API_SECRET=

# DATA PROVIDERS
POLYGON_KEY=            # Optional (free tier has limited data)
NEWSAPI_KEY=            # 100 req/day free
FINNHUB_TOKEN=          # Free tier available
FRED_API_KEY=           # Free, unlimited
ALPHAVANTAGE_KEY=       # 25 req/day free

# NOTIFICATIONS
SMTP_PASSWORD=
TWILIO_PHONE_FROM=
TWILIO_PHONE_TO=
SLACK_WEBHOOK_URL=
DISCORD_WEBHOOK_URL=

# LLM (OPTIONAL — ONLY IF CLOUD FALLBACK ENABLED)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
```

---

### 14.3 First-Run Setup (`scripts/first_run_setup.py`)

Interactive wizard run once. Performs:
1. Verifies Python 3.11+. Checks for required compiled libraries (ta-lib).
2. Copies `broker_secrets.env.example` → `broker_secrets.env` and prompts for each key.
3. Prompts for tax rates (marginal, LTCG, state) and updates `settings.toml`.
4. Runs `python engine/database/migrations.py` — creates all 18 SQLite tables, pre-populates `control_flags`.
5. Downloads and caches ONNX model: `python scripts/export_model.py` (exports FinBERT to ONNX format for fast inference).
6. Runs `python scripts/fetch_history.py --years 2` — downloads 2-year historical data for the default universe (S&P 500 + top 50 ETFs).
7. Trains initial HMM model on downloaded data.
8. Tests all broker connections in paper/mock mode.
9. Confirms `shadow_mode = true`.
10. Opens UI in default browser at `http://localhost:8766`.

### 14.4 Windows Service Installation (`install_service.bat`)

```batch
@echo off
echo Installing AQTA Windows Services...

:: Engine service
nssm install AQTA_Engine "C:\Python311\python.exe" "C:\TradingSystem\engine\main.py"
nssm set AQTA_Engine AppDirectory "C:\TradingSystem"
nssm set AQTA_Engine AppEnvironmentExtra "PYTHONPATH=C:\TradingSystem"
nssm set AQTA_Engine AppStdout "C:\TradingSystem\logs\engine.log"
nssm set AQTA_Engine AppStderr "C:\TradingSystem\logs\engine_err.log"
nssm set AQTA_Engine Start SERVICE_AUTO_START
nssm set AQTA_Engine AppRestartDelay 5000
nssm set AQTA_Engine AppThrottle 1500

:: UI service
nssm install AQTA_UI "C:\Python311\python.exe" "C:\TradingSystem\ui\ui_server.py"
nssm set AQTA_UI AppDirectory "C:\TradingSystem"
nssm set AQTA_UI AppStdout "C:\TradingSystem\logs\ui.log"
nssm set AQTA_UI AppStderr "C:\TradingSystem\logs\ui_err.log"
nssm set AQTA_UI Start SERVICE_AUTO_START
nssm set AQTA_UI AppRestartDelay 3000

net start AQTA_Engine
net start AQTA_UI
echo Done. UI at http://localhost:8766
pause
```

### 14.5 Health Check Script (`scripts/check_health.bat`)

```batch
@echo off
echo ─── AQTA Health Check ───
curl -s http://localhost:8765/health | python -m json.tool
echo.
echo ─── Strategy Health ───
curl -s http://localhost:8765/system/health_checks | python -c "import json,sys; d=json.load(sys.stdin); [print(f'{s[\"id\"]}: {s[\"status\"]}') for s in d['strategies']]"
echo.
echo ─── NLP Status ───
curl -s http://localhost:8765/system/nlp_status | python -m json.tool
pause
```

### 14.6 Optional Components

| Component | Install | Enable Flag |
|---|---|---|
| Redis 7 (WSL2) | `apt install redis-server && redis-server --daemonize yes` | `redis_enabled = true` |
| Redis 7 (Windows) | Redis for Windows (GitHub: tporadowski) | Same |
| Prometheus | Download prometheus.io/download | `prometheus_enabled = true` |
| Grafana | Download grafana.com/grafana/download | Connect to `:8765/metrics` |
| Ollama | Download ollama.ai/download | `llm_mode = "LOCAL"` |
| CUDA (GPU acceleration) | `pip install torch --index-url https://download.pytorch.org/whl/cu121` | Auto-detected |
| ta-lib | Pre-compiled wheel from `whl.pythonhosted.org` | Auto-detected at startup |
| IBKR TWS/Gateway | Download IBKR Trader Workstation | Configure `IBKR_PORT` |

---

## 15. IMPLEMENTATION PHASES (15-Phase Copilot Roadmap)

Each phase has:
- **Deliverable:** What exists after this phase.
- **Acceptance Criteria:** Measurable tests.
- **Prompt:** Copilot/AI instruction to kick off the phase.

---

### Phase 1 — Project Scaffold & Database

**Deliverable:** Directory structure, `settings.toml`, `broker_secrets.env.example`, SQLite schema (all 18 tables + DuckDB schema), `migrations.py`, `first_run_setup.py`, `config.py`.

**Acceptance Criteria:**
- `python engine/database/migrations.py` creates all tables with no errors.
- `control_flags` table pre-populated with all 24 default rows.
- `DailyTargetConfig` dataclass unit-tested: given `starting_capital=10000`, `min_profit_target_pct=1.5`, asserts `min_target_usd=150.0`.

**Prompt:** "Create the AQTA project scaffold. Generate the full directory structure under `C:\TradingSystem\`. Create `config/settings.toml` with all sections from the spec. Generate `engine/database/models.py` using SQLAlchemy 2.0 ORM with all 18 tables including v3 additions (`llm_fallback_log`, `strategy_correlation_matrix`, `dark_pool_prints`, `options_positions`, `greeks_snapshots`, `crypto_positions`, `funding_rate_log`). Generate `migrations.py` that creates tables and seeds `control_flags`. Include `DailyTargetConfig` dataclass in `engine/brain/daily_pnl_manager.py`."

---

### Phase 2 — Capital Framework & DailyPnLManager

**Deliverable:** `DailyPnLManager` with full state machine, `initialize_day()`, `settle_regular_session()`, `settle_final()`, `lock_in_profits()`. All targets dynamic from `starting_capital × pct`. Override logic from `control_flags`. Capital state machine with all 9 states and transitions.

**Acceptance Criteria:**
- Unit test: `initialize_day(starting_capital=12500)` with defaults → `min_target_usd=187.50`, `ideal_target_usd=375.00`, source=`"DYNAMIC_PCT"`.
- Unit test: `initialize_day()` with `target_override_usd=$500` in `control_flags` → `min_target_usd=500`, source=`"OVERRIDE_USD"`.
- Unit test: override pct = 2.0% → `min_target_usd=250.0`, source=`"OVERRIDE_PCT"`.
- State machine test: 5 consecutive wins → state = COMPOUNDING, `size_multiplier=1.20`.
- Dual settlement test: `settle_regular_session()` + `settle_final()` both write correct columns to `daily_cycle_log`.

**Prompt:** "Implement `engine/brain/daily_pnl_manager.py` per the AQTA v3 spec. Include: `DailyTargetConfig` dataclass (all fields), `initialize_day()` with 3-priority override logic, capital state machine enum with all 9 states and transition rules, `settle_regular_session()` writing to `preliminary_pnl`, `settle_final()` writing to `final_pnl` and `after_hours_pnl`, `lock_in_profits()` ratchet logic, and `OPPORTUNITY_SURGE` detection. Full async interface. Unit tests covering all override scenarios and state transitions."

---

### Phase 3 — Broker Integration Layer

**Deliverable:** `BaseBroker` ABC (all abstract methods including `get_after_hours_quote`), `MockBroker` (full simulation), `SchwabBroker`, `RobinhoodBroker`, `IBKRBroker`, `AlpacaBroker`, `CoinbaseBroker`. `SmartOrderRouter` with 8-rule chain. All execution algorithms in `algo_orders.py`.

**Acceptance Criteria:**
- MockBroker: place limit order → fill simulation → position appears in `positions` table.
- SOR test: after-hours order (16:30 ET) → routes to `RobinhoodBroker` (rule 3).
- SOR test: notional $150k → routes to `IBKRBroker` (rule 6).
- Circuit breaker: 3 consecutive 500-errors → circuit OPEN; 4th call returns cached error without hitting API; after 5 min → circuit CLOSED again.

**Prompt:** "Implement the complete broker integration layer for AQTA v3. Include: `engine/brokers/base_broker.py` with all abstract methods from the spec; `MockBroker` that simulates fills with configurable slippage and latency; `SchwabBroker` using `schwab-py` library; `RobinhoodBroker` using `robin_stocks`; `IBKRBroker` using `ib_insync`; `AlpacaBroker`; `CoinbaseBroker` using `ccxt`. Add the `SmartOrderRouter` with all 8 routing rules. Implement all execution algorithms (MARKET, LIMIT, TWAP, VWAP, ICEBERG, POV, SNIPER, CLOSE_ONLY, AH_LIMIT). All brokers must implement the circuit breaker pattern."

---

### Phase 4 — Data Engine & Alternative Data

**Deliverable:** `MarketData`, `OptionsData`, `MacroData`, `AlternativeData`, `Level2Data`, `DarkPoolData`, `OnChainData`, `NewsStream`. Free API cascade. Parquet feature cache. `MultiTimeframeData`. All indicators from spec.

**Acceptance Criteria:**
- `MarketData.get_ohlcv("AAPL", period="2y", interval="1d")` → returns DataFrame; second call returns from cache.
- `AlternativeData.get_insider_buys()` → DataFrame from OpenInsider scrape.
- `MacroData.get_fred("DGS10")` → Series of 10Y treasury yields.
- Indicators: given sample OHLCV, `calculate_all_indicators()` adds all 22+ indicators without NaN on data > 200 rows.
- `MultiTimeframeData` for "MSFT" returns dict with keys: `1m, 5m, 15m, 30m, 1h, 1d`.

**Prompt:** "Implement the complete data engine for AQTA v3 in `engine/data/`. Implement free-API-first cascade (no paid APIs required). Include: `MarketData` (yfinance primary, Polygon optional), `OptionsData` (yfinance + Polygon), `MacroData` (FRED API, US Treasury API), `AlternativeData` (OpenInsider scrape, congressional trades scrape, FINRA ATS dark pool, EIA energy, CFTC COT, StockTwits), `Level2Data` (conditional on `level2_enabled`), `DarkPoolData`, `OnChainData` (Glassnode free tier, Binance public), `NewsStream` (NewsAPI + real-time async). All data cached in Parquet. Include `MultiTimeframeData` aggregator."

---

### Phase 5 — NLP 3-Tier Engine

**Deliverable:** `NLPEngine` dispatcher, `LLMAnalyst` (Tier 1), `SLMScorer` (Tier 2, FinBERT + ONNX), `KeywordScorer` (Tier 3, VADER). `export_model.py` script. All structured output schemas. `llm_fallback_log` writes.

**Acceptance Criteria:**
- With `llm_mode = "DISABLED"`: `NLPEngine.analyze("AAPL is crushing earnings", "AAPL")` → uses Tier 2 ONNX; returns `{direction: "BULLISH", confidence: ≥0.80}`.
- With SLM models deleted (force-fail): falls through to Tier 3 VADER; returns `{direction: "BULLISH"}` based on VADER compound score.
- Tier fallback logged to `llm_fallback_log` every time.
- Batch inference test: 100 headlines processed by FinBERT ONNX in < 5 seconds on CPU.
- `export_model.py` produces `data_cache/models/finbert.onnx` that loads cleanly with `onnxruntime`.

**Prompt:** "Implement the AQTA v3 3-tier NLP engine in `engine/meta_brain/nlp_engine.py`. Tier 1: `LLMAnalyst` using Ollama or Anthropic/OpenAI via `llm_mode` flag; structured JSON output. Tier 2: `SLMScorer` using FinBERT via HuggingFace `transformers` + ONNX export for fast inference; batch tokenization. Tier 3: `KeywordScorer` using `vaderSentiment` as the always-available deterministic fallback. Include `scripts/export_model.py` to export FinBERT to ONNX. Auto-fallback logic per spec. All tier choices logged to `llm_fallback_log`. Include `analyze_news()`, `analyze_earnings()`, `analyze_sec_filing()` with all 3 tiers."

---

### Phase 6 — Meta-Brain & Portfolio Optimizer

**Deliverable:** `RegimeDetector` (HMM + LightGBM ensemble), `ContextualThompsonSampler`, `KalmanSmoother`, `OnlineLearner` (Page-Hinkley drift detection), `PortfolioOptimizer` (MVO, CVaR-MVO, HRP, regime-conditional), stress test runner.

**Acceptance Criteria:**
- `RegimeDetector` trains on 2 years of SPY data in < 60 seconds. Predicts one of 6 regimes with probabilities summing to 1.0.
- `ensemble_agreement < 0.45` → regime = `"UNCERTAIN"`.
- Thompson Sampler: given 5 consecutive wins for strategy A → A's weight increases. After a loss → weight decreases.
- `strategy_correlation_matrix` penalty: if strategies A and B have r > 0.8 → lower-performing weight reduced per formula.
- `KalmanSmoother.smooth([0.8, 0.2, 0.9, 0.1, 0.85])` returns smoother series than input.
- Stress test: given a position in SPY, `run_stress_test()` returns a dict with `2008_drawdown`, `2020_drawdown`, `2022_drawdown` keys.

**Prompt:** "Implement the AQTA v3 Meta-Brain in `engine/meta_brain/`. Include: `RegimeDetector` using `GaussianHMM` (hmmlearn) + `LightGBM` ensemble with 6 regime states and the feature set from the spec; `ContextualThompsonSampler` with magnitude-weighted Bayesian updates and strategy correlation penalty using the `strategy_correlation_matrix` table; `KalmanSmoother` (filterpy) with per-strategy-family noise tuning; `OnlineLearner` with Page-Hinkley drift detection triggering emergency retrain; `PortfolioOptimizer` with MVO, CVaR-MVO, and HRP (riskfolio-lib) with regime-conditional covariance matrices and stress test scenarios."

---

### Phase 7 — Risk Management Engine

**Deliverable:** `RiskManager` (full 15-step pipeline), `GreeksMonitor`, `MarginOptimizer`, `compliance.py` (all regulatory checks), `ComplianceAuditLog` writes.

**Acceptance Criteria:**
- Step 5 (PDT): given `{"day_trades_5d": 3, "equity": 24000}` → blocks; `{"day_trades_5d": 2, "equity": 24000}` → passes.
- Step 6 (Wash-Sale): SELL of AAPL at a loss when AAPL is in `wash_sale_blacklist` → blocks; offers IVV as proxy.
- Step 7 (Concentration): order of $1,500 on $10,000 equity (15%) → resized to $1,000 (10%).
- Step 13 (Correlation Spike): given all positions at correlation 0.90 → blocks new long entry.
- Step 15 (Strategy Drawdown): given strategy drawdown = 26% → strategy auto-disabled.
- All blocks logged to `compliance_audit_log` with rule name and reason.

**Prompt:** "Implement `engine/risk/risk_manager.py` with the full 15-step pre-trade pipeline per AQTA v3 spec. Each step must return `RiskCheckResult(passed: bool, rule: str, reason: str, auto_action_taken: str | None)`. All failures log to `compliance_audit_log`. Implement `GreeksMonitor` (recalculate portfolio Greeks every 5 min; warn at 80% of limits; block at 100%). Implement `MarginOptimizer` (rank positions by risk-adjusted margin efficiency; auto-close worst 2 if margin > 90%). Include `compliance.py` with all regulatory checks from the compliance matrix."

---

### Phase 8 — Strategy Arsenal (Batch 1: Core Families)

**Deliverable:** All 27 Momentum strategies (EQ-01 to EQ-10, A1–A18), all 14 Mean Reversion strategies (EQ-03, B1–B14), `BaseStrategy` ABC with `health_check()`, `StrategyLoader`.

**Acceptance Criteria:**
- `BaseStrategy` has all 4 abstract methods: `generate_signals`, `calculate_position_size`, `_rule_based_fallback`, `health_check`.
- `StrategyLoader.health_check_all()` completes in < 30 seconds for all 27+14 strategies.
- A1 (ORB): given 15 minutes of 1-min OHLCV where high of 9:30–9:44 = $150.20, low = $149.50, and 9:45 candle closes at $150.80 on 3× volume → generates BUY signal, stop = $149.50, target = $151.30.
- B6 (Connors RSI): given CRSI < 10 AND price above 200-day SMA → generates BUY signal.
- A8 (VWAP MACD 1-min): requires `intraday_strategies_enabled = true`; correctly disabled when flag is false.
- All strategies: `_rule_based_fallback()` works without any NLP call.

**Prompt:** "Implement all Equity Momentum and Mean Reversion strategies for AQTA v3 in `engine/strategies/equity/`. Implement `BaseStrategy` ABC with `generate_signals()`, `calculate_position_size()` (Kelly-based), `_rule_based_fallback()`, and `health_check() -> HealthStatus`. Implement `StrategyLoader` with concurrent health checks and auto-retry. Implement: EQ-01 (Trend Following), EQ-03 (BB Mean Reversion), EQ-05–EQ-10, A1 (ORB), A2 (VWAP Momentum), A3 (Gap-and-Go), A4–A18 as fully specified. B1–B14 including B6 (Connors RSI), B7 (StdDev Channel), B8 (POC Reversion), B9 (AH Liquidity Fade)."

---

### Phase 9 — Strategy Arsenal (Batch 2: Sentiment, Quant, Macro)

**Deliverable:** All 16 Sentiment/Copy strategies (D1–D16), all 16 Quant/Arb strategies (EQ-02, E1–E16), all 18 Macro strategies (F1–F18).

**Acceptance Criteria:**
- D1 (Congress): given a congressional trade filing with date < 48h ago and size > $15,000 → generates BUY signal.
- D11 (SLM News Flash): processes a headline in < 100ms end-to-end (headline → SNIPER order queued).
- E7 (Index Rebalance Arb): given S&P 500 announcement of new addition → generates BUY signal within 1 hour.
- F3 (FOMC): given `economic_events` has FOMC 3 days out → queues VXX buy; on FOMC day, evaluates market direction.
- F10 (Global Handoff): Nikkei +2.1% AND FTSE +1.8% → `global_bullish_multiplier = 1.3` applied to A3/A10/A12 that day.
- All D-series strategies use NLP tier from `NLPEngine` (not a direct LLM call).

**Prompt:** "Implement all Sentiment, Quant/Arbitrage, and Macro strategies for AQTA v3. D1–D16 in `engine/strategies/sentiment/`: D1 Congressional replication, D2 Insider Cluster, D3 FinBERT Sentiment, D4 WSB Reddit, D5 Google Trends, D6 Dark Pool Flow, D7 13F Builder, D8 UOA Equity Signal, D9 C-Suite Conviction, D10 Dark Pool Print, D11 SLM News Flash, D12 Social Divergence, D13 ETF Flow, D14 Earnings Whisper, D15 Block Trade Detector, D16 Supply Chain. E1–E16 in `engine/strategies/quant/`. F1–F18 in `engine/strategies/macro/`. All use the `NLPEngine` 3-tier dispatch — never call LLM directly."

---

### Phase 10 — Strategy Arsenal (Batch 3: Cash/Hedge, Options, Crypto, FX/FI, Group G)

**Deliverable:** All 13 Cash/Hedging strategies (CM-01 to CM-12, EQ-04/EQ-05), all 14 Options strategies (OP-01 to OP-12, C4, C6–C9), all 7 Crypto strategies (CR-01–CR-07), FX and FI strategies, Group G (G1–G4), Commodities (CO-01/CO-02), Volatility (VX-01/VX-02), Alternatives (AL-01–AL-03).

**Acceptance Criteria:**
- CM-01 (Money Market Sweep): cash > $1,500 at 16:15 → buy SWVXX order queued.
- CM-05 (Margin Minimizer): margin > 90% → flags 2 worst-ranked positions for liquidation.
- EQ-05 (Tail Risk Convexity): VIX < 12 AND SPY at 52-week high → VIX call option buy signal generated (blocked if `options_enabled = false`).
- G1 (Leveraged ETF): disabled when regime is not BULL_TREND; disabled when `leveraged_strategies_enabled = false`.
- G4 (Short Vol Carry): exits immediately on VIX spike > 20%.
- AL-02 (SPAC NAV Arb): scans SPAC universe; returns any SPAC with price < $9.90.
- All Group G strategies respect 5% max position cap.

**Prompt:** "Implement the remaining strategy families for AQTA v3. Cash/Hedging in `engine/strategies/cash_hedging/`: CM-01–CM-12, EQ-04 (Flash Crash), EQ-05 (Tail Risk Convexity). Options in `engine/strategies/options/`: OP-01–OP-12, C4, C6–C9, OP-05 (LEAPS Bull Spread). Crypto in `engine/strategies/crypto/`: CR-01–CR-07. FX/FI in `engine/strategies/fx_fi/`. Leveraged in `engine/strategies/leveraged/`: G1–G4 with BULL_TREND gate and 5% position cap. Commodities CO-01, CO-02. Volatility VX-01, VX-02. Alternatives AL-01, AL-02, AL-03."

---

### Phase 11 — Execution Engine & Signal Aggregator

**Deliverable:** `ExecutionEngine` (priority queue, concurrent order submission), `SignalAggregator` (dedup, merge, Kalman smoothing), `StateCacheManager` (Redis + asyncio fallback), `OpportunityScanner` (5-level architecture), DuckDB analytics layer.

**Acceptance Criteria:**
- `SignalAggregator`: two BUY signals on "AAPL" within 30 minutes → merged (single order, strength averaged with Kalman weight).
- `ExecutionEngine.route(order)`: in shadow mode → routes to MockBroker.
- `StateCacheManager`: Redis down → seamlessly switches to asyncio dict; `get(key)` returns cached values.
- `OpportunityScanner.run_full_scan()` completes in < 30 seconds for a 500-stock universe with all scoring enabled.
- DuckDB ETL: `sync_to_duckdb()` copies yesterday's closed trades; `DuckDB SELECT` returns the row.
- `OPPORTUNITY_SURGE` state: 5 HIGH signals in one cycle → state transitions correctly.

**Prompt:** "Implement the execution and aggregation layer for AQTA v3. Implement `engine/execution/execution_engine.py` with priority-ordered concurrent order submission using `asyncio.gather`. Implement `engine/brain/signal_aggregator.py` with 30-minute deduplication window, signal merging (average Kalman-smoothed strength), and expiry of old signals. Implement `engine/brain/state_cache_manager.py` with Redis primary and asyncio native fallback (seamless switching). Implement the 5-level `OpportunityScanner` with full composite scoring. Implement `engine/database/analytics_db.py` DuckDB ETL layer."

---

### Phase 12 — Tax Engine

**Deliverable:** `TaxEngine` (lot selection with 4 methods + AMT check), `TaxOptimizer` (TLH, gain deferral, proxy scoring), `TaxReporter` (Form 8949, quarterly payments, year-end), wash-sale blacklist management, December aggressive mode.

**Acceptance Criteria:**
- Lot method selection: given `amt_exposure_projected=True` → method = FIFO regardless of losses.
- TLH opportunity cost test: unrealized loss = $1,000 on a stock with annual return 20% → opportunity cost = $1,000 × 0.20 / 12 × 31/21 = ~$24. Tax saving at 35% = $350 > $24 × 1.2 → harvests.
- Proxy swap: AAPL sold at loss → IVV offered (score 0.72 → accepted since > 0.60 threshold). SPY SPDR sold → IVV (score 0.99 → excellent).
- Form 8949: given 10 closed trades, `generate_form_8949()` returns correct short/long-term classification with proceeds, cost, and gain/loss columns.
- December mode: threshold drops to $300; gain deferral runs for all 335–365-day positions.
- Quarterly payment planner: given YTD STCG = $5,000, `calculate_estimated_payment(quarter=2)` returns correct safe harbor amount.

**Prompt:** "Implement the complete tax optimization engine for AQTA v3. `engine/tax/tax_engine.py`: lot selection with FIFO/HIFO/LTCG_FIRST/LOSS_FIRST and AMT impact assessor. `engine/tax/tax_optimizer.py`: TLH with opportunity cost analysis, gain deferral optimizer (3 strategies: unhedged/put/call), proxy scoring with formula from spec, proxy_swap_map.json, wash-sale blacklist management, December aggressive mode. `engine/tax/tax_reporter.py`: Form 8949 CSV + PDF, quarterly estimated payment calculator with safe harbor, year-end report generator, Section 1256 contracts, straddle detection."

---

### Phase 13 — Scheduler (16 Steps)

**Deliverable:** `engine/scheduler/jobs.py` with all 19 APScheduler jobs. `main_cycle_interval_minutes` parameter validation and hot-reload. Dual settlement (Steps 12 and 16). Pre-market scanning. After-hours transition.

**Acceptance Criteria:**
- On startup: all 19 jobs registered in APScheduler.
- `POST /control/flag` with `{"key": "main_cycle_interval_minutes", "value": "3"}` → main trading cycle changes from 5-min to 3-min interval within 1 cycle (no restart).
- Value "11" → rejected; returns `{"error": "main_cycle_interval_minutes must be 1–10"}`.
- `preliminary_settlement` fires at exactly 15:55 ET; writes `preliminary_pnl` to `daily_cycle_log`.
- `final_settlement` fires at exactly 20:00 ET; writes `final_pnl` and `after_hours_pnl`.
- `health_monitor` fires every 60 seconds without missing; if it misses by > 2 minutes, fires CRITICAL alert.
- `nightly_maintenance` fires at 23:55 ET; DuckDB ETL runs; daily HTML report generated.

**Prompt:** "Implement `engine/scheduler/jobs.py` for AQTA v3 with all 19 APScheduler jobs per the spec. Main cycle is parameterized by `MAIN_CYCLE_INTERVAL_MINUTES` (1–10, hot-reloadable). Implement dual settlement: `preliminary_settlement` at 15:55 ET (writes `preliminary_pnl`, does NOT reset profit_wallet) and `final_settlement` at 20:00 ET (writes `final_pnl`, `after_hours_pnl`, triggers capital state transitions). Include `regular_market_open` at 09:30 ET, `intraday_micro_cycle` every 1 minute, `moc_imbalance_scan` at 15:40–15:50 ET, `margin_minimizer` at 19:30 ET, `after_hours_transition` at 16:01 ET. Validate cycle interval in [1, 10] with error response."

---

### Phase 14 — FastAPI + WebSocket Engine & UI

**Deliverable:** `engine_api.py` (all REST endpoints), `websocket_manager.py` (all WebSocket events), `ui_server.py`, all 10 UI tabs with full functionality, Trade Replay modal, NLP status panel, System Topology graph, Dual Settlement widget, Target Override modal.

**Acceptance Criteria:**
- All REST endpoints return correct status codes and JSON schemas.
- WebSocket: `settlement_preliminary` event broadcasts at 15:55 ET with `{preliminary_pnl, starting_capital, pnl_pct, targets_met: [min, ideal, stretch]}`.
- `settlement_final` event broadcasts at 20:00 ET with full PnL breakdown.
- `daily_targets_set` event broadcasts at 09:28 ET with `DailyTargetConfig` serialized.
- UI Tab 1: Strategy override modal works; after submitting override, next cycle uses new targets.
- Cycle interval slider (Tab 2 and Tab 10): changing to "2" updates the engine and shows confirmation.
- System Health tab: NLP tier badge updates live when tier changes; red dot on strategy shows hover tooltip with resolution steps.
- Trade Replay modal: click closed trade → shows chart with entry/exit/NLP annotations.

**Prompt:** "Implement the FastAPI engine API and complete UI for AQTA v3. `engine/api/engine_api.py`: all REST endpoints from the spec including `/analytics/`, `/tax/`, `/backtest/`, `/system/`. `engine/api/websocket_manager.py`: all WebSocket events with proper serialization. `ui/ui_server.py`: serve SPA. `ui/static/`: full 10-tab SPA in Vanilla HTML5/JS/CSS using Chart.js, D3.js, and Lightweight Charts (all locally vendored). Include: Dual Settlement widget (Tab 1), Target Override modal (Tab 1), Cycle Interval slider (Tabs 2 and 10), Trade Replay modal (Tab 3), NLP Tier Usage chart (Tab 4), System Topology D3 graph (Tab 9), Strategy Health tooltips (Tab 2), all notification WebSocket events."

---

### Phase 15 — Backtest, Reporting & Final Integration

**Deliverable:** `Backtester`, `WalkForwardValidator`, `MonteCarloSimulator`, all report generators (daily HTML, weekly HTML, year-end HTML+PDF, Form 8949), Prometheus metrics, integration test suite, shadow mode end-to-end test.

**Acceptance Criteria:**
- `Backtester.run(strategy="B3", start="2022-01-01", end="2024-01-01")` completes in < 120 seconds. Returns Sharpe > 0 (B3 is a valid strategy).
- Walk-forward: IS Sharpe and OOS Sharpe both returned; `overfitting_score = OOS/IS` stored in `backtest_results`.
- NLP ablation: backtest with and without NLP returns different Sharpe values (NLP impact is nonzero).
- Monte Carlo (numba): 10,000 paths for a 10-position portfolio completes in < 10 seconds.
- Daily HTML report generated in < 5 seconds; contains all 9 sections.
- Prometheus metrics endpoint returns valid Prometheus text format.
- End-to-end shadow mode test: start engine in shadow mode; let it run one full main cycle (5 min); verify signals were generated, MockBroker received orders, `portfolio_tick` WebSocket events broadcast, no real orders submitted.
- All 15 phases integrated: full system starts from a clean database, completes first-run setup, connects brokers in mock mode, generates signals, runs preliminary and final settlement on a simulated day.

**Prompt:** "Implement the final integration layer for AQTA v3. `engine/backtest/backtester.py`: full historical replay with realistic fills, slippage model, commission model, survivorship bias control (sp500_membership_history.parquet), after-hours backtest support. `walk_forward.py`: rolling IS/OOS with Optuna hyperparameter tuning. `monte_carlo.py`: 10,000 paths with numba JIT. `performance_stats.py`: Sharpe, Sortino, Calmar, win rate, profit factor. Report generators: daily HTML, weekly HTML, year-end HTML+PDF, Form 8949 PDF. Prometheus metrics in `metrics.py`. Write an end-to-end integration test in `tests/integration/` that starts the engine in shadow mode, runs one full cycle, validates all outputs, and confirms no real broker calls were made."

---

## APPENDIX A: COMPLETE STRATEGY REFERENCE (160+ STRATEGIES)

| ID | Name | Family | Regime | NLP Req | Options Req | Flags Required |
|---|---|---|---|---|---|---|
| EQ-01 | Classic Trend Following | Momentum | BULL | No | No | — |
| EQ-05 | Trend Acceleration (SAR) | Momentum | BULL | No | No | — |
| EQ-06 | Sector Momentum 30m | Momentum | BULL/SIDEWAYS | No | No | — |
| EQ-07 | Relative Volume Surge | Momentum | ANY | No | No | — |
| EQ-08 | First Hour Continuation | Momentum | BULL | No | No | intraday |
| EQ-09 | Power Hour Sweep | Momentum | BULL | No | No | intraday |
| EQ-10 | Breadth Divergence | Momentum | BULL | No | No | intraday |
| A1 | Opening Range Breakout | Momentum | BULL | No | No | intraday |
| A2 | VWAP Momentum | Momentum | BULL | No | No | intraday |
| A3 | Gap-and-Go | Momentum | ANY | Optional | No | intraday |
| A4 | Relative Strength Rotation | Momentum | ANY | No | No | — |
| A5 | EMA Ribbon Expansion | Momentum | BULL | No | No | — |
| A6 | 52-Week High Breakout | Momentum | BULL | No | No | — |
| A7 | Unusual Volume (No News) | Momentum | ANY | No | No | — |
| A8 | VWAP MACD 1-min | Momentum | BULL | No | No | intraday |
| A9 | Opening Drive Momentum | Momentum | ANY | No | No | intraday |
| A10 | EOD Imbalance Fade | Momentum | ANY | No | No | intraday |
| A11 | T-WAP Trend Follow | Momentum | BULL | No | No | intraday |
| A12 | Pre-Market Catalyst Drift | Momentum | ANY | Tier2+ | No | after_hours |
| A13 | After-Hours Earnings Momo | Momentum | ANY | Tier2+ | No | after_hours |
| A14 | Multi-TF Confluence | Momentum | ANY | No | No | — |
| A15 | Key Level Reversal | MeanRev | ANY | No | No | — |
| A16 | News Catalyst (Rule-Based) | Momentum | ANY | No | No | — |
| A17 | Earnings Gap Continuation | Momentum | BULL | No | No | — |
| A18 | Dark Pool Accumulation | Momentum | ANY | No | No | dark_pool |
| EQ-03 | BB Mean Reversion | MeanRev | SIDEWAYS | No | No | — |
| B1 | BB Squeeze Breakout | MeanRev | SIDEWAYS | No | No | — |
| B2 | RSI Divergence | MeanRev | SIDEWAYS | No | No | — |
| B3 | Oversold Large-Cap Bounce | MeanRev | ANY | No | No | — |
| B4 | Intraday VWAP Deviation | MeanRev | ANY | No | No | intraday |
| B5 | Monday Gap Fade | MeanRev | ANY | No | No | intraday |
| B6 | Connors RSI Pullback | MeanRev | ANY | No | No | — |
| B7 | StdDev Channel Fade | MeanRev | SIDEWAYS | No | No | — |
| B8 | Volume Profile POC Rev | MeanRev | ANY | No | No | intraday |
| B9 | AH Liquidity Fade | MeanRev | ANY | No | No | after_hours |
| B10 | Overnight Gap Fade | MeanRev | ANY | No | No | intraday |
| B11 | Anchored VWAP Reversion | MeanRev | ANY | No | No | — |
| B12 | Multi-Day Oversold Accum | MeanRev | BULL/RECOVERY | No | No | — |
| B13 | Option-Implied Reversion | MeanRev | SIDEWAYS | No | Optional | options |
| B14 | High-Beta Reversion | MeanRev | SIDEWAYS_LOW | No | No | — |
| D1 | Congress Trade Replication | Sentiment | ANY | No | No | — |
| D2 | Insider Cluster Buy | Sentiment | ANY | No | No | — |
| D3 | SLM Sentiment (FinBERT) | Sentiment | ANY | Tier2 | No | — |
| D4 | WSB Reddit Momentum | Sentiment | ANY | No | No | — |
| D5 | Google Trends Catalyst | Sentiment | ANY | No | No | — |
| D6 | Dark Pool Flow | Sentiment | ANY | No | No | dark_pool |
| D7 | Institutional 13F Builder | Sentiment | ANY | No | No | — |
| D8 | StockTwits Cashtag Velocity | Sentiment | ANY | No | No | — |
| D9 | C-Suite Conviction Buy | Sentiment | ANY | No | No | — |
| D10 | Dark Pool Print Tracking | Sentiment | ANY | No | No | dark_pool |
| D11 | SLM News Flash (SNIPER) | Sentiment | ANY | Tier2 | No | — |
| D12 | Social Sentiment Divergence | Sentiment | ANY | Tier2+ | No | — |
| D13 | ETF Flow Signal | Sentiment | ANY | No | No | — |
| D14 | Earnings Whisper Gap | Sentiment | ANY | No | No | — |
| D15 | Institutional Block Trade | Sentiment | ANY | No | No | level2 |
| D16 | Supply Chain Contagion | Sentiment | ANY | Optional | No | — |
| EQ-02 | Stat Arb Pairs | Quant/Arb | SIDEWAYS | No | No | — |
| E1 | 3-Leg Cointegration | Quant/Arb | SIDEWAYS | No | No | — |
| E2 | Vol Regime Switching | Quant/Arb | ANY | No | Optional | — |
| E3 | Cross-Asset Corr Breakdown | Quant/Arb | ANY | No | No | — |
| E4 | ETF NAV Arb | Quant/Arb | ANY | No | No | — |
| E5 | 5-Factor Momentum | Quant/Arb | ANY | No | No | — |
| E6 | Lead-Lag Sector | Quant/Arb | BULL | No | No | — |
| E7 | S&P 500 Rebalance Arb | Quant/Arb | ANY | No | No | — |
| E8 | ETF Component Dispersion | Quant/Arb | ANY | No | No | — |
| E9 | Kalman Filter Price Est | Quant/Arb | ANY | No | No | — |
| E10 | Overnight Index Arb | Quant/Arb | ANY | No | No | after_hours |
| E11 | PCA Factor Breakout | Quant/Arb | ANY | No | No | — |
| E12 | Kalman Filter Pairs | Quant/Arb | SIDEWAYS | No | No | — |
| E13 | HMM State Transition Arb | Quant/Arb | TRANSITION | No | No | meta_brain |
| E14 | Vol Surface Arb (Skew) | Quant/Arb | ANY | No | Required | options |
| E15 | Correlation Regime Arb | Quant/Arb | TRANSITION | No | No | — |
| E16 | Multi-Asset Carry Harvest | Quant/Arb | ANY | No | No | — |
| F1 | Rate-Sensitive Rotation | Macro | ANY | No | No | macro |
| F2 | VIX Mean Reversion | Macro | ANY | No | No | macro |
| F3 | FOMC Calendar | Macro | ANY | No | No | macro |
| F4 | CPI/PPI Reaction | Macro | ANY | No | Optional | macro |
| F5 | Gold/Dollar Inverse | Macro | ANY | No | No | macro |
| F6 | Commodity-to-Equity | Macro | ANY | No | No | macro |
| F7 | Yield Curve Inversion Play | Macro | BEAR | No | No | macro |
| F8 | Energy Inventory Surprise | Macro | ANY | No | No | macro |
| F9 | Currency-Hedged Rotation | Macro | ANY | No | No | macro |
| F10 | Global Session Handoff | Macro | BULL | No | No | macro |
| F11 | Earnings Season Rotation | Macro | BULL | No | No | macro |
| F12 | Seasonal Macro Calendar | Macro | ANY | No | No | macro |
| F13 | Credit Spread Signal | Macro | ANY | No | No | macro |
| F14 | EM/DM Divergence | Macro | ANY | No | No | macro |
| F15 | Inflation Regime | Macro | ANY | No | No | macro |
| F16 | Central Bank Divergence | Macro | ANY | No | No | macro |
| F17 | Commodity Roll Yield | Macro | ANY | No | No | macro |
| F18 | Housing Data Sensitivity | Macro | ANY | No | No | macro |
| CM-01 | Money Market Sweep | Cash/Hedge | ANY | No | No | — |
| CM-02 | Static Hedge Ladder | Cash/Hedge | ANY | No | Optional | — |
| CM-03 | T-Bill Laddering | Cash/Hedge | ANY | No | No | — |
| CM-04 | Dividend Capture | Cash/Hedge | ANY | No | Optional | — |
| CM-05 | Margin Interest Minimizer | Cash/Hedge | ANY | No | No | — |
| CM-06 | T-Bill Ladder Optimizer | Cash/Hedge | ANY | No | No | — |
| CM-07 | Tail Risk Protection | Cash/Hedge | BEAR/CRASH | No | Optional | — |
| CM-08 | Correlation Breakdown Hedge | Cash/Hedge | ANY | No | No | — |
| CM-09 | Delta-Neutral Cash Park | Cash/Hedge | ANY | No | Required | options |
| CM-10 | Max Diversification Rebal | Cash/Hedge | ANY | No | No | — |
| CM-11 | Drawdown Circuit Breaker | Cash/Hedge | ANY | No | No | — |
| CM-12 | Margin Utilization Opt | Cash/Hedge | ANY | No | No | — |
| EQ-04 | Flash Crash Buy Ladder | Cash/Hedge | CRASH | No | No | — |
| EQ-05 | Tail Risk Convexity | Cash/Hedge | BULL | No | Required | options |
| OP-01 | 0DTE Iron Condor | Options | SIDEWAYS | No | Required | options |
| OP-02 | Vol Skew Arb | Options | ANY | No | Required | options |
| OP-03 | Covered Call Yield | Options | ANY | No | Required | options |
| OP-04 | Protective Put | Options | ANY | No | Required | options |
| OP-05 | LEAPS Bull Spread | Options | BULL | No | Required | options |
| OP-06 | Earnings IV Crush | Options | ANY | No | Required | options |
| OP-07 | Iron Butterfly | Options | SIDEWAYS | No | Required | options |
| OP-08 | Jade Lizard | Options | BULL | No | Required | options |
| OP-09 | Calendar Spread | Options | SIDEWAYS | No | Required | options |
| OP-10 | Diagonal Spread | Options | BULL | No | Required | options |
| OP-11 | Pre-Event Strangle | Options | ANY | No | Required | options |
| OP-12 | Short Gamma Scalping | Options | SIDEWAYS_LOW | No | Required | options |
| C4 | Cash-Secured Put | Options | ANY | No | Required | options |
| C6 | Poor Man's Covered Call | Options | BULL | No | Required | options |
| C7 | Ratio Spread | Options | BULL | No | Required | options |
| C8 | Protective Collar | Options | ANY | No | Required | options |
| C9 | Wheel Strategy | Options | ANY | No | Required | options |
| G1 | Leveraged ETF Trend | Leveraged | BULL ONLY | No | No | leveraged |
| G2 | Gamma Squeeze Detector | Leveraged | BULL | No | Optional | leveraged, options |
| G3 | Crypto Momentum Burst | Leveraged | ANY | No | No | crypto, leveraged |
| G4 | Short Vol Carry (SVXY) | Leveraged | ANY≠BEAR | No | No | leveraged |
| CO-01 | Gold & Oil + CoT | Commodities | ANY | No | No | macro |
| CO-02 | Commodity Roll Yield | Commodities | ANY | No | No | macro |
| VX-01 | VIX Term Structure | Volatility | ANY≠CRASH | No | No | — |
| VX-02 | Realized Vol Surface | Volatility | SIDEWAYS_LOW | No | Required | options |
| AL-01 | REIT Div Capture + MeanRev | Alternatives | ANY | No | Optional | — |
| AL-02 | SPAC NAV Arb | Alternatives | ANY | No | No | — |
| AL-03 | Convertible Bond Arb | Alternatives | ANY | No | Required | options |
| CR-01 | Crypto Trend (4H) | Crypto | ANY | No | No | crypto |
| CR-02 | CEX/DEX Arb | Crypto | ANY | No | No | crypto |
| CR-03 | Funding Rate Harvest | Crypto | ANY | No | No | crypto |
| CR-04 | On-Chain Whale Alert | Crypto | ANY | No | No | crypto |
| CR-05 | BTC Halving Cycle | Crypto | ANY | No | No | crypto |
| CR-06 | Crypto Fear & Greed | Crypto | ANY | No | No | crypto |
| CR-07 | DeFi Yield Capture | Crypto | ANY | No | No | crypto |
| FX-01 | G10 Carry | FX | ANY | No | No | — |
| FX-02 | Dollar Strength Overlay | FX | ANY | No | No | — |
| FX-03 | Currency Momentum | FX | ANY | No | No | — |
| FX-04 | Carry + Momentum Combo | FX | ANY | No | No | — |
| FX-05 | Vol-Adjusted Carry | FX | ANY | No | No | — |
| FI-01 | Duration Ladder T-Bills | Fixed Inc | ANY | No | No | — |
| FI-02 | Treasury Yield Momentum | Fixed Inc | ANY | No | No | — |
| FI-03 | TIPS Inflation Protection | Fixed Inc | ANY | No | No | — |
| FI-04 | Municipal Bond Spread | Fixed Inc | ANY | No | No | — |

**Total Unique Strategies: 163**

---

## APPENDIX B: KPI MONITORING REFERENCE

| KPI | Target | WARN Threshold | CRITICAL Threshold | Action |
|---|---|---|---|---|
| Daily PnL (final) | > ideal_target_usd | < 0 (loss day) | < −hard_halt_usd | RECOVERY_MODE / HARD_HALT |
| Intraday Drawdown | < 2% | 2% (soft halt) | 4% (hard halt) | Size reduction / halt |
| ATH Drawdown (rolling 90d) | < 8% | > 4% | > 8% | CM-11 ladder activates |
| Win Rate (90d) | > 55% | < 50% | < 40% | Strategy review |
| Sharpe (30d rolling) | > 3.0 | < 2.0 | < 1.0 | Regime check + retrain |
| Sortino (30d) | > 4.5 | < 3.0 | — | Review |
| Options Theta / Total PnL | > 30% | < 15% | — | Options allocation review |
| SOR Latency | < 5ms | > 20ms | > 100ms | Broker circuit check |
| Main Cycle Duration | < cycle_interval / 2 | > cycle_interval × 0.7 | > cycle_interval | Increase cycle interval |
| System Uptime | > 99.5% | < 98% | < 95% | NSSM restart check |
| NLP Tier 3 Rate | < 5% | > 30% | > 70% | SLM model health check |
| Portfolio Beta | 0.85–1.05 | > 1.3 or < 0.3 | > 1.5 | CM-03 hedge |
| Net Delta | ± 0.15×NAV | ±0.20×NAV | ±0.30×NAV | Delta hedge |
| Margin Utilization | < 75% | > 75% | > 90% | CM-12 de-lever |
| Avg Pairwise Correlation | < 0.30 | > 0.60 | > 0.85 | Step 13 block |
| Strategy Drawdown (any) | < 25% | 20% | 25% | Step 15 auto-halt |
| Compounding Streak | > 5 days | — | — | Scale up sizing |
| Recovery Progress | By day 5 | Not met day 3 | Not met day 5 | Capital Preservation |
| Overfitting Score (OOS/IS) | > 0.70 | < 0.50 | < 0.30 | Walk-forward review / auto-disable |
| Crypto Yield (DeFi + funding) | > 8% APY | < 5% | — | Protocol review |

---

## APPENDIX C: DEPENDENCIES & REQUIREMENTS

```txt
# Core Runtime
python>=3.11
fastapi==0.111.0
uvicorn==0.30.0
apscheduler==3.10.4
pydantic==2.7.4
sqlalchemy==2.0.30
aiohttp==3.9.5
aiofiles==23.2.1
websockets==12.0
httpx==0.27.0
tenacity==8.3.0
structlog==24.2.0
prometheus-client==0.20.0
pyotp==2.9.0
watchdog==4.0.1
psutil==5.9.8

# Data & Math
pandas==2.2.2
numpy==1.26.4
scipy==1.13.0
pandas-ta==0.3.14b0
pyarrow==16.0.0
duckdb>=0.10.0
numba==0.59.1

# ML & Quant
scikit-learn==1.5.0
hmmlearn==0.3.2
statsmodels==0.14.2
lightgbm==4.3.0
optuna==3.6.1
filterpy==1.4.5
arch==6.3.0
pyportfolioopt==1.5.5
riskfolio-lib>=5.0.0
cvxpy==1.5.1

# NLP — Tier 2 (SLM, default-on)
transformers==4.40.2
onnxruntime>=1.18.0
optimum[onnxruntime]>=1.20.0
sentence-transformers>=2.7.0

# NLP — Tier 3 (always-on fallback)
nltk==3.8.1
vaderSentiment==3.3.2

# NLP — Tier 1 (LLM, optional)
ollama==0.2.1
anthropic>=0.30.0
openai>=1.30.0

# Options
py_vollib_vectorized==0.1.2
QuantLib-Python==1.33

# Brokers & Market Data
schwab-py==1.2.0
robin_stocks==3.0.4
ib_insync==0.9.86
alpaca-trade-api==3.3.2
ccxt==4.3.19
web3==6.19.0
yfinance==0.2.38
polygon-api-client==1.14.2
finnhub-python==2.4.20
pytrends==4.9.2
praw==7.7.1
alpha_vantage==2.3.1
sec-edgar-downloader==5.0.2
fredapi==0.5.2
finvizfinance==0.14.7
nasdaqdatalink==1.0.4
beautifulsoup4==4.12.3

# Redis
redis==5.0.6
aioredis==2.0.1

# Testing & Dev
pytest==8.2.2
pytest-asyncio==0.23.7
hypothesis==6.100.0
mypy==1.10.0
ruff==0.4.7
```

---

*AQTA v3.0 — Definitive Local Infrastructure Edition*
*Total Pages (estimated): 85+ | Strategies: 163 | Implementation Phases: 15*
*All times Eastern (ET). All monetary values USD. Shadow mode default: ON.*
