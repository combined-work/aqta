# AQTA MASTER DOCUMENTATION
## Comprehensive Architecture & Implementation Guide (v2.0 – v3.0)

This document unifies the sequential updates and enhancements of the Autonomous Quantitative Trading Architecture (AQTA), combining the v2.0 Enterprise-Grade Blueprint, the v3.0 Ultimate Day-Trading Edition, and the complete end-to-end Copilot Agent Implementation Prompts into a single master reference.

---

# BOOK I: AQTA v2.0 ENTERPRISE-GRADE BLUEPRINT
*Enterprise-Grade AI Coding Agent Implementation Master Plan (All Asset Classes & Instruments)*

## 1. System Architecture Overview
AQTA v2.0 is a fully autonomous, multi-asset, multi-broker quantitative trading platform designed to maximise risk-adjusted returns across every investable instrument class. The system integrates machine learning, alternative data, real-time risk management, and multi-jurisdiction compliance into a single orchestrated Python stack.

### Core Metrics & Specifications
| Metric | Specification |
| :--- | :--- |
| **Python Version** | 3.11+ (asyncio-native) |
| **Target Sharpe Ratio** | > 3.0 annualised |
| **Max Drawdown Target** | < 8% portfolio-wide |
| **Strategy Coverage** | 15+ asset classes, 40+ signal types |
| **Execution Latency** | < 5ms smart-order routing |
| **Autonomous Cycle** | 24 / 7 / 365 — fully unattended |
| **Compliance Layers** | PDT, Wash-Sale, FINRA, MiFID II, SEC |

### Technology Stack Summary
| Layer | Component | Technology | Fallback / Alternative |
| :--- | :--- | :--- | :--- |
| **Language** | Python 3.11+ | — | — |
| **Async Runtime** | asyncio + aiohttp | trio | — |
| **ORM / DB** | SQLAlchemy 2.0 + PostgreSQL 16 | TimescaleDB (for tick data) | — |
| **Task Queue** | Celery 5 + Redis 7 | APScheduler | — |
| **API Framework** | FastAPI + Uvicorn | — | — |
| **Brokers** | Schwab, RH, IBKR, Alpaca, Coinbase | Interactive Brokers TWS direct | — |
| **Market Data** | Polygon.io (primary) | yfinance, Finnhub | — |
| **Alt Data** | SEC EDGAR, Glassnode, QuiverQuant | Benzinga, Apify | — |
| **LLM (local)** | Ollama (llama3.3 / mistral-large) | — | — |
| **LLM (cloud)** | Anthropic Claude API | OpenAI GPT-4o | — |
| **ML / Quant** | scikit-learn, hmmlearn, QuantLib | PyTorch, statsmodels | — |
| **Portfolio Opt.** | PyPortfolioOpt + Riskfolio-Lib | CVXPY | — |
| **Crypto** | CCXT + Web3.py | — | — |
| **Options Math** | py_vollib + mibian | QuantLib-Python | — |
| **Hyperparameter** | Optuna | Ray Tune | — |
| **Observability** | Prometheus + Grafana | CloudWatch | — |
| **Containerisation**| Docker + docker-compose | Kubernetes (future) | — |
| **Cloud / Storage** | AWS S3 + Lambda | MinIO (local dev) | — |
| **CI / CD** | GitHub Actions | GitLab CI | — |

## 2. Complete Strategy Arsenal — All Asset Classes
The following strategies are implemented across every major asset class. All inherit from BaseStrategy and are orchestrated by the Meta-Brain.

| Strategy ID | Asset Class | Technique | Expected Edge |
| :--- | :--- | :--- | :--- |
| **EQ-01** | US Equities | MovAvg Crossover + ADX filter | Trend momentum |
| **EQ-02** | US Equities | Pairs Stat-Arb (Z-score) | Mean-reversion spread |
| **EQ-03** | US Equities | Bollinger Band Squeeze + RSI | Range breakout |
| **EQ-04** | US Equities | Flash-Crash Limit Ladder (9:30 AM) | Dip liquidity premium |
| **EQ-05** | US Equities | Earnings Drift + LLM Sentiment | Post-announcement alpha |
| **EQ-06** | US Equities | Dark Pool Print Momentum | Informed-order flow |
| **EQ-07** | US Equities | Short-Interest Squeeze Monitor | Gamma-squeeze catalyst |
| **OP-01** | Options | 0DTE Iron Condor (SPX/SPY) | Theta decay on low-IV days |
| **OP-02** | Options | Volatility Skew Arb (VIX vs RV) | Implied vs realised gap |
| **OP-03** | Options | Covered Call Writing (holdings) | Yield enhancement |
| **OP-04** | Options | Protective Put — Portfolio Hedge | Tail-risk insurance |
| **OP-05** | Options | LEAPS Bull Spread (sector ETFs) | Leveraged directional |
| **OP-06** | Options | Calendar Spread (earnings crush) | IV collapse profit |
| **CR-01** | Crypto | BTC/ETH Trend via MACD + OBV | 24/7 trend following |
| **CR-02** | Crypto | Cross-Exchange Arb (CEX vs DEX) | Latency arbitrage |
| **CR-03** | Crypto | Funding Rate Harvest (perps) | Positive carry on longs |
| **CR-04** | Crypto | On-Chain Flow Analysis | Whale wallet signals |
| **CR-05** | Crypto | DeFi Yield Rotation (Aave/Curve) | Protocol yield optimiser |
| **FX-01** | Forex | G10 Carry Trade (high vs low yield) | Interest rate differential |
| **FX-02** | Forex | USD Index Mean Reversion | Dollar cycle arbitrage |
| **FX-03** | Macro | Rate Hike Anticipation (TIPS spread) | Bond vs equity rotation |
| **FI-01** | Fixed Income | Duration-adjusted Ladder | Yield curve positioning |
| **FI-02** | Fixed Income | Corp Bond Spread Widening | Credit spread alpha |
| **CO-01** | Commodities | Gold/Oil Momentum + CoT Report | Seasonal + positioning |
| **CO-02** | Commodities | Commodity Futures Roll Yield | Backwardation carry |
| **VX-01** | Volatility | VIX Futures Term Structure | Contango roll short |
| **VX-02** | Volatility | Realized Vol Surface Fitting | Delta-hedged gamma |
| **AL-01** | Real Estate | REIT Dividend Capture + Reversion | Income + momentum |
| **AL-02** | Alt | SPACs — NAV floor arbitrage | Merger premium harvest |
| **AL-03** | Alt | Convertible Bond Arb | Equity + debt mispricing |
| **CM-01** | Cash Mgmt | Money Market Sweep (SWVXX) | 3:50 PM yield on idle cash |
| **CM-02** | Cash Mgmt | T-Bill ladder rotation (13/26 wk) | Risk-free optimisation |

## 3. Implementation Phases (v2.0)

### PHASE 0: PROJECT INITIALIZATION & CORE INFRASTRUCTURE
**OBJECTIVE:** Bootstrap the enterprise repository, dependency management, containerisation, and CI/CD pipeline.

*   **Step 0.1 — Repository & Directory Structure**
    *   Initialise Git with signed commits; enforce branch protection on `main`.
    *   Directory layout: `/api`, `/core`, `/strategies`, `/data`, `/models`, `/utils`, `/tests`, `/infra`, `/notebooks`, `/migrations`
    *   Add `.gitignore` excluding all `.env`, `*.key`, `*.pem`, `__pycache__`, `*.parquet` files.
*   **Step 0.2 — Dependency Management (pyproject.toml)**
    *   Core: `pandas`, `numpy`, `scipy`, `statsmodels`, `ta-lib`, `scikit-learn`, `hmmlearn`
    *   Async I/O: `aiohttp`, `asyncio`, `aiofiles`, `websockets`
    *   Brokers & Data: `yfinance`, `ccxt`, `polygon-api-client`, `alpaca-trade-api`, `ib_insync`
    *   DB & Queue: `sqlalchemy[asyncio]`, `asyncpg`, `psycopg2-binary`, `celery[redis]`, `redis`
    *   API: `fastapi`, `uvicorn[standard]`, `pydantic-settings`, `websockets`
    *   LLM: `ollama`, `anthropic`, `openai` (fallback), `langchain`
    *   Options: `py_vollib`, `mibian`, `QuantLib-Python`
    *   Crypto: `ccxt`, `web3`, `eth-account`
    *   ML/Quant: `pytorch`, `optuna`, `pyportfolioopt`, `riskfolio-lib`, `cvxpy`
    *   Compliance: `mypy`, `ruff`, `pytest`, `pytest-asyncio`, `hypothesis`
*   **Step 0.3 — Environment Variables (.env.example)**
    *   `SCHWAB_API_KEY=`, `SCHWAB_SECRET=`, `SCHWAB_ACCOUNT_ID=`
    *   `ROBINHOOD_USER=`, `ROBINHOOD_PASS=`, `ROBINHOOD_TOTP_SECRET=`
    *   `IBKR_HOST=127.0.0.1`, `IBKR_PORT=7497`, `IBKR_CLIENT_ID=`
    *   `ALPACA_KEY=`, `ALPACA_SECRET=`, `ALPACA_BASE_URL=`
    *   `COINBASE_ADV_KEY=`, `COINBASE_ADV_SECRET=`
    *   `POLYGON_KEY=`, `FINNHUB_KEY=`, `FRED_KEY=`, `EDGAR_USER_AGENT=`
    *   `TELEGRAM_BOT_TOKEN=`, `TELEGRAM_CHAT_ID=`, `PAGERDUTY_KEY=`
    *   `DB_URL=`, `REDIS_URL=`, `S3_BUCKET=`, `AWS_ACCESS_KEY=`, `AWS_SECRET_KEY=`
    *   `ENCRYPTION_KEY=`, `MASTER_KILLSWITCH_PIN=`
    *   `IS_LIVE=false`, `MAX_PORTFOLIO_RISK_PCT=0.02`, `PDT_BUFFER=26500`
*   **Step 0.4 — Dockerization**
    *   `docker-compose.yml`: PostgreSQL 16, Redis 7, Grafana, Prometheus
    *   Separate Dockerfile for API, Celery Worker, and Beat Scheduler
    *   GitHub Actions CI: lint → mypy → pytest → build Docker image → push to ECR
    *   Secrets managed via AWS Secrets Manager or HashiCorp Vault; NEVER in env files in production
*   **Step 0.5 — Observability Stack (NEW)**
    *   Prometheus metrics endpoint on `/metrics` via `prometheus-fastapi-instrumentator`
    *   Grafana dashboards: PnL curve, position heat-map, latency percentiles, error rates
    *   Structured JSON logging via `structlog`; shipped to CloudWatch or ELK stack
    *   PagerDuty alert: triggered if drawdown > 5% intraday or any unhandled exception in live mode
> **✔ ACCEPTANCE CRITERIA:** docker-compose up -d succeeds; all services healthy; Prometheus scrapes metrics; pytest passes.

### PHASE 1: DATABASE SCHEMA & STATE MANAGEMENT
**OBJECTIVE:** Build the full ORM layer — trading, tax, ML features, audit trail, and multi-asset positions.

*   **Step 1.1 — Core Trading Tables**
    *   **Trade:** `id, symbol, asset_class, broker, strategy_id, qty, buy_price, sell_price, status, order_type, fill_time, slippage_bps, commission, timestamp`
    *   **Position:** `symbol, asset_class, broker, current_qty, average_cost, unrealized_pl, realized_pl, days_held, strategy_used, last_updated, delta, theta, vega` (options-aware)
    *   **Order:** `id, parent_trade_id, broker_order_id, status, fills_json, routing_reason, latency_ms`
*   **Step 1.2 — Tax & Compliance Tables**
    *   **WashSaleBlacklist:** `symbol, loss_realized_date, expiration_date, loss_amount, proxy_used`
    *   **TaxLot:** `id, symbol, acquisition_date, qty, cost_basis, lot_method (FIFO/HIFO/LIFO), stcg_ltcg_flag`
    *   **TaxHarvestLog:** `date, symbol_sold, proxy_bought, loss_captured, estimated_tax_saving`
    *   **ComplianceAudit:** Every risk block logged: `timestamp, rule_triggered, order_id, reason`
*   **Step 1.3 — Intelligence & ML Tables**
    *   **StrategyPerformance:** `strategy_id, win_rate, total_pnl, avg_holding_period, sharpe, max_dd, current_weight, regime_context`
    *   **MarketRegimeLog:** `date, hmm_state, vix_level, sp500_trend, macro_score, llm_sentiment_avg`
    *   **FeatureStore:** `symbol, date, rsi, macd, atr, vix, sentiment_score, dark_pool_vol, funding_rate, on_chain_flow, parquet_path`
    *   **AlphaSignalLog:** `signal_id, strategy_id, symbol, generated_at, strength_score, acted_on, outcome_pnl`
*   **Step 1.4 — Options & Derivatives Tables (NEW)**
    *   **OptionsPosition:** `id, underlying, expiry, strike, option_type, qty, premium_paid, delta, gamma, theta, vega, iv, days_to_expiry`
    *   **GreeksSnapshot:** Hourly Greeks snapshots for all open options; feeds real-time P&L dashboard
*   **Step 1.5 — Crypto & DeFi Tables (NEW)**
    *   **CryptoPosition:** `token, network, wallet_address, qty, avg_cost, protocol_staked, apy, last_harvest`
    *   **FundingRateLog:** `symbol, exchange, rate, timestamp`
> **✔ ACCEPTANCE CRITERIA:** Alembic `upgrade head` completes error-free; all 15 tables confirmed in pgAdmin; FK constraints pass.

### PHASE 2: BROKER API & DATA INGESTION ENGINE
**OBJECTIVE:** Standardise all external API access behind ABCs; build async multi-source data pipelines.

*   **Step 2.1 — The Universal Broker Interface**
    *   Abstract class `BaseBroker`: `get_quote(), submit_order(), cancel_order(), get_positions(), get_balances(), get_option_chain(), request_ach_transfer(), get_order_history()`
    *   Circuit-breaker decorator: auto-pause broker if >3 consecutive API errors in 60 seconds
    *   Retry policy: exponential back-off (1s, 2s, 4s) with jitter, max 5 retries
*   **Step 2.2 — Broker Implementations**
    *   **SchwabBroker:** OAuth2 PKCE flow, token auto-refresh, options chain, streaming quotes via WebSocket
    *   **RobinhoodBroker:** 2FA/TOTP support, fractional shares, 24/5 extended hours, crypto routing
    *   **IBKRBroker (NEW):** ib_insync integration; direct market access for equities, futures, FX, options; TWS API
    *   **AlpacaBroker (NEW):** Paper + live mode; crypto; market data; portfolio margin
    *   **CoinbaseBroker (NEW):** Advanced Trade API; spot, perpetuals; on-chain withdrawal support
    *   **MockBroker:** In-memory virtual broker for Shadow Mode; emulates fills with realistic slippage model
*   **Step 2.3 — Data Ingestion Engine (Multi-Source Async)**
    *   Historical OHLCV: `yfinance` (fallback), `polygon.io` (primary — tick-level, 15yr history)
    *   Real-time quotes: Finnhub WebSocket; Polygon WebSocket; crypto via CCXT streaming
    *   Options chain: Polygon Options API + CBOE CFE feed; IV surface construction
    *   Macro data: FRED API (rates, CPI, unemployment), OECD, World Bank
    *   Alternative data: SEC EDGAR (10-K/10-Q), news NLP (NewsAPI + Benzinga), social sentiment (Reddit WSB, Twitter/X via apify)
    *   On-chain data (NEW): Glassnode API (BTC/ETH flows, miner data, exchange netflows)
    *   Dark pool prints (NEW): Placeholder `data/dark_pools.py`; integrates FlowAlgo or CheddarFlow REST API
    *   Economic calendar (NEW): Scrape Investing.com / ForexFactory for earnings, CPI, FOMC events
    *   Short interest (NEW): Fintel API — daily short interest ratio, days-to-cover
    *   Congressional trades (NEW): QuiverQuant API — track Congress members' stock disclosures
*   **Step 2.4 — Real-Time Data Normalisation**
    *   All incoming quotes normalised to `QuoteEvent` dataclass: `symbol, price, bid, ask, volume, timestamp_ns, source`
    *   Async fan-out: each `QuoteEvent` pushed to Redis pub/sub; all strategies subscribe to relevant channels
    *   Websocket reconnect watchdog: automatically re-subscribes after any disconnect
*   **Step 2.5 — Token Refresh & Auth Daemon**
    *   Celery beat task every 20 min: refresh Schwab OAuth2, IBKR session, Alpaca JWT
    *   Encrypted storage of all tokens in PostgreSQL `auth_tokens` table (Fernet AES-128)
> **✔ ACCEPTANCE CRITERIA:** All 5 broker mock_submit_order and get_quote calls succeed; quote fan-out reaches Redis in <2ms.

### PHASE 3: RISK MANAGEMENT & TAX OPTIMIZATION ENGINE
**OBJECTIVE:** Multi-layer pre-trade, intraday, and post-trade risk framework; advanced tax harvesting.

*   **Step 3.1 — Pre-Trade Risk Checks (ordered pipeline)**
    *   `check_pdt_buffer(account_value)`: reject if equity would drop < $26,500 post-trade
    *   `check_wash_sale(symbol)`: query WashSaleBlacklist, offer auto proxy-swap
    *   `check_position_limit(symbol)`: reject if single-name > 10% of portfolio NAV
    *   `check_portfolio_correlation(symbol)`: reject if Pearson r > 0.75 with existing holdings
    *   `check_sector_concentration()`: reject if any GICS sector > 35% of NAV
    *   `check_liquidity(symbol, qty)`: reject if order > 5% of 20-day ADTV (average daily trading volume)
    *   `check_iv_crush_risk(option)`: warn if earnings within 5 days and long vega exposure > threshold
    *   `check_leverage_ratio()`: reject if portfolio notional > 4x NAV (Reg-T aware)
    *   `check_crypto_position_limit()`: crypto capped at configurable % of NAV (default 15%)
*   **Step 3.2 — Real-Time Risk Monitoring**
    *   Intraday PnL breaker: if portfolio drawdown exceeds 2% intraday → halt new entries
    *   Greeks dashboard: real-time net delta, gamma, theta, vega across all options positions
    *   VaR / CVaR engine: daily 99% Value-at-Risk calculated via Monte Carlo (10,000 paths)
    *   Stress-test scenarios: 2008, 2020-COVID, 2022-rate-shock — run nightly on current portfolio
    *   Correlation matrix live update: recalculated every 5 minutes during market hours
*   **Step 3.3 — Post-Trade Risk**
    *   ATR trailing stops: 14-day ATR; stop = current_price − (2 × ATR); updated daily
    *   Time-based exits: any position open > configurable max_hold_days triggers review
    *   Profit-lock mechanism: once position +20%, stop rises to +10% (ratchet stop)
*   **Step 3.4 — Tax Optimization (Advanced)**
    *   Lot-level tracking: FIFO / HIFO / LIFO selectable per strategy at order time
    *   Tax-loss harvesting (TLH) engine: scans all positions at 4:15 PM for unrealised losses > $500
    *   Proxy swap dictionary: SPY↔VOO, QQQ↔VGT, AMD↔NVDA, BTC↔ETH, GLD↔IAU — maintains market exposure
    *   STCG vs LTCG optimiser: prioritises selling positions past 365-day mark to qualify for long-term rate
    *   Year-end tax projection: estimates capital gains liability in November; suggests harvest candidates
    *   Estimated tax saving logged per harvest: `loss_captured × estimated_marginal_rate`
*   **Step 3.5 — Compliance Engine (NEW)**
    *   FINRA PDT rule: tracks day-trades per 5-day rolling window; blocks 4th trade if <$25k account
    *   Reg SHO locate check: placeholder for short-sale locate confirmation with prime broker
    *   MiFID II best-execution log: every order records all venue quotes considered before routing
    *   Insider trading guardrail: cross-reference LLM-extracted SEC 8-K material events; block trading in affected tickers for 72h
> **✔ ACCEPTANCE CRITERIA:** Wash-sale blocked; PDT blocked correctly; TLH harvest triggers; CVaR report generated without error.

### PHASE 4: THE STRATEGY ARSENAL — ALL INSTRUMENTS
**OBJECTIVE:** Implement all 30+ strategies spanning equities, options, crypto, FX, fixed income, and commodities.

*   **Step 4.1 — Strategy Base Class & Signal Framework**
    *   `BaseStrategy(ABC)`: `generate_signals(df) → SignalEvent`, `calculate_position_size() → float`, `on_fill(trade)`, `on_stop_triggered(trade)`
    *   `SignalEvent` dataclass: `symbol, direction (BUY/SELL/HOLD), strength (0–1), conviction, recommended_size, stop_price, take_profit, metadata_dict`
    *   Position sizing: Kelly Criterion (fractional, capped at 0.25f) as default; override per strategy
*   **Step 4.2 — Equity Strategies (EQ-01 to EQ-07)**
    *   EQ-01 MovAvg Crossover: 9/21/50 EMA + ADX > 25 confirmation; long-only in BULL regime
    *   EQ-02 Stat-Arb Pairs: cointegration test (Engle-Granger p<0.05); Z-score entry > ±2σ, exit at 0
    *   EQ-03 Bollinger + RSI: band squeeze detection (BW < 6-month low); RSI divergence filter
    *   EQ-04 Flash Crash: ladder of 5 limit orders at 5%, 10%, 15%, 20%, 25% below prior close; placed 9:28 AM
    *   EQ-05 Earnings Drift: enter pre-announcement +3 days; LLM sentiment > 65; exit T+5
    *   EQ-06 Dark Pool: monitor large off-exchange prints > $5M; direction bias within 30 min
    *   EQ-07 Short Squeeze: SI/float > 20%, DTC > 5, momentum confirmation; sized via option gamma exposure
*   **Step 4.3 — Options Strategies (OP-01 to OP-06) (NEW)**
    *   OP-01 0DTE Iron Condor: SPX daily; entry when VIX < 18 and IV percentile > 50; 16Δ wings; auto-manage at 50% profit or 200% loss
    *   OP-02 Vol Skew Arb: buy cheap skew (low put/call IV ratio); hedge with VIX futures; target IV normalisation
    *   OP-03 Covered Call: write 30DTE 0.30Δ calls on core long equity holdings; roll at 21 DTE
    *   OP-04 Protective Put: buy 90DTE 0.10Δ puts on SPY as portfolio insurance; size = 2% NAV/year
    *   OP-05 LEAPS Spread: 12-month bull call spread on sector ETF leaders; targets 3:1 reward/risk
    *   OP-06 Calendar Spread: sell near-month, buy far-month around earnings; profit from IV crush
*   **Step 4.4 — Crypto Strategies (CR-01 to CR-05) (NEW)**
    *   CR-01 BTC/ETH Trend: 4H MACD histogram + OBV divergence; route to Coinbase or Alpaca Crypto
    *   CR-02 CEX/DEX Arb: compare Coinbase spot vs Uniswap V3 pool price; execute via Web3 if spread > 0.3%
    *   CR-03 Funding Rate Harvest: hold long BTC when perp funding rate > 0.01%/8h on Bybit (via CCXT)
    *   CR-04 On-Chain Whale Alert: Glassnode exchange outflow > 3σ spike → bullish long signal within 48h
    *   CR-05 DeFi Yield: rotate idle USDC between Aave, Compound, Curve pools targeting highest net APY
*   **Step 4.5 — FX, Fixed Income, Commodity Strategies (NEW)**
    *   FX-01 G10 Carry: long AUD/USD + NZD/USD vs short USD/JPY + CHF; rebalance weekly on rate differential
    *   FX-02 DXY Mean-Rev: USD Index deviation from 50-day MA > 2.5%; fade with EUR/USD + GBP/USD basket
    *   FI-01 Duration Ladder: T-bill 4-week + 3-month + 6-month rotation; hold to maturity for risk-free yield
    *   CO-01 Gold Momentum: buy GLD if 20d MA > 50d MA and CFTC net non-commercial position > 200k contracts
    *   VX-01 VIX Futures Short: short VIX near-month futures when term structure in contango > 5%; target roll yield
*   **Step 4.6 — Cash Management (CM-01, CM-02)**
    *   CM-01 Money Market Sweep: idle cash > $500 at 3:50 PM → buy SWVXX (Schwab) or VMFXX (Vanguard)
    *   CM-02 T-Bill Ladder: allocate 20% of 'safe reserves' to 4/13/26-week T-bills; autoroll at maturity
> **✔ ACCEPTANCE CRITERIA:** Every strategy ingests mock DataFrame and returns valid SignalEvent; Kelly sizing test passes; options Greeks computed correctly.

### PHASE 5: THE META-BRAIN — AUTONOMOUS INTELLIGENCE CORE
**OBJECTIVE:** Central AI orchestration: regime detection, dynamic allocation, multi-LLM analysis, adaptive learning.

*   **Step 5.1 — Market Regime Detection (HMM v2)**
    *   HMM trained on: SPY returns, VIX level, 10Y-2Y yield spread, put/call ratio, AAII sentiment, credit spreads
    *   6-state model: BULL_TREND, BEAR_TREND, SIDEWAYS_LOW_VOL, SIDEWAYS_HIGH_VOL, CRASH_RISK, RECOVERY
    *   Regime probabilities used as strategy weight multipliers — not binary on/off
    *   Regime transitions trigger Telegram alert with probability distribution summary
*   **Step 5.2 — Multi-Armed Bandit Capital Allocator**
    *   Thompson Sampling: posterior Beta(α, β) updated after each trade; win → α+1, loss → β+1
    *   Outputs `AllocationDict`: per-strategy weight sum = 1.0; minimum 5% floor per active strategy
    *   Regime-conditional allocation: Bandit weights multiplied by regime suitability matrix
    *   Explainability log: every reallocation records reasoning for compliance audit
*   **Step 5.3 — Multi-LLM Analyst Ensemble (NEW)**
    *   Primary: Ollama (local) with llama3.3 or mistral-large for SEC filings, earnings calls, news
    *   Fallback: Anthropic Claude API — used for complex multi-document synthesis
    *   Prompt templates: earnings call transcript → `{sentiment_score, surprise_factors, guidance_revision}` JSON
    *   Prompt templates: SEC 10-K → `{risk_factors_delta, revenue_quality, management_tone}` JSON
    *   Prompt templates: macro news → `{asset_impact_map, timeline_estimate, confidence}` JSON
    *   Ensemble voting: if local LLM and cloud LLM disagree by > 30 points, abstain from trade
    *   EDGAR filing fetcher: async downloads latest 10-K, 10-Q, 8-K via SEC EDGAR full-text search API
*   **Step 5.4 — Correlation & Portfolio Optimizer (NEW)**
    *   Pearson correlation matrix recalculated every 5 min on live P&L stream; reject if r > 0.75
    *   PyPortfolioOpt: Black-Litterman model for weekly portfolio rebalancing; views injected from LLM analyst scores
    *   Riskfolio-Lib: CVaR-constrained mean-variance frontier; efficient frontier visualised in dashboard
    *   Max diversification: daily check that no factor (momentum, value, quality) dominates > 50% of variance
*   **Step 5.5 — Adaptive Strategy Evolution (NEW)**
    *   Optuna hyperparameter tuner: runs nightly on last 90 days of trade data; tunes MA periods, Z-score thresholds, ATR multipliers
    *   Walk-forward validation: each strategy re-validated on 30-day out-of-sample window before live update
    *   Strategy retirement: any strategy with 90-day Sharpe < 0.5 is auto-disabled and flagged for review
    *   A/B testing framework: shadow-run new parameter sets alongside live; promote if Sharpe improves > 0.3
*   **Step 5.6 — Alternative Data Intelligence (NEW)**
    *   Congressional trades monitor: QuiverQuant API; if senator buys sector ETF → add 10% weight to that sector
    *   Insider filing tracker: SEC Form 4 scraper; cluster buys by multiple insiders → bullish signal
    *   Google Trends: weekly search volume for target companies; spike detection for retail attention
    *   Satellite data placeholder: `data/satellite.py` for future Planet Labs / Orbital Insight integration (parking lots, shipping traffic)
> **✔ ACCEPTANCE CRITERIA:** Meta-Brain outputs AllocationDict from mock regime data; LLM sentiment returns valid JSON; Optuna trial completes one cycle.

### PHASE 6: EXECUTION ENGINE & SMART ORDER ROUTING v2
**OBJECTIVE:** Intelligent multi-broker routing with latency optimisation, smart sizing, and execution analytics.

*   **Step 6.1 — Smart Order Router Logic**
    *   Rule 1 (Time): Pre/post-market outside 9:30–16:00 ET → RobinhoodBroker or AlpacaBroker
    *   Rule 2 (Crypto): Any crypto asset → CoinbaseBroker (spot) or Alpaca (24/7)
    *   Rule 3 (Options): All options orders → SchwabBroker or IBKRBroker (if leg count > 2)
    *   Rule 4 (Size): Order > $100k notional → IBKRBroker (DMA, lower commission)
    *   Rule 5 (Fractional): Qty < 1 share → RobinhoodBroker
    *   Rule 6 (Futures/FX): Commodity futures or forex → IBKRBroker
    *   Rule 7 (Best Price): For equities matching multiple rules → query all eligible brokers for quote; route to best bid/ask
*   **Step 6.2 — Order Types & Execution Algorithms (NEW)**
    *   TWAP: split large orders into time-weighted slices over configurable window
    *   VWAP: slice order per 5-min volume histogram to minimise market impact
    *   Iceberg: show only 10% of order size; auto-refill as fills arrive
    *   Trailing Stop: broker-native where supported; software fallback via quote monitor
    *   OCO (One-Cancels-Other): take-profit + stop-loss bracket on every new entry
*   **Step 6.3 — Execution Analytics**
    *   Slippage tracking: record `(fill_price - signal_price) / signal_price × 10000` bps per trade
    *   Market impact model: log pre/post-trade mid-price; estimate permanent vs temporary impact
    *   Commission optimiser: quarterly review of per-broker commission schedule; auto-switch default if savings > $200/month
> **✔ ACCEPTANCE CRITERIA:** Overnight trade → Robinhood; options leg → Schwab/IBKR; crypto → Coinbase; TWAP execution verified with mock fills.

### PHASE 7: AUTONOMOUS DAILY CYCLE & EVENT AUTOMATION
**OBJECTIVE:** Full 24-hour Celery-orchestrated pipeline covering every market session and timezone.

*   **Step 7.1 — Pre-Market (04:00 AM ET)**
    *   Refresh all broker OAuth tokens; validate balances
    *   Download overnight macro events (FRED, economic calendar)
    *   Fetch SEC filings published overnight; run LLM analysis queue
    *   Place Flash Crash limit ladders for watchlist symbols
    *   Generate morning regime report via HMM; push to Telegram
*   **Step 7.2 — Pre-Open Preparation (09:00 AM ET)**
    *   Run Optuna overnight tuning results; apply any promoted parameter updates
    *   Calculate opening gap signals; pre-position for gap-fill mean-reversion
    *   Set OCO brackets on all overnight positions
*   **Step 7.3 — Market Hours Loop (09:30 AM – 04:00 PM ET, every 5 min)**
    *   Meta-Brain cycle: update regime → update allocation → scan signals → risk-check → execute
    *   Real-time Greeks update for all options positions
    *   Correlation matrix refresh; block correlated signals automatically
    *   Intraday drawdown check: if portfolio -2% → pause new entries; if -4% → close all day-trades
    *   0DTE options management: at 3:00 PM, close any 0DTE position at market to avoid pin risk
*   **Step 7.4 — After-Hours (04:15 PM ET)**
    *   TLH scan: evaluate all unrealised losses > $500 for harvest viability
    *   Execute proxy swaps for approved harvests
    *   Update ATR trailing stops on all open positions
    *   Run VaR and CVaR calculation; store in MarketRegimeLog
    *   Money-market sweep: uninvested cash → SWVXX
*   **Step 7.5 — Crypto After-Hours (05:00 PM – 09:00 AM ET, every 15 min)**
    *   Run CR-01 trend strategy on 4H BTC/ETH candles
    *   Monitor funding rates; harvest if positive
    *   DeFi yield check: compare current protocol APY vs alternatives; rotate if delta > 1%
*   **Step 7.6 — Nightly Jobs (11:00 PM ET)**
    *   Profit sweep: if total_equity > 30,000 → ACH transfer excess settled cash
    *   Run Optuna tuning overnight on last 90-day trade history
    *   Backup PostgreSQL → S3 encrypted snapshot
    *   Generate daily performance report (HTML + PDF); email to owner
    *   Update ML Feature Store: append today's features to Parquet files
*   **Step 7.7 — Weekend (Saturday 08:00 AM ET)**
    *   Full portfolio review: PnL attribution by strategy, sector, broker
    *   Rebalance portfolio to target weights using Black-Litterman output
    *   Update congressional trade signals from QuiverQuant weekly data
    *   Run stress-test suite; adjust protective put sizing if needed
> **✔ ACCEPTANCE CRITERIA:** All Celery beat schedules configured; task dependency chain verified; no race conditions in concurrent strategy execution.

### PHASE 8: REPORTING, DASHBOARD & INVESTOR INTERFACE
**OBJECTIVE:** Real-time portfolio visibility, performance attribution, and autonomous reporting.

*   **Step 8.1 — FastAPI Backend**
    *   REST endpoints: `/portfolio`, `/positions`, `/trades`, `/performance`, `/risk`, `/signals`, `/regime`
    *   WebSocket endpoint `/ws/live`: streams real-time PnL ticks, regime updates, signal alerts
    *   Authentication: JWT with RS256; rate-limited at 100 req/min
*   **Step 8.2 — Dashboard**
    *   Equity curve chart with benchmark comparison (SPY, BTC)
    *   Heat-map: sector exposure, factor loading, correlation matrix
    *   Live Greeks panel: net delta, gamma, theta, vega, charm
    *   Tax projection widget: STCG/LTCG estimate, YTD harvest savings
    *   Strategy performance table: per-strategy Sharpe, win rate, avg hold, current weight
*   **Step 8.3 — Automated Reporting**
    *   Daily HTML report: trade log, PnL, risk metrics — emailed at midnight
    *   Monthly PDF: full performance attribution, Sharpe breakdown, tax summary
    *   Telegram alerts: new signal executed, stop triggered, drawdown warning, regime change
> **✔ ACCEPTANCE CRITERIA:** Dashboard loads; WebSocket streams live PnL; daily email report delivered; Telegram alert fires on mock drawdown.

### PHASE 9: SHADOW MODE, DISASTER RECOVERY & ENTERPRISE HARDENING
**OBJECTIVE:** Production-grade resilience, cloud failover, and 30-day paper-trading validation.

*   **Step 9.1 — Shadow Mode (Paper Trading Sandbox)**
    *   `is_live` flag on BaseStrategy; routes all execution to MockBroker
    *   MockBroker: realistic fill model — mid-price ± configurable slippage; partial fills probabilistically modelled
    *   Shadow portfolio tracks virtual NAV alongside live account for side-by-side Sharpe comparison
    *   Auto-promote: if shadow Sharpe > live Sharpe by 0.5 for 30 days → Telegram confirmation prompt before going live
*   **Step 9.2 — Cloud Failover (AWS Lambda Watchdog)**
    *   FastAPI `/heartbeat` endpoint returns `{status: ok, timestamp, drawdown_pct}`
    *   Lambda pings every 60 seconds; if 5 consecutive failures → trigger emergency liquidation
    *   Emergency liquidation: market-sell all equity day-trades via Schwab API directly
    *   SNS alert to owner: SMS + email with liquidation report
*   **Step 9.3 — Master Kill-Switch**
    *   POST `/killswitch?pin=MASTER_KILLSWITCH_PIN` → immediately halts all Celery tasks
    *   Sets `trading_enabled = False` flag in Redis; all execution checks this flag first
    *   Graceful shutdown: cancels all open limit orders; closes 0DTE options at market
*   **Step 9.4 — Security Hardening**
    *   All secrets encrypted at rest with Fernet AES-128 in database; never in plaintext .env in production
    *   API key rotation reminders: automated 90-day expiry alert via Telegram
    *   Database connection pooled with SSL (`?sslmode=require`); Redis TLS enabled
    *   Docker containers run as non-root user; read-only filesystem where possible
    *   Dependency audit: `pip-audit` and `safety check` run in CI on every PR
*   **Step 9.5 — ML Feature Store & Future Deep Learning**
    *   Nightly Parquet append: VIX, RSI, MACD, sentiment_score, dark_pool_vol, funding_rate, on_chain_flow, regime_state, strategy_pnl
    *   S3-compatible storage (local MinIO in dev; AWS S3 in prod)
    *   Placeholder `models/deep_rl_agent.py` for future PPO reinforcement learning agent trained on Feature Store
*   **Step 9.6 — Regulatory & Tax Filing Assist (NEW)**
    *   Year-end Form 8949 generator: exports all closed lots in IRS-compatible CSV
    *   Broker reconciliation: cross-check database trade log vs broker 1099-B PDF; flag discrepancies
    *   Estimated quarterly tax payment calculator: projects liability in March, June, September, December
> **✔ ACCEPTANCE CRITERIA:** Full codebase: mypy 0 errors, ruff 0 warnings, pytest >95% coverage; 30-day shadow Sharpe > 1.5; killswitch verified; Lambda failover tested.

### Target KPIs & Performance Benchmarks
| KPI | Target | Measurement Frequency |
| :--- | :--- | :--- |
| **Annualised Sharpe Ratio** | > 3.0 | Monthly rolling |
| **Maximum Drawdown** | < 8% | Real-time intraday |
| **Win Rate (all strategies)** | > 55% | Rolling 90-day |
| **Average Hold Period** | 2 – 15 days (equities) | Per trade |
| **Options P&L (theta decay)** | > 30% of total P&L | Monthly |
| **Tax-Loss Harvested (annual)** | > $5,000 | Yearly |
| **Execution Slippage** | < 3 bps average | Per trade |
| **System Uptime** | > 99.5% | Monthly |
| **Order Latency (SOR)** | < 5ms | Real-time |
| **Crypto Yield (DeFi + funding)** | > 8% APY on crypto allocation | Monthly |
| **Daily Reporting** | Delivered by 12:01 AM | Daily |
| **Emergency Failover Trigger** | < 5 min to full liquidation | Quarterly test |

---

# BOOK II: AQTA v3.0 ULTIMATE DAY-TRADING EDITION
*Maximum Daily Profit, Zero-Loss Protocol, Tax-Aware (Local Windows Architecture)*

> **CLASSIFICATION:** Technical System Design & Copilot Agent Prompt
> **Capital Base:** $10,000+ per cycle | **Goal:** Maximum daily profit extraction
> **Platform:** Windows Local Machine | **Brokers:** Robinhood + Schwab (free tier only)
> **Philosophy:** Every dollar should work. Every day should profit. Every loss should recover.

## PART I — SYSTEM PHILOSOPHY & CAPITAL FRAMEWORK

### The Core Operating Doctrine

```
DAILY CYCLE GOAL:
  Morning:  Deploy $10,000+ across highest-probability setups
  Intraday: Monitor, adjust, protect, compound
  Evening:  Extract profit above $10,000 floor
  Night:    Reset, analyse, prepare next day's playbook

ZERO-LOSS PROTOCOL:
  If day ends negative → do NOT extract capital
  If day ends negative → activate Loss Recovery Mode for next N days
  Loss Recovery Mode: more conservative sizing, hedged entries, mean-reversion bias
  Track: recovery_days_remaining, recovery_target, recovery_daily_pnl

PROFIT EXTRACTION RULE:
  End-of-day equity > 10,000 + MIN_DAILY_PROFIT_TARGET → extract excess to "profit wallet"
  profit_wallet is a virtual ledger (real settled cash stays in brokerage)
  Weekly: if profit_wallet > threshold → note for manual ACH transfer
```

### Capital State Machine

```
States:
  NORMAL_OPERATION   → Daily target, normal risk, full strategy set
  RECOVERY_MODE      → After loss day; conservative sizing, hedged, 5-day window
  DRAWDOWN_ALERT     → Portfolio down > 3% intraday; pause new entries
  DRAWDOWN_CRITICAL  → Portfolio down > 5% intraday; close all positions
  COMPOUNDING_MODE   → Consecutive profitable days; slightly increase position sizes
  OPPORTUNITY_SURGE  → High-conviction scan finds >5 setups; increase deployment
```

## PART II — FREE API & BROKER INVENTORY

### Every Free Data Source Available

| Source | What It Provides | Free Tier Limit | Library |
|---|---|---|---|
| **Robinhood** | Quotes, options chain, crypto, fractional, 24/7 | Unlimited (personal account) | `robin_stocks` |
| **Schwab** | Quotes, Level 2, options, equity orders, account data | Unlimited (personal account) | `schwab-py` |
| **Yahoo Finance** | OHLCV history (20yr+), fundamentals, earnings calendar | Unlimited | `yfinance` |
| **FRED (St. Louis Fed)** | 800,000 macro series: rates, CPI, GDP, employment | Unlimited | `fredapi` |
| **SEC EDGAR** | All 10-K, 10-Q, 8-K, Form 4, 13F filings | Unlimited | `sec-edgar-downloader` |
| **CBOE** | VIX data, options settlement, historical IV | Unlimited (public) | `requests` scrape |
| **US Treasury** | Daily yield curve rates (2Y, 5Y, 10Y, 30Y) | Unlimited | `requests` JSON API |
| **Quandl / Nasdaq Data Link** | Futures COT data, alternative datasets | Free tier: limited | `nasdaqdatalink` |
| **Reddit (Pushshift / PRAW)** | WSB, investing, options sentiment | Unlimited | `praw` |
| **Google Trends** | Search volume for tickers, products | Unlimited | `pytrends` |
| **NewsAPI.org** | 100 req/day free tier — financial news headlines | 100/day free | `newsapi-python` |
| **GNews API** | News search — 100 req/day free | 100/day free | `requests` |
| **OpenInsider** | SEC Form 4 insider buying/selling, free scrape | Unlimited (scrape) | `requests+bs4` |
| **Finviz** | Stock screener data, sector maps, news | Unlimited (scrape) | `finvizfinance` |
| **StockAnalysis.com** | Earnings, revenue, short interest, IPO calendar | Unlimited (scrape) | `requests+bs4` |
| **Unusual Whales (free)** | Options flow public feed (partial) | Limited free | `requests` |
| **CFTC** | Commitment of Traders (COT) weekly futures positioning | Unlimited | `requests` JSON |
| **CryptoCompare** | Crypto OHLCV, social sentiment, on-chain basics | 100k calls/month free | `cryptocompare` |
| **Binance Public API** | Crypto prices, order book depth, funding rates | Unlimited (no key needed) | `python-binance` |
| **Coinbase Advanced** | Crypto spot prices, order book | Unlimited (no key needed) | `requests` |
| **Alpha Vantage** | 25 req/day free — equity, forex, crypto | 25/day free | `alpha_vantage` |
| **Ollama (local)** | LLM inference — llama3, mistral, phi3 | Unlimited (local) | `ollama` |
| **Hugging Face** | FinBERT sentiment model, local inference | Unlimited (local) | `transformers` |

### Zero-Cost Principle
```
Rule: NEVER pay for data. If a source requires payment → find the free equivalent.
Fallback chain: Schwab API → Robinhood API → yfinance → scrape → cache
Cache everything: if data was fetched today, use cached version for remaining calls
```

## PART III — OPPORTUNITY SCANNER ENGINE

### The Master Opportunity Scanner

This is the heart of the system — it runs continuously and feeds the Brain with ranked opportunities.

```python
# Conceptual architecture
class OpportunityScanner:
    """
    Scans ALL available instruments across ALL asset classes
    Returns ranked list of SetupOpportunity objects
    Runs every 5 minutes during market hours
    """
    
    SCAN_UNIVERSE = {
        "US_EQUITIES": {
            "large_cap":    500 stocks (SP500 components via yfinance),
            "mid_cap":      400 stocks (SP400 components),
            "small_cap":    600 stocks (SP600 components),
            "momentum":     top 50 by 1-month momentum (Finviz scrape),
            "earnings":     stocks with earnings today +/- 3 days,
            "gapper":       pre-market movers > 3% (yfinance pre-market),
            "unusual_vol":  volume today > 2x 20-day average,
            "insider_buy":  recent Form 4 cluster buys (OpenInsider scrape),
        },
        "ETFs": {
            "sector":       11 SPDR sector ETFs (XLK, XLF, XLE, XLV, etc.),
            "leveraged":    TQQQ, SOXL, UPRO, SPXL, TNA (3x ETFs),
            "inverse":      SQQQ, SPXS, TZA (inverse ETFs — bear market tools),
            "volatility":   VXX, UVXY, SVXY (volatility products),
            "thematic":     ARK funds, BOTZ, KOMP, BLOK (innovation),
        },
        "OPTIONS": {
            "0DTE":         SPY, QQQ, SPX daily expirations,
            "high_iv":      options with IV rank > 70% (sell premium),
            "low_iv":       options with IV rank < 30% (buy premium),
            "earnings_play": options on earnings stocks,
        },
        "CRYPTO": {
            "majors":       BTC, ETH, SOL, BNB (via Robinhood/Binance),
            "high_momentum": top 10 by 24h volume change (CryptoCompare),
            "defi_tokens":  available via Robinhood crypto list,
        },
        "FIXED_INCOME": {
            "t_bills":      SGOV, BIL (short-term T-bill ETFs),
            "money_market": SWVXX, VMFXX (sweep vehicles),
        }
    }
```

### Screener Filters (Applied Before Signal Generation)

```
TIER 1 FILTERS (mandatory — reduces universe from 1500+ to ~100):
  Volume: avg_daily_volume > $5M (liquid enough to enter/exit)
  Price: $1 < price < $5000 (avoid penny stocks and extreme prices)
  Spread: bid-ask spread < 0.5% (tight enough to trade profitably)
  Volatility: ATR/Price > 0.5% (enough movement to capture)

TIER 2 SCORES (rank the 100 survivors):
  Momentum Score:     (5d return + 10d return + 20d return) / 3, normalised
  Volume Score:       today_volume / avg_20d_volume
  Volatility Score:   current ATR / 20d avg ATR
  Catalyst Score:     earnings/news/insider activity binary flags
  Regime Score:       strategy suitability for current regime
  Technical Score:    number of bullish technical signals present

COMPOSITE OPPORTUNITY SCORE = weighted sum of Tier 2 scores
  Weights adjusted by current regime (BULL: weight momentum 40%, vol 20%)
  Top 20 opportunities fed to strategy matching engine
```

### Opportunity Types (All Detectable by Scanner)

```
MOMENTUM PLAYS:
  - Breakout: price above 52-week high with volume surge
  - Gap-and-Go: pre-market gap > 3%, holding above VWAP at open
  - Trend Continuation: ADX > 30, pullback to EMA-21, resuming
  - Sector Rotation: sector ETF RSI < 40 turning up while market bullish

MEAN REVERSION:
  - Oversold Bounce: RSI < 28, price at lower Bollinger Band, reversal candle
  - Gap Fill: gap up/down yesterday, filling back toward prior close
  - VWAP Reversion: extended deviation from VWAP (>2%)

CATALYST PLAYS:
  - Pre-Earnings Drift: 3 days before earnings, strong LLM sentiment
  - Post-Earnings Surprise: beat + raised guidance + positive LLM score
  - Insider Cluster Buy: 3+ officers buying same week (Form 4 signal)
  - Congress Trade Follow: senator bought → replicate within 48h

VOLATILITY PLAYS:
  - IV Crush: sell straddle before earnings (take opposite side post-announcement)
  - VIX Spike: VIX > 25 → buy volatility products or inverse ETFs
  - Low IV Expansion: buy straddles when IV rank < 15%

ARBITRAGE / STRUCTURAL:
  - ETF Pairs: SPY vs IVV, QQQ vs ONEQ (near-zero risk spread)
  - Leveraged ETF Decay: TQQQ vs QQQ divergence exploitation
  - Futures Basis: implied carry in commodity ETFs

CRYPTO OPPORTUNITIES:
  - BTC Funding Rate: positive funding → short bias via inverse; negative → long
  - Crypto-Equity Correlation Break: BTC diverging from NASDAQ
  - Stablecoin Yield: holding USDC equivalent for overnight carry
```

## PART IV — THE COMPLETE STRATEGY ARSENAL (50+ STRATEGIES)

### Strategy Registry with Free-API Compatibility

Each strategy below is rated by:
- **Edge Type**: where the alpha comes from
- **Regime**: which market conditions it works in
- **Holding Period**: typical trade duration
- **Free APIs Used**: data sources (all free)

#### GROUP A — MOMENTUM STRATEGIES

```
A1. OPENING_RANGE_BREAKOUT (ORB)
    Logic: Calculate high/low of first 15-minute candle (9:30-9:45).
           BUY if price breaks above ORB high with volume > 2x average.
           SELL if price breaks below ORB low.
    Stop: Other side of ORB. Target: 2x ORB range.
    Regime: Best in BULL_TREND and HIGH_VOL.
    Hold: 30 minutes to 2 hours.
    Data: yfinance 15m bars, Schwab real-time quote.
    Edge: Institutional order flow sets direction early.

A2. VWAP_MOMENTUM
    Logic: If price > VWAP and VWAP slope > 0 → long bias.
           Entry: first pullback to VWAP with RSI bounce from 45-55.
           Only trade stocks with volume rank > 1.5x average.
    Stop: VWAP - 0.5*ATR. Target: VWAP + 2*ATR.
    Regime: BULL_TREND, SIDEWAYS_HIGH.
    Data: yfinance intraday, calculated VWAP from open.
    Edge: VWAP acts as magnetic attractor; institutions use it.

A3. GAP_AND_GO
    Logic: Pre-market gap > 3% on news catalyst (LLM-confirmed positive).
           Enter at 9:32 AM if price holds above prior day close.
           Requires: float < 100M shares OR news catalyst score > 70.
    Stop: -2% from entry. Target: measured-move = prior day range.
    Regime: Any. Best in BULL.
    Data: yfinance pre-market, NewsAPI headlines, LLM sentiment.
    Edge: Short squeeze + retail FOMO on news gaps.

A4. RELATIVE_STRENGTH_ROTATION
    Logic: Rank all 11 SPDR sector ETFs by 5-day and 20-day momentum.
           Long top 3 sectors, short bottom 1 sector (hedge).
           Rebalance weekly; intraday signals on momentum divergence.
    Data: yfinance daily, SPDR ETF list (static).
    Regime: Any. Captures inter-sector flows.
    Hold: 1-5 days.

A5. MOMO_PREMARKET_SCANNER
    Logic: At 4:00 AM, scan top 50 pre-market movers via yfinance.
           Filter: gap > 3%, volume > 50k pre-market, not in wash-sale list.
           Score each by: gap size, news sentiment, volume, float.
           Build watchlist for opening session.
    Data: yfinance pre-market quotes, NewsAPI, Reddit mentions.
    Edge: Pre-market movers frequently set intraday direction.

A6. 52_WEEK_HIGH_BREAKOUT
    Logic: Scan for stocks making new 52-week highs with volume > 2x.
           Enter on first intraday pullback to breakout level.
           ADX > 25 required. No earnings within 5 days.
    Stop: Below breakout level. Target: prior resistance + 1 ATR.
    Data: yfinance history (52-week), Finviz screener scrape.
    Edge: Breakouts to new highs statistically continue (price discovery mode).

A7. UNUSUAL_VOLUME_SPIKE
    Logic: Scan every 5 minutes for stocks with volume > 3x 20-day average.
           Cross-reference with news (NewsAPI), options flow (Unusual Whales free).
           If no obvious news → may be informed buying (dark pool, insider).
           Enter small position; add if confirmed direction.
    Data: yfinance 5m bars, NewsAPI, OpenInsider.
    Edge: Volume precedes price; informed participants move first.
```

#### GROUP B — MEAN REVERSION STRATEGIES

```
B1. BOLLINGER_BAND_SQUEEZE_BREAKOUT
    Logic: Detect BB Width at 6-month low (squeeze).
           Wait for price to break out of squeeze with volume.
           Direction confirmed by MACD histogram turning positive.
    Stop: Re-entry of band. Target: opposite band.
    Regime: SIDEWAYS_LOW → transition to TRENDING.
    Data: yfinance daily + 1h bars.
    Edge: Volatility is mean-reverting; low vol precedes high vol.

B2. RSI_DIVERGENCE_REVERSAL
    Logic: Price makes new low but RSI makes higher low (bullish divergence).
           Or price makes new high but RSI makes lower high (bearish divergence).
           Confirm with MACD cross or engulfing candle.
    Hold: 1-3 days.
    Data: yfinance 1h or daily.
    Edge: Momentum exhaustion is a high-probability reversal signal.

B3. OVERSOLD_LARGE_CAP_BOUNCE
    Logic: SP500 stocks with: RSI < 28 AND price < lower BB AND
           no earnings in 5 days AND sector not in bear trend.
           Enter at close on oversold day; exit T+2 or at BBM.
    Stop: New 20-day low. Target: 20-day SMA.
    Data: yfinance daily, SP500 component list.
    Edge: Large caps rarely stay oversold — mean reversion is fast.

B4. INTRADAY_VWAP_DEVIATION
    Logic: If price deviates > 1.5% from VWAP by 11:00 AM without a catalyst:
           Fade the move (buy if 1.5% below VWAP, sell if 1.5% above).
           Only trade stocks with prior-day range < today's deviation.
    Stop: 2% deviation (extreme momentum may continue).
    Target: VWAP reversion.
    Edge: Most intraday deviations revert by 2 PM.

B5. MONDAY_GAP_FADE
    Logic: If market gaps up > 0.5% on Monday open with no major catalyst:
           Fade gap by shorting SPY or buying SQQQ.
           Close by 11 AM. Small size only (structural pattern, not fundamental).
    Data: yfinance pre-market, FRED (no weekend macro event check).
    Win Rate: ~58% historically on small Monday gaps.

B6. OVEREXTENDED_CRYPTO_REVERSION
    Logic: BTC or ETH extends > 5% from 20-day MA without on-chain catalyst.
           Short via Robinhood crypto sell (or buy inverse).
           Cover when price returns to 20-day MA.
    Data: yfinance crypto, CryptoCompare social sentiment.
    Edge: Crypto has strong mean-reversion within weekly ranges.
```

#### GROUP C — OPTIONS STRATEGIES (via Schwab)

```
C1. ZERO_DTE_IRON_CONDOR (SPY/QQQ)
    Logic: Each morning, check VIX < 20 and IV Rank > 50%.
           Sell OTM call + OTM put 1 standard deviation away (16 delta each).
           Buy wings 2 strikes further for protection.
           Close at 50% max profit OR 11 AM (avoid afternoon theta decay risk).
    Target: 40-50% of premium collected.
    Stop: 200% of premium (wings cap loss).
    Data: Schwab options chain, CBOE VIX data, calculated IV percentile.
    Edge: 0DTE theta decay is fastest; 16-delta condors have 68% win rate.

C2. EARNINGS_VOLATILITY_CRUSH
    Logic: Day before earnings: sell straddle (ATM call + ATM put).
           Close 30 minutes before market close on earnings day.
           Only trade when IV Rank > 80% (options priced for maximum fear).
    Risk: Earnings surprise can blow through wings → always use spreads (condor).
    Data: Schwab options chain, earnings calendar (yfinance), IV rank calculated locally.
    Edge: Options overprice earnings moves ~70% of the time.

C3. COVERED_CALL_YIELD_ENHANCEMENT
    Logic: On existing long stock positions held > 1 day:
           Sell 30 DTE calls at 0.30 delta.
           Roll at 21 DTE if untouched. Accept assignment if called away.
    Target: 1-2% monthly premium on held positions.
    Data: Schwab options chain.
    Edge: Free yield on existing positions; reduces cost basis.

C4. CASH_SECURED_PUT_ACQUISITION
    Logic: On stocks you want to own at lower price:
           Sell OTM puts 5-10% below current price, 30-45 DTE.
           Keep cash reserved (Schwab margin).
           If assigned: own stock at effective cost = strike - premium.
    Data: Schwab options chain, IV rank.
    Edge: Get paid to wait for your entry price; ~70% expire worthless.

C5. LONG_STRADDLE_PRE_CATALYST
    Logic: Buy ATM straddle (call + put) 5 days before earnings on stocks with:
           IV Rank < 30% (options cheap), historical earnings move > IV implied move.
           Close day before earnings (sell into IV expansion).
    Data: Schwab options chain, earnings calendar, historical earnings moves (yfinance).
    Edge: If historical move > implied move → straddle is mispriced cheap.

C6. POOR_MANS_COVERED_CALL (PMCC)
    Logic: Buy deep ITM LEAPS (6-12 month, 0.80 delta) instead of stock.
           Sell short-dated OTM calls against it monthly.
           Capital efficiency: LEAPS costs ~20% of stock price.
    Data: Schwab options chain.
    Edge: 5x capital efficiency vs stock ownership; same income generation.

C7. BROKEN_WING_BUTTERFLY
    Logic: In SIDEWAYS regime: set up asymmetric butterfly around expected range.
           Buy 1 call at lower strike, sell 2 calls at middle, buy 1 call at upper.
           Structure so one wing is further OTM → net credit received.
    Data: Schwab options chain.
    Edge: Receive credit for rangebound outcome; defined risk.
```

#### GROUP D — COPY TRADING & SIGNAL FOLLOWING STRATEGIES

```
D1. CONGRESS_TRADE_REPLICATION
    Logic: Monitor SEC Form 4 disclosures and congressional trading reports.
           Data source: OpenInsider (free scrape) + housestockwatcher.com (free).
           When a Congress member or senator files a purchase > $15,000:
             - Check if stock not in wash-sale or correlation limit
             - Replicate within 48 hours (regulatory window)
             - Size: 1% of portfolio per trade
             - Exit: 30-day hold or 10% profit target
    Data: OpenInsider scrape, Schwab for execution.
    Historical Edge: Congress trades outperformed market by ~6-10% historically.

D2. INSIDER_CLUSTER_BUY_FOLLOW
    Logic: OpenInsider.com free scrape — detect when 3+ company officers
           all buy stock in same 2-week window (cluster buy signal).
           Filter: purchases > $50,000 each, open market (not options exercise).
           Enter within 3 trading days of last filing.
    Exit: 10% profit OR 90 days (whichever first).
    Data: OpenInsider, yfinance, NewsAPI confirmation.
    Edge: Officers buying own stock with personal money → highest conviction signal.

D3. FINBERT_SENTIMENT_SIGNAL
    Logic: Run FinBERT (local HuggingFace model, free) on:
             - CNBC headlines (scraped free), NewsAPI, Reddit WSB posts
           Score each stock: -1 to +1 sentiment.
           Generate BUY if sentiment > 0.6 + technical confirmation.
           Generate SELL if sentiment < -0.4 + technical confirmation.
    Data: NewsAPI (100 calls/day free), Reddit PRAW (free), HuggingFace local FinBERT.
    Edge: Retail sentiment measurably predicts short-term price moves.

D4. WSB_REDDIT_MOMENTUM
    Logic: Every hour, scan r/wallstreetbets + r/stocks via PRAW (free Reddit API).
           Count mentions of each ticker in last 2 hours.
           Score by: mention velocity (rising), sentiment ratio, awards count.
           If ticker mention count spikes > 3 standard deviations:
             - Check float and short interest (Finviz scrape)
             - If small float + high short interest → potential squeeze setup
             - Enter small starter position; scale if confirmed
    Data: PRAW Reddit API (free), Finviz scrape.
    Edge: Retail coordination creates self-fulfilling momentum (GameStop model).

D5. GOOGLE_TRENDS_CATALYST
    Logic: Daily check Google Trends via pytrends (free) for rising searches.
           Map rising searches to tradeable symbols.
           If "buy gold" trending up → GLD/GDX setup.
           If "mortgage rates" trending → financial sector setup.
    Data: pytrends (completely free).
    Edge: Search intent leads price by 1-3 days in some categories.

D6. ETF_FLOW_MOMENTUM
    Logic: Monitor ETF inflows/outflows via StockAnalysis.com scrape.
           If sector ETF has 3-consecutive days inflows → sector rotation bullish.
           Invest in top 3 holdings of that ETF.
    Data: StockAnalysis scrape (free), yfinance for holdings.
    Edge: ETF inflows create mechanical buying pressure on underlying stocks.

D7. INSTITUTIONAL_13F_MOMENTUM
    Logic: Quarterly 13F filings reveal hedge fund holdings (SEC EDGAR, free).
           Track top 20 hedge funds' new positions from latest 13F.
           If multiple funds added same stock → institutional conviction signal.
           Buy within 30 days of 13F filing.
    Data: sec-edgar-downloader (free), SEC EDGAR JSON API.
    Edge: Follow smart money with 45-day lag; still meaningful for mid-term holds.
```

#### GROUP E — QUANTITATIVE & STATISTICAL STRATEGIES

```
E1. STATISTICAL_ARBITRAGE_PAIRS
    Logic: Full pairs universe — not just 2 pairs.
           Run cointegration test (Engle-Granger) on 200+ ETF pairs daily.
           Select top 10 cointegrated pairs (p < 0.01).
           Trade Z-score > ±2.0; exit at 0.
    Pairs tested: All combinations of sector ETFs, country ETFs, factor ETFs.
    Data: yfinance, statsmodels.
    Edge: Cointegrated pairs have structural mean-reversion property.

E2. VOLATILITY_REGIME_SWITCHING
    Logic: Use realized volatility (20-day) vs implied volatility (VIX) ratio.
           If RV/IV < 0.7 → sell options premium (vol overpriced).
           If RV/IV > 1.3 → buy options (vol underpriced).
           Size by ratio magnitude.
    Data: yfinance (realized vol), CBOE VIX (free scrape).
    Edge: IV and RV mean-revert to each other over 20-day cycles.

E3. CROSS_ASSET_CORRELATION_BREAK
    Logic: Track rolling 20-day correlation between: 
           BTC/NASDAQ, Gold/Dollar, Oil/Energy stocks, Yields/Banks.
           When correlation breaks from historical norm (> 2 SD):
             - Trade the divergence — long underperformer, short outperformer
             - Wait for re-correlation
    Data: yfinance, FRED, CryptoCompare.
    Edge: Structural relationships have strong mean-reversion.

E4. EARNINGS_PRICE_REACTION_MODEL
    Logic: Train a simple regression model (scikit-learn) on 3 years of earnings data:
           Features: beat/miss %, revenue surprise %, guidance revision, sector, IV crush.
           Target: post-earnings 5-day price move direction.
           Predict each upcoming earnings; trade if model confidence > 70%.
    Data: yfinance historical earnings (free), calculated features.
    Edge: Earnings reactions are partially predictable with sufficient features.

E5. FACTOR_MOMENTUM_PORTFOLIO
    Logic: Run daily factor scoring on SP500 universe:
           Value factor: P/E, P/B, EV/EBITDA (from yfinance fundamentals)
           Momentum factor: 12-1 month return
           Quality factor: ROE, debt/equity, earnings consistency
           Size factor: market cap tier
           Low-vol factor: 20-day return standard deviation
           Build long-short portfolio: long top quintile, short bottom quintile per factor.
    Rebalance: weekly.
    Data: yfinance fundamentals + history (all free).
    Edge: Academic factor premiums are real and persistent.

E6. LEAD_LAG_SECTOR_SIGNAL
    Logic: Research shows certain sectors lead/lag others:
           Tech leads Consumer Discretionary by ~3 days.
           Financials lead market turns by ~2 days.
           Energy lags commodity prices by ~1 week.
           Detect divergence → trade the lagging sector in direction of leading sector.
    Data: yfinance sector ETFs.
    Edge: Information propagates across sectors with measurable delay.

E7. QUANTILE_REGRESSION_INTRADAY
    Logic: For each stock in universe, build intraday quantile regression model:
           Predict probability distribution of close price given open, pre-market move, volume.
           Trade when predicted close is > 1.5% from current price with > 65% confidence.
    Data: yfinance 15m bars (90 days history, free).
    Edge: Statistical edge in prediction without needing directional certainty.

E8. MARKET_MICROSTRUCTURE_SIGNAL
    Logic: Calculate Order Flow Imbalance (OFI) from bid-ask data:
           OFI = (ask_size - bid_size) / (ask_size + bid_size)
           Positive OFI → buying pressure → bullish next 5 minutes.
           Use Schwab Level 2 data if available, else use bid/ask from quote.
    Data: Schwab real-time quotes.
    Edge: Microstructure signals predict next 5-15 minute moves.
```

#### GROUP F — MACRO & THEMATIC STRATEGIES

```
F1. RATE_SENSITIVE_ROTATION
    Logic: Monitor daily 10Y Treasury yield via FRED or US Treasury API.
           If 10Y yield rises > 5bps in a day → rotate from Growth to Value/Financials.
           If 10Y yield falls > 5bps → rotate from Value to Growth/Tech.
           ETF proxies: XLK (tech), XLF (financials), XLV (healthcare), XLE (energy).
    Data: FRED API (free), yfinance ETF quotes.
    Edge: Rate sensitivity creates predictable sector reactions.

F2. VIX_MEAN_REVERSION
    Logic: VIX > 28 → buy SPY dips (fear is overdone).
           VIX < 13 → begin hedging with small VXX position (complacency).
           VIX spikes > 15% in 1 day → buy UVXY for short-term spike continuation.
    Data: yfinance ^VIX.
    Edge: VIX has strong mean-reversion; spikes are temporary.

F3. FED_CALENDAR_POSITIONING
    Logic: 3 days before FOMC meeting → buy VXX (uncertainty premium).
           Day of FOMC → sell VXX at open (uncertainty peaks at announcement).
           "Buy the rumour, sell the news" on rate decisions.
    Data: FRED fed calendar, yfinance.
    Edge: Fed meeting uncertainty creates systematic volatility premium.

F4. CPI_RELEASE_TRADE
    Logic: Day before CPI release:
           If consensus CPI > prior → buy energy ETFs, short TLT (bonds).
           If consensus CPI < prior → buy tech, buy TLT.
           Close position same day as CPI release.
    Data: FRED API (free), economic calendar (Yahoo Finance scrape).
    Edge: Inflation data creates systematic sector rotations.

F5. GOLD_DOLLAR_INVERSE
    Logic: When DXY (US Dollar) falls > 0.5% → buy GLD or GDX.
           When DXY rises > 0.5% → sell/short GLD.
           Use DXY proxy: inverse of EUR/USD + GBP/USD via yfinance forex.
    Data: yfinance (EURUSD=X, GBPUSD=X, GLD).
    Edge: Gold/Dollar inverse relationship is one of the most stable in markets.

F6. COMMODITY_FUTURES_SIGNAL_TO_EQUITY
    Logic: Oil futures rise > 1.5% (CL=F from yfinance) → buy XLE, CVX, XOM.
           Natural gas (NG=F) spike → buy UNG ETF.
           Copper (HG=F) rise → buy FCX, copper miners.
    Data: yfinance futures tickers (CL=F, NG=F, GC=F, HG=F) — all free.
    Edge: Commodity moves precede equity moves in related sectors.
```

#### GROUP G — LEVERAGED / HIGH-OCTANE STRATEGIES (Small Size, High Potential)

```
G1. LEVERAGED_ETF_TREND_FOLLOW
    Logic: In BULL_TREND regime only:
           TQQQ (3x NASDAQ) or SOXL (3x Semiconductors) on MACD crossover.
           Position size: MAX 5% of portfolio (leverage amplifies both directions).
           Strict stop: -5% (leveraged ETFs can move 10%+ in a day).
    Data: yfinance.
    Edge: Leveraged ETFs amplify trend gains; strict stop prevents catastrophic loss.

G2. GAMMA_SQUEEZE_DETECTOR
    Logic: Detect stocks with:
           Short interest > 20% float AND rising call option open interest.
           When these conditions meet → gamma squeeze potential.
           Enter small position in stock OR near-dated call options.
           Exit immediately at first sign of squeeze exhaustion (volume drop).
    Data: Finviz scrape (short interest), Schwab options chain.
    Edge: Dealer hedging creates mechanical buying pressure in squeeze scenarios.

G3. CRYPTO_MOMENTUM_BURST
    Logic: BTC or ETH makes 3% move in 1 hour (CryptoCompare free).
           Enter same direction with 2% portfolio allocation via Robinhood crypto.
           Stop: 1.5% against position. Target: 3% (1:2 R:R).
           Exit if move stalls > 30 minutes (intraday crypto momentum is short-lived).
    Data: CryptoCompare (free), Robinhood for execution.
    Edge: Crypto trend bursts have high continuation rate in first 2 hours.

G4. SHORT_VOLATILITY_CARRY
    Logic: When VIX term structure is in contango (front month < back month):
           This contango decays daily → profit by holding SVXY (short VIX ETF).
           Entry: VIX term structure slope > 5% contango.
           Exit: VIX spikes > 20% in one day (regime change).
           Size: 3% max portfolio.
    Data: CBOE VIX futures term structure (free scrape).
    Edge: VIX contango is persistent; carrying short vol pays 20-40% annually in normal markets.
```

## PART V — THE QUANTUM BRAIN (STRATEGY SELECTOR)

### Architecture: The Decision Hierarchy

```
LEVEL 1 — MARKET REGIME ENGINE (HMM + Macro)
  Input: SPY 2yr daily, VIX, Yield Curve, Put/Call Ratio, Breadth
  Output: {regime_state, bull_prob, crash_prob, vol_regime}
  Frequency: Every 30 minutes

LEVEL 2 — OPPORTUNITY RANKER
  Input: Scan results from OpportunityScanner (all 1500+ symbols)
  Process: Apply Tier 1 filters → Tier 2 scoring → rank
  Output: Top 20 opportunities with composite scores
  Frequency: Every 5 minutes

LEVEL 3 — STRATEGY MATCHER
  Input: {opportunity, regime_state, current_portfolio_state, capital_available}
  Process: For each opportunity → find compatible strategies → score strategy fit
  Output: List of (opportunity, strategy, priority_score) tuples
  Frequency: Per opportunity, every cycle

LEVEL 4 — PORTFOLIO CONSTRUCTOR
  Input: All (opportunity, strategy) pairs
  Process: 
    - Check correlation with existing positions
    - Apply Kelly sizing
    - Check total risk budget (max 6% portfolio at risk simultaneously)
    - Optimise: max expected daily PnL subject to drawdown constraints
  Output: Final approved trade list with sizes
  Frequency: Per cycle, final approval gate

LEVEL 5 — RISK GATE (NEVER BYPASSED)
  12-step risk check (from Phase 4) runs on every approved trade.
  If blocked → log, find next best opportunity.

LEVEL 6 — TAX-AWARE ORDER BUILDER
  Before any sell order:
    - Check lot ages (prefer LTCG lots after 365 days)
    - Check wash-sale impact
    - Calculate net after-tax gain vs gross gain
    - If net after-tax gain < threshold → delay sale, hedge with options instead
  Output: Final orders with lot-level tax optimisation
```

### Strategy-Regime Compatibility Matrix

```
                    BULL  BEAR  SIDEWAYS  HIGH_VOL  CRASH  RECOVERY
OPENING_RANGE_BREAK   ✓✓    ✓     ✓✓        ✓✓       ✗       ✓
VWAP_MOMENTUM         ✓✓    ✗     ✓         ✓        ✗       ✓
GAP_AND_GO            ✓✓    ✓     ✗         ✓✓       ✗       ✓
RELATIVE_STR_ROT      ✓     ✓✓    ✓✓        ✓        ✓       ✓✓
52WK_HIGH_BREAKOUT    ✓✓    ✗     ✗         ✓        ✗       ✗
UNUSUAL_VOLUME        ✓     ✓     ✓✓        ✓✓       ✗       ✓
BB_SQUEEZE            ✓     ✓     ✓✓        ✓        ✗       ✓
RSI_DIVERGENCE        ✓     ✓✓    ✓✓        ✓        ✗       ✓✓
OVERSOLD_BOUNCE       ✓     ✓✓    ✓         ✓        ✗       ✓✓
VWAP_DEVIATION        ✓     ✓     ✓✓        ✓        ✗       ✓
0DTE_IRON_CONDOR      ✗     ✗     ✓✓        ✗        ✗       ✓
EARNINGS_IV_CRUSH     ✓     ✓     ✓✓        ✓✓       ✗       ✓
STAT_ARB_PAIRS        ✓     ✓✓    ✓✓        ✓        ✓       ✓✓
CONGRESS_COPY         ✓✓    ✗     ✓         ✗        ✗       ✓
INSIDER_FOLLOW        ✓✓    ✗     ✓         ✗        ✗       ✓
FINBERT_SENTIMENT     ✓     ✓     ✓         ✓        ✗       ✓
WSB_MOMENTUM          ✓✓    ✗     ✗         ✓✓       ✗       ✗
VIX_MEAN_REVERSION    ✗     ✓✓    ✗         ✓✓       ✓✓      ✓✓
LEVERAGED_ETF         ✓✓    ✗     ✗         ✗        ✗       ✗
GAMMA_SQUEEZE         ✓✓    ✗     ✗         ✓✓       ✗       ✗
CRYPTO_MOMENTUM       ✓     ✗     ✓         ✓✓       ✗       ✓
RATE_ROTATION         ✓     ✓     ✓✓        ✓        ✓       ✓

Legend: ✓✓ = strongly favoured  ✓ = compatible  ✗ = disabled in this regime
```

### Thompson Sampling Bandit with Contextual Extension

```python
class ContextualThompsonSampler:
    """
    Standard Thompson Sampling extended with context features.
    Each (strategy, regime) pair has its own Beta distribution.
    This means the Brain learns which strategies work in which regimes independently.
    """
    
    # State: dict[(strategy_id, regime_state)] → Beta(alpha, beta)
    
    def sample_allocation(self, available_strategies, regime, capital):
        scores = {}
        for strategy_id in available_strategies:
            key = (strategy_id, regime)
            alpha, beta = self.get_params(key)  # from DB
            
            # Sample from posterior
            sampled_prob = np.random.beta(alpha, beta)
            
            # Apply regime compatibility multiplier
            regime_mult = REGIME_COMPATIBILITY_MATRIX[strategy_id][regime]
            
            # Apply recency weight (recent performance weighted more)
            recency_weight = self.get_recency_weighted_performance(strategy_id, days=14)
            
            scores[strategy_id] = sampled_prob * regime_mult * recency_weight
        
        # Normalise, apply floors, return allocation
        return self.normalise_with_floors(scores, min_weight=0.03)
    
    def update(self, strategy_id, regime, pnl, trade_metadata):
        key = (strategy_id, regime)
        if pnl > 0:
            self.increment_alpha(key)
        else:
            self.increment_beta(key)
        # Extra: update by magnitude (scale update by |pnl| / avg_pnl)
```

## PART VI — TAX-AWARE QUANTITATIVE PORTFOLIO MANAGER

### Philosophy: Net-After-Tax Return is the Only Return That Matters

```
DECISION FRAMEWORK FOR EVERY SELL:
  Gross PnL = fill_price - cost_basis
  Tax cost = gross_pnl * applicable_rate(holding_period)
  Net PnL = gross_pnl - tax_cost

  Rates (2024 US):
    Short-term gain (< 1 year): taxed as ordinary income (~22-37%)
    Long-term gain (≥ 1 year): 0%, 15%, or 20% (based on income)
    Short-term loss: can offset same-year gains dollar-for-dollar
    Long-term loss: offsets LTCG first, then STCG

  Decision: if position is day 360 of 365 → WAIT 5 MORE DAYS → save ~15-17% tax rate
  Decision: if losing position with no recovery signal → harvest loss now → reduce tax bill
```

### Tax Engine Extended Capabilities

```
1. REAL-TIME TAX LIABILITY TRACKER
   - Maintain running YTD tax liability estimate
   - Update on every fill
   - Display in dashboard: "Estimated YTD Tax: $X,XXX"

2. LOT SELECTION INTELLIGENCE
   For every sell order, evaluate ALL lot selection methods:
   - FIFO: first-in first-out (IRS default)
   - HIFO: highest-cost first (minimises current gain — best for taxable accounts)
   - LTCG_FIRST: sell lots past 365 days first (get preferential rate)
   - LOSS_FIRST: sell lots with losses first (harvest losses, defer gains)
   
   Algorithm: for each sell, calculate net-after-tax proceeds under each method.
   Select method that maximises net-after-tax proceeds.
   Store lot_method used per trade in tax_lots table.

3. GAIN DEFERRAL OPTIMIZER
   Before selling a profitable short-term position:
   - Calculate days until it becomes long-term
   - If < 30 days to 1-year anniversary AND downside risk is manageable:
     → Consider holding + buying protective put to lock in gain
     → Constructive sale rules: do NOT short same stock (IRS wash-sale related)
   - Calculate: premium of protective put vs tax savings
     If tax_savings > put_premium → buy put and wait

4. WASH SALE INTELLIGENCE
   - Not just tracking blacklist: proactively SCHEDULE proxy swaps
   - 30 days before wash-sale expiry → schedule re-entry if signal is positive
   - Track "substantially identical" securities (IRS definition):
     Flagged pairs: SPY/IVV/VFIAX, QQQ/ONEQ/NASDAQ, same underlying options

5. YEAR-END TAX PLANNING (December Mode)
   - October 1: Run full year-end projection
   - November 15: If projected STCG > $5,000 → aggressive TLH scan
   - December 1: If still net positive → consider donating appreciated shares
     (charitable deduction at FMV; no capital gains) — log as note, not automated
   - December 15: Final harvest window; lock in losses before year-end
   - December 26: Re-enter proxies (wash sale 30-day clock started Dec 15)

6. QUARTERLY ESTIMATED TAX TRACKER
   Payment due dates: April 15, June 15, September 15, January 15
   - Project quarterly liability from realized gains YTD
   - Alert 30 days before each deadline: "Estimated Q{N} payment: $X,XXX due {date}"
   - Log to dashboard tax summary section

7. FORM 8949 + SCHEDULE D EXPORT
   - Full IRS-compatible CSV export of all closed lots
   - Group A (short-term, reported to IRS), Group D (long-term, reported to IRS)
   - Include wash sale adjustments in column G
   - Export available from UI at any time
```

## PART VII — ZERO-LOSS PROTOCOL & RECOVERY SYSTEM

### Loss Prevention Architecture (Not Zero-Loss in Absolute Terms — Loss Prevention)

```
IMPORTANT ENGINEERING NOTE:
No system can guarantee zero losses in all market conditions.
What we CAN build is:
1. Maximum loss limitation (position-level stops, portfolio-level halts)
2. Loss recovery system (adaptive behaviour after loss days)
3. Dynamic risk reduction (reduce size when drawdown occurs)
4. Asymmetric strategies (more ways to profit than to lose)
5. Daily profit extraction (lock in profits before they can be given back)

TARGET: Expected value positive every day across the strategy ensemble.
REALITY: Some days will be small negatives; recovery mode handles them.
```

### Daily Profit & Loss Management Rules

```python
class DailyPnLManager:
    """
    Manages the $10,000 daily reset cycle
    """
    
    DAILY_RULES = {
        # How much profit to target before easing into risk
        "min_daily_profit_target":  1500.0,   # $150 = 15% on $10k (conservative)
        "ideal_daily_profit_target": 3000.0,  # $300 = 30% on $10k (achievable)
        "stretch_daily_target":     5000.0,   # $500 = 50% on $10k (on great days)
        
        # When to lock in profits (reduce new entries)
        "profit_lock_threshold":    2000.0,   # At $2000 profit → protect 60% of it
        "profit_protect_pct":       0.60,    # Don't risk more than 40% of made profit
        
        # Daily loss limits
        "max_daily_loss":           300.0,   # -$300 = -3% → full halt
        "soft_halt_loss":           150.0,   # -$150 = -1.5% → reduce size 50%
        
        # Recovery mode settings
        "recovery_max_days":        5,       # Try to recover within 5 trading days
        "recovery_daily_target":    1.0,     # Recovery: target +1% per day (conservative)
        "recovery_risk_multiplier": 0.5,     # Half normal position sizes in recovery
    }
    
    def end_of_day_settlement(self, final_equity, starting_equity=10000):
        """Called at 3:55 PM ET"""
        daily_pnl = final_equity - starting_equity
        
        if daily_pnl > self.DAILY_RULES["min_daily_profit_target"]:
            # PROFIT DAY: Extract excess above $10,000 floor
            extract_amount = daily_pnl  # Or daily_pnl - buffer for tomorrow
            self.log_profit_extraction(extract_amount)
            self.reset_capital_to_base(starting_equity=10000)
            self.state = "NORMAL_OPERATION"
            self.consecutive_profit_days += 1
            
        elif daily_pnl < 0:
            # LOSS DAY: No extraction, enter recovery mode
            self.state = "RECOVERY_MODE"
            self.recovery_days_remaining = self.DAILY_RULES["recovery_max_days"]
            self.recovery_target = abs(daily_pnl) * 1.1  # Recover loss + 10% buffer
            self.consecutive_profit_days = 0
            self.log_loss_day(daily_pnl)
            
        else:
            # SMALL PROFIT: Keep in account, don't extract (below min target)
            self.state = "NORMAL_OPERATION"
    
    def get_position_size_multiplier(self):
        """Reduce position sizes based on state"""
        if self.state == "RECOVERY_MODE":
            return self.DAILY_RULES["recovery_risk_multiplier"]  # 0.5x
        elif self.consecutive_profit_days >= 5:
            return 1.2  # Slight increase after 5 winning days
        elif self.current_day_pnl < -self.DAILY_RULES["soft_halt_loss"]:
            return 0.5  # Intraday soft halt: cut sizes
        else:
            return 1.0
```

### Hedging Strategies for Downside Protection

```
PORTFOLIO HEDGE LADDER (always-on protection):

Hedge 1 — SMALL PERMANENT SPY PUT WING
  - Hold 1-2 far OTM SPY puts (30-60 DTE, 5% OTM) at all times
  - Cost: ~$15-30/month in premium
  - Payoff: protects against sudden -5% market moves
  - This is "portfolio insurance"

Hedge 2 — VIX CALL ON SPIKE DAYS
  - When VIX < 15 (complacency): buy small VXX position (1-2% NAV)
  - This gains when market drops (VIX inversely correlated with SPY)
  - Cost-of-carry: negative (VIX ETFs have bleed); keep position < 5 days

Hedge 3 — INVERSE ETF DURING BEAR SIGNALS
  - HMM outputs BEAR_TREND or CRASH_RISK probability > 40%:
    → Allocate 5-10% to SQQQ or SPXS (inverse 3x ETFs)
  - Full exit when regime reverts to BULL

Hedge 4 — CASH IS A POSITION
  - At any time: minimum 20% cash buffer
  - Cash generates yield via SWVXX (money market ~5% APY annualized)
  - Cash is the ultimate hedge; never be 100% invested
```

## PART VIII — ENHANCED SYSTEM ARCHITECTURE

### New Components (Additions to Phase I–XI Design)

```
NEW FILE: engine/scanner/opportunity_scanner.py
  Class OpportunityScanner
  - run_full_scan() → list[SetupOpportunity] (runs every 5 min)
  - run_premarket_scan() → list[SetupOpportunity] (runs at 4 AM)
  - score_opportunity(opp) → float
  - SetupOpportunity dataclass: symbol, asset_class, opportunity_type, 
    composite_score, technical_signals, catalyst_flags, recommended_strategies

NEW FILE: engine/scanner/stock_screener.py
  - get_sp500_components() → list[str] (Wikipedia scrape, cached daily)
  - get_premarket_movers() → list[dict] (yfinance pre-market)
  - get_high_volume_stocks() → list[str] (volume > 2x average)
  - get_earnings_calendar(days_ahead=5) → list[dict]
  - get_52week_high_breakouts() → list[str]
  - scan_finviz(filters: dict) → list[str] (Finviz free scrape)

NEW FILE: engine/data/alternative_data.py
  - get_insider_trades() → list[dict] (OpenInsider scrape)
  - get_congress_trades() → list[dict] (housestockwatcher.com scrape)
  - get_reddit_sentiment(symbols: list[str]) → dict[str, float]
  - get_finbert_sentiment(text: str) → dict  (local HuggingFace FinBERT)
  - get_google_trends(keywords: list[str]) → dict[str, float]
  - get_13f_new_positions() → list[dict] (SEC EDGAR)
  - get_short_interest(symbol: str) -> dict (Finviz scrape)

NEW FILE: engine/brain/opportunity_ranker.py
  - rank_opportunities(opportunities, regime, portfolio_state) → list[RankedSetup]
  - match_strategies(setup: SetupOpportunity, regime: str) → list[str]
  - build_trade_list(ranked_setups, capital_available) → list[ApprovedTrade]

NEW FILE: engine/brain/daily_pnl_manager.py
  - Class DailyPnLManager (see above)
  - end_of_day_settlement()
  - get_position_size_multiplier()
  - is_in_recovery_mode() → bool
  - get_recovery_status() → dict

NEW FILE: engine/tax/tax_optimizer.py
  - Class TaxAwarePortfolioManager
  - select_optimal_lots(symbol, qty_to_sell) → list[TaxLot]
  - evaluate_gain_deferral(position) → GainDeferralRecommendation
  - should_harvest_now(position, regime) → bool
  - calculate_net_after_tax_pnl(gross_pnl, holding_days) → float
  - get_year_end_plan() → dict
  - project_quarterly_tax(quarter: int) → float

NEW STRATEGIES FILES:
  engine/strategies/copy_trading/congress_trade.py
  engine/strategies/copy_trading/insider_follow.py
  engine/strategies/copy_trading/institutional_13f.py
  engine/strategies/sentiment/finbert_signal.py
  engine/strategies/sentiment/wsb_momentum.py
  engine/strategies/sentiment/google_trends_signal.py
  engine/strategies/options/zero_dte_condor.py
  engine/strategies/options/earnings_iv_crush.py
  engine/strategies/options/cash_secured_put.py
  engine/strategies/options/poor_mans_covered_call.py
  engine/strategies/macro/rate_rotation.py
  engine/strategies/macro/vix_mean_reversion.py
  engine/strategies/macro/commodity_equity_signal.py
  engine/strategies/quant/volatility_regime.py
  engine/strategies/quant/cross_asset_correlation.py
  engine/strategies/quant/factor_momentum.py
  engine/strategies/quant/lead_lag_sector.py
  engine/strategies/intraday/opening_range_breakout.py
  engine/strategies/intraday/vwap_momentum.py
  engine/strategies/intraday/gap_and_go.py
  engine/strategies/intraday/unusual_volume.py

ENHANCED SCHEDULER JOBS:
  - pre_market_scan (4:00 AM): Run OpportunityScanner.run_premarket_scan()
  - alternative_data_refresh (4:30 AM): Fetch insider/congress/Reddit/news
  - finbert_batch_analysis (5:00 AM): Run FinBERT on overnight news batch
  - opportunity_refresh (every 5 min, market hours): Full scan cycle
  - tax_optimizer_scan (4:15 PM): TaxAwarePortfolioManager.evaluate_all_positions()
  - daily_settlement (3:55 PM): DailyPnLManager.end_of_day_settlement()
  - profit_wallet_update (4:00 PM): Log daily extraction amount
  - weekly_tax_review (Saturday): Full year-to-date tax projection
```

## PART IX — ENHANCED DATABASE SCHEMA (ADDITIONS)

```sql
-- Daily capital cycle tracking
TABLE daily_cycle_log:
  id, cycle_date, starting_capital, ending_equity,
  daily_pnl, daily_pnl_pct, profit_extracted, profit_wallet_cumulative,
  cycle_state (NORMAL/RECOVERY/HALTED), num_trades, 
  winning_trades, losing_trades, largest_win, largest_loss,
  strategies_used (JSON array), regime_state, notes

-- Profit wallet (virtual ledger of extracted profits)
TABLE profit_wallet:
  id, extraction_date, amount, cumulative_balance,
  cycle_state_at_extraction, daily_pnl_at_extraction, notes

-- Recovery mode tracking
TABLE recovery_sessions:
  id, start_date, trigger_loss, recovery_target,
  days_allowed, days_used, amount_recovered,
  status (IN_PROGRESS/SUCCESS/TIMEOUT/ABANDONED),
  strategy_adjustments_json

-- Opportunity scan results (for analysis/learning)
TABLE opportunity_scans:
  id, scan_time, symbol, opportunity_type, composite_score,
  technical_signals_json, catalyst_flags_json,
  recommended_strategies_json, acted_on, outcome_pnl

-- Alternative data signals
TABLE alternative_signals:
  id, signal_time, source (INSIDER/CONGRESS/REDDIT/FINBERT/GOOGLE_TRENDS),
  symbol, signal_type, signal_value, confidence,
  acted_on, outcome_pnl_if_acted

-- Tax optimization decisions
TABLE tax_optimization_decisions:
  id, decision_time, symbol, position_pnl, holding_days,
  lot_method_chosen, alternative_considered,
  gross_pnl, estimated_tax_cost, net_pnl_after_tax,
  decision_reason (HIFO_SELECTED/DEFERRED_FOR_LTCG/HARVESTED_LOSS),
  actual_tax_saving_vs_fifo

-- Hedge positions (tracked separately)
TABLE hedge_positions:
  id, symbol, hedge_type (SPY_PUT/VXX/INVERSE_ETF),
  qty, cost, current_value, hedge_ratio,
  portfolio_delta_offset, opened_at, closed_at, pnl
```

## PART X — ENHANCED CONTROL UI (ADDITIONS)

### New Dashboard Panels

```
PANEL: DAILY CYCLE TRACKER
  ┌─────────────────────────────────────────────────────────┐
  │  TODAY'S CYCLE                                          │
  │  Starting Capital: $10,000.00                           │
  │  Current Equity:   $10,247.83   (+$247.83 / +2.48%)    │
  │  Profit Target:    $3000.00  ████████░░░░  82% achieved  │
  │  Profit Locked:    $1480.70  (60% of gains protected)    │
  │  State: NORMAL ●  |  Recovery Mode: OFF                 │
  │  Profit Wallet (cumulative): $3,847.22                  │
  └─────────────────────────────────────────────────────────┘

PANEL: OPPORTUNITY SCANNER FEED (live, every 5 min)
  ┌─────────────────────────────────────────────────────────┐
  │  LIVE OPPORTUNITIES                     Scan: 09:45 AM  │
  │  Rank │ Symbol │ Type           │ Score │ Strategy      │
  │    1  │  NVDA  │ 52WK Breakout  │  0.87 │ TREND_FOLLOW  │
  │    2  │  SPY   │ ORB Long       │  0.82 │ OPEN_RANGE    │
  │    3  │  TSLA  │ Unusual Volume │  0.79 │ VOL_MOMENTUM  │
  │    4  │  SPY   │ 0DTE Condor    │  0.74 │ IRON_CONDOR   │
  │    5  │  BTC   │ Funding+Trend  │  0.71 │ CRYPTO_MOMO   │
  └─────────────────────────────────────────────────────────┘

PANEL: STRATEGY PERFORMANCE MATRIX
  ┌─────────────────────────────────────────────────────────┐
  │  STRATEGY      │ 7d PnL  │ WinRate │ Weight │ Regime ✓  │
  │  ORB           │ +$312   │  68%    │ 0.22   │    ✓      │
  │  VWAP_MOMO     │ +$187   │  61%    │ 0.15   │    ✓      │
  │  0DTE_CONDOR   │ +$94    │  71%    │ 0.12   │    ✓      │
  │  CONGRESS_COPY │ +$76    │  78%    │ 0.10   │    ✓      │
  │  INSIDER_FOLLOW│ +$43    │  74%    │ 0.08   │    ✓      │
  │  ...           │  ...    │  ...    │  ...   │   ...     │
  └─────────────────────────────────────────────────────────┘

PANEL: TAX DASHBOARD
  ┌─────────────────────────────────────────────────────────┐
  │  TAX SUMMARY (YTD 2025)                                 │
  │  Realized STCG:     +$2,847.00   Est. Tax: ~$711        │
  │  Realized LTCG:     +$1,203.00   Est. Tax: ~$180        │
  │  Harvested Losses:  -$892.00     Tax Saved: ~$223        │
  │  Net Tax Liability: ~$668        vs Naive: ~$1,012       │
  │  Tax Efficiency:    34% SAVED vs naive FIFO strategy     │
  │  Next Est. Payment: Jun 15  ~$334  [30 days away]       │
  │  [Download Form 8949 CSV]  [Full Tax Report]            │
  └─────────────────────────────────────────────────────────┘

PANEL: ALTERNATIVE DATA SIGNALS
  ┌─────────────────────────────────────────────────────────┐
  │  ALTERNATIVE DATA FEED                  Updated: 5m ago  │
  │  [INSIDER] NVDA — 3 officers bought $2.1M — 2 days ago  │
  │  [CONGRESS] Sen. Smith bought MSFT $47k — yesterday     │
  │  [REDDIT] AMC — mention spike +340% — high short int    │
  │  [FINBERT] AAPL earnings — sentiment 0.74 BULLISH       │
  │  [TRENDS] "buy gold" +180% search vol — gold signal     │
  └─────────────────────────────────────────────────────────┘

PANEL: RECOVERY MODE TRACKER (visible when in recovery)
  ┌─────────────────────────────────────────────────────────┐
  │  ⚠ RECOVERY MODE ACTIVE                                 │
  │  Trigger Loss: -$187.43 (loss on 2025-01-14)           │
  │  Recovery Target: $206.17 (+10% buffer)                 │
  │  Recovered So Far: $143.22  (69%)                       │
  │  Days Used: 2 of 5 allowed                              │
  │  Position Size Multiplier: 0.5x (conservative mode)     │
  │  Active Strategies: Mean-Rev, Stat-Arb, Options only    │
  └─────────────────────────────────────────────────────────┘

CONTROLS: PARAMETER OVERRIDE PANEL
  ┌─────────────────────────────────────────────────────────┐
  │  LIVE PARAMETER OVERRIDES (no restart required)         │
  │  Daily Profit Target:  [  300  ] $ [Apply]             │
  │  Max Daily Loss:       [  300  ] $ [Apply]             │
  │  Position Size Multi:  [  1.0  ] x [Apply]             │
  │  Max Open Positions:   [  10   ]   [Apply]             │
  │  Risk Per Trade:       [  2.0  ] % [Apply]             │
  │  Recovery Mode Days:   [  5    ]   [Apply]             │
  └─────────────────────────────────────────────────────────┘
```

## PART XI — REGULATORY COMPLIANCE MATRIX

```
RULE                  REGULATION      IMPLEMENTATION
─────────────────────────────────────────────────────────────────────
PDT (Pattern Day       FINRA Rule       Track all day-trades in 5-day
Trader) Rule           4210             rolling window. Block 4th 
                                        day-trade if equity < $25,000.
                                        Mitigation: Use Robinhood for
                                        some trades (PDT-exempt for
                                        cash accounts up to limit).

Wash-Sale Rule         IRC §1091        30-day pre/post loss blocking.
                                        Proxy swap system. NEVER re-
                                        enter same or substantially
                                        identical security.

Short-Term vs          IRC §1222        Lot-level tracking. HIFO lot
Long-Term Capital                       selection. Gain deferral to 
Gains                                   365-day LTCG threshold.

Constructive Sale      IRC §1259        Do NOT enter forward contract,
Rule                                    short sale, or total return
                                        swap on appreciated stock you
                                        still hold.

SEC Regulation SHO     17 CFR §242      Do not short sell without
(Short Sales)                           locating shares. Robinhood and
                                        Schwab handle this server-side.
                                        Log any "locate failed" errors.

FINRA Best             FINRA Rule       Smart Order Router always logs
Execution              5310             both broker quotes considered
                                        before routing.

Form 4 Trading         SEC §16(b)       We are NOT insiders. We follow
Restrictions                            publicly disclosed Form 4 data
                                        after the filing is public.
                                        48-hour delay from filing.

Tax Reporting          IRS Schedule D   Form 8949 export includes ALL
                       & Form 8949      required columns. Wash sale
                                        adjustments in column G.
                                        Broker 1099-B reconciliation
                                        check in December.

Estimated Tax          IRS §6654        Quarterly tax estimator alerts
Payments                                before each due date.
                                        Underpayment penalty if YTD
                                        withholding < 90% of liability.
```

## PART XIII — EXPECTED PERFORMANCE PARAMETERS

### Realistic Daily Expectations on $10,000 Capital

```
CONSERVATIVE SCENARIO (high-certainty trades only, low volatility market):
  Daily profit target: $100-$150 (1.0-1.5%)
  Expected win rate: 62-68%
  Strategies active: Mean-Reversion, Stat-Arb, Covered Calls, VWAP
  Max daily loss: -$100 (1%)
  Monthly compounded: ~$2,500-$4,000 on $10k

NORMAL SCENARIO (mixed market, balanced strategies):
  Daily profit target: $150-$300 (1.5-3%)
  Expected win rate: 58-65%
  Strategies active: All non-aggressive (15-20 strategies)
  Max daily loss: -$200 (2%)
  Monthly compounded: ~$4,000-$8,000 on $10k

AGGRESSIVE SCENARIO (bull market, momentum strategies):
  Daily profit target: $300-$500 (3-5%)
  Expected win rate: 55-62%
  Strategies active: Full arsenal including leveraged ETFs, 0DTE options
  Max daily loss: -$300 (3%)
  Monthly compounded: ~$8,000-$12,000 on $10k

IMPORTANT NOTES:
  - These are EXPECTED VALUES, not guarantees
  - 30-40% of trading days may be small losses (< 1%)
  - Recovery Mode handles loss days over 5-day window
  - Tax efficiency adds 15-20% to net returns over gross
  - Compounding effect: reinvesting profits grows base capital
  - All strategies must be backtested before live deployment
  - Start with 30-day shadow mode validation before any real money
```

### Annual Projection (if $10k floor maintained, profits extracted)

```
Monthly extracted profits (conservative): $2,500-$4,000
Annual extracted profits: $30,000-$48,000 on $10,000 at risk
Return on capital: 300-480% annually (theoretical maximum with compounding)

REALISTIC EXPECTATION with all risks factored:
  Achieving 100-200% annual return on capital is ambitious but possible
  with a disciplined, diversified multi-strategy approach.
  Expect: some strategies to underperform, some to surprise upward.
  The Brain's job is to allocate more capital to what's working RIGHT NOW.
```

---

# BOOK III: COMPLETE COPILOT AGENT IMPLEMENTATION PROMPTS
*Complete Directed Implementation Prompt for GitHub Copilot (Claude Sonnet 4.6)*

> **HOW TO USE THIS PROMPT**
> Paste the entire contents of each Phase section into Copilot Chat or Copilot Edits one Phase at a time.
> Do NOT move to the next Phase until every Acceptance Criterion in the current Phase is met.
> Always prepend each Phase prompt with: *"You are an elite Python quant engineer building an enterprise-grade autonomous trading system. Strictly follow these instructions. Use only open-source libraries. Target platform: Windows 10/11 x64, Python 3.11+."*

## SYSTEM OVERVIEW — READ BEFORE ALL PHASES

### What You Are Building
Two completely independent Python processes that run simultaneously on a local Windows machine:

```
PROCESS 1 — Trading Engine (Background Service)
  ├── Runs 24 / 7 as a Windows background process (pythonw.exe or NSSM service)
  ├── Executes all trading logic, strategies, risk checks, and broker API calls
  ├── Persists all state to SQLite (single-file, zero-install database)
  ├── Exposes a lightweight REST + WebSocket API on localhost:8765
  └── Reads a "control file" (SQLite flags table) to honour UI commands

PROCESS 2 — Control UI (Independent Web App)
  ├── Runs as a separate FastAPI server on localhost:8766
  ├── Serves a single-page HTML/JS dashboard (no npm, no Node, no build step)
  ├── Reads ONLY from the shared SQLite database and Engine REST API
  ├── Writes control commands back to the SQLite flags table
  └── Can be started / stopped without affecting the Trading Engine
```

### Technology Stack — 100% Open-Source, Windows-Native, Zero-Install Infra
| Layer | Library | Purpose |
|---|---|---|
| Language | Python 3.11+ | Core runtime |
| Database | SQLite 3 (built-in) + SQLAlchemy 2.0 | Persistence, state, IPC |
| Async runtime | asyncio + aiohttp | All network I/O |
| Task scheduling | APScheduler 3.x | Cron-style job scheduling |
| Broker — Schwab | `schwab-py` (open-source OAuth2 wrapper) | US equities, options |
| Broker — Robinhood | `robin_stocks` | US equities, crypto, 24/7 |
| Market data | `yfinance`, `pandas-ta` | Historical + indicator data |
| Options math | `py_vollib_vectorized` | Greeks, IV surface |
| ML / Quant | `scikit-learn`, `hmmlearn`, `statsmodels`, `scipy` | Regime detection, stats |
| Portfolio opt. | `PyPortfolioOpt` | Mean-variance, Kelly sizing |
| LLM (local) | `ollama` Python SDK | Sentiment, SEC analysis |
| API server | `FastAPI` + `uvicorn` | Engine API + UI server |
| UI | Vanilla HTML + CSS + JavaScript (served by FastAPI) | Dashboard, no build tools |
| Logging | Python `logging` + `structlog` | JSON structured logs |
| Type checking | `mypy`, `ruff` | Code quality |
| Testing | `pytest`, `pytest-asyncio` | Unit + integration tests |
| Windows service | `NSSM` (Non-Sucking Service Manager, free) | Keeps engine alive 24/7 |

### Project Directory Structure (create this first)
```
C:\TradingSystem\
├── engine\                     # Trading Engine process
│   ├── main.py                 # Entry point — starts Engine + APScheduler + API
│   ├── config.py               # All constants, env vars, tunable params
│   ├── database\
│   │   ├── models.py           # SQLAlchemy ORM models
│   │   ├── session.py          # DB session factory
│   │   └── migrations.py      # Auto-creates / upgrades schema on startup
│   ├── brokers\
│   │   ├── base_broker.py      # Abstract base class
│   │   ├── schwab_broker.py    # Schwab implementation
│   │   ├── robinhood_broker.py # Robinhood implementation
│   │   └── mock_broker.py      # Paper-trading mock
│   ├── data\
│   │   ├── market_data.py      # Async data fetchers
│   │   ├── options_data.py     # Options chain + Greeks
│   │   └── macro_data.py       # FRED, economic calendar
│   ├── strategies\
│   │   ├── base_strategy.py    # Abstract BaseStrategy
│   │   ├── equity\             # All equity strategies
│   │   ├── options\            # All options strategies
│   │   └── cash_mgmt\          # Money market sweep
│   ├── risk\
│   │   ├── risk_manager.py     # Pre-trade check pipeline
│   │   ├── tax_engine.py       # Lot tracking, TLH, wash-sale
│   │   └── compliance.py       # PDT, leverage, sector limits
│   ├── meta_brain\
│   │   ├── regime_detector.py  # HMM market regime
│   │   ├── allocator.py        # Thompson Sampling bandit
│   │   └── llm_analyst.py      # Ollama integration
│   ├── execution\
│   │   ├── order_router.py     # Smart Order Router
│   │   └── execution_engine.py # Submit + log trades
│   ├── scheduler\
│   │   └── jobs.py             # All APScheduler job definitions
│   └── api\
│       └── engine_api.py       # FastAPI app exposed on :8765
│
├── ui\                         # Control UI process (independent)
│   ├── ui_server.py            # FastAPI serving dashboard on :8766
│   └── static\
│       ├── index.html          # Single-page dashboard
│       ├── dashboard.js        # All UI logic, charts, WebSocket
│       └── styles.css          # Dashboard styling
│
├── shared\
│   └── trading.db              # SQLite — the ONLY shared resource between processes
│
├── logs\                       # Rotating log files
├── data_cache\                 # Parquet feature store (local files)
├── requirements.txt
├── .env                        # Secrets — never commit
├── .env.example
├── run_engine.bat              # One-click start trading engine
├── run_ui.bat                  # One-click start UI
└── install_service.bat         # Registers engine as Windows service via NSSM
```

### Inter-Process Communication Design
The two processes NEVER import from each other. They communicate exclusively through:
1. **SQLite `control_flags` table** — UI writes flags; Engine reads them every cycle
2. **Engine REST API on localhost:8765** — UI polls for live data
3. **Engine WebSocket on ws://localhost:8765/ws** — UI receives real-time PnL ticks

---

## PHASE 0 — PROJECT BOOTSTRAP

```
Create the complete project scaffold for an autonomous trading system on Windows.

TASK 1 — Create directory structure:
Create all directories listed in the System Overview above under C:\TradingSystem\.
Create empty __init__.py in every Python package directory.

TASK 2 — Create requirements.txt with these exact packages:
fastapi==0.111.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.30
aiohttp==3.9.5
aiofiles==23.2.1
apscheduler==3.10.4
schwab-py==1.2.0
robin_stocks==3.0.4
yfinance==0.2.40
pandas==2.2.2
pandas-ta==0.3.14b
numpy==1.26.4
scipy==1.13.0
scikit-learn==1.5.0
hmmlearn==0.3.2
statsmodels==0.14.2
pyportfolioopt==1.5.5
py_vollib_vectorized==0.1.2
ollama==0.2.1
structlog==24.2.0
python-dotenv==1.0.1
httpx==0.27.0
websockets==12.0
mypy==1.10.0
ruff==0.4.7
pytest==8.2.2
pytest-asyncio==0.23.7

TASK 3 — Create .env.example:
SCHWAB_APP_KEY=
SCHWAB_APP_SECRET=
SCHWAB_CALLBACK_URL=https://127.0.0.1
SCHWAB_ACCOUNT_HASH=
ROBINHOOD_USERNAME=
ROBINHOOD_PASSWORD=
ROBINHOOD_TOTP_SECRET=
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
DB_PATH=C:/TradingSystem/shared/trading.db
LOG_DIR=C:/TradingSystem/logs
DATA_CACHE_DIR=C:/TradingSystem/data_cache
IS_LIVE=false
ENGINE_PORT=8765
UI_PORT=8766
PDT_EQUITY_BUFFER=26500
MAX_SINGLE_POSITION_PCT=0.10
MAX_SECTOR_PCT=0.35
MAX_CRYPTO_PCT=0.15
MAX_PORTFOLIO_LEVERAGE=2.0
INTRADAY_DRAWDOWN_HALT_PCT=0.02
INTRADAY_DRAWDOWN_CLOSE_PCT=0.04
MAX_CORRELATION_THRESHOLD=0.75
ATR_MULTIPLIER=2.0
KELLY_FRACTION=0.25
TLH_MIN_LOSS_THRESHOLD=500
PROFIT_SWEEP_THRESHOLD=30000
MONEY_MARKET_TICKER=SWVXX
TIMEZONE=America/New_York

TASK 4 — Create engine/config.py:
Load all .env variables using python-dotenv.
Define a Config dataclass with every variable above, with correct Python types.
Add a PROXY_SWAP_MAP dict: {"SPY":"VOO","QQQ":"VGT","AMD":"NVDA","GLD":"IAU","IWM":"VB"}
Add a STRATEGY_REGISTRY list of strategy IDs that will be populated later.
Add a MARKET_OPEN time (09:30 ET) and MARKET_CLOSE time (16:00 ET).

TASK 5 — Create run_engine.bat:
@echo off
cd /d C:\TradingSystem
python engine\main.py >> logs\engine_stdout.log 2>&1

TASK 6 — Create run_ui.bat:
@echo off
cd /d C:\TradingSystem
python ui\ui_server.py >> logs\ui_stdout.log 2>&1

TASK 7 — Create install_service.bat (uses NSSM):
@echo off
nssm install TradingEngine python "C:\TradingSystem\engine\main.py"
nssm set TradingEngine AppDirectory C:\TradingSystem
nssm set TradingEngine AppStdout C:\TradingSystem\logs\service.log
nssm set TradingEngine AppStderr C:\TradingSystem\logs\service_err.log
nssm set TradingEngine Start SERVICE_AUTO_START

ACCEPTANCE CRITERIA:
- pip install -r requirements.txt completes with no errors
- All directories and __init__.py files exist
- python -c "from engine.config import Config; c=Config(); print(c.DB_PATH)" prints the path
- Both .bat files are syntactically valid
```

---

## PHASE 1 — DATABASE LAYER (SQLite + SQLAlchemy)

```
Build the complete SQLite database layer for the trading system.
File: engine/database/models.py

Use SQLAlchemy 2.0 declarative syntax with type annotations on every column.
The database file path comes from Config.DB_PATH.
All timestamps are stored as UTC ISO-8601 strings.
Use SQLite pragma: WAL mode (faster concurrent reads), foreign keys ON.

CREATE THESE EXACT TABLES:

TABLE 1 — trades
  id: Integer, primary key, autoincrement
  symbol: String(20), not null
  asset_class: String(20), not null  # EQUITY / OPTION / CRYPTO / ETF / CASH
  broker: String(20), not null       # SCHWAB / ROBINHOOD / MOCK
  strategy_id: String(50), not null
  direction: String(10), not null    # BUY / SELL / BUY_TO_OPEN / SELL_TO_CLOSE etc
  qty: Float, not null
  order_type: String(20), not null   # MARKET / LIMIT / STOP / STOP_LIMIT
  limit_price: Float, nullable
  fill_price: Float, nullable
  commission: Float, default 0.0
  slippage_bps: Float, nullable
  status: String(20), default "PENDING"   # PENDING/FILLED/CANCELLED/REJECTED
  broker_order_id: String(100), nullable
  fill_timestamp: String(50), nullable
  created_at: String(50), not null
  notes: Text, nullable

TABLE 2 — positions
  id: Integer, primary key, autoincrement
  symbol: String(20), unique, not null
  asset_class: String(20), not null
  broker: String(20), not null
  current_qty: Float, default 0.0
  average_cost: Float, default 0.0
  last_price: Float, nullable
  unrealized_pl: Float, default 0.0
  unrealized_pl_pct: Float, default 0.0
  realized_pl: Float, default 0.0
  days_held: Integer, default 0
  strategy_id: String(50), nullable
  stop_price: Float, nullable
  take_profit_price: Float, nullable
  delta: Float, nullable             # Options Greeks
  theta: Float, nullable
  vega: Float, nullable
  gamma: Float, nullable
  option_expiry: String(20), nullable
  option_strike: Float, nullable
  option_type: String(5), nullable   # CALL / PUT
  last_updated: String(50), not null

TABLE 3 — tax_lots
  id: Integer, primary key, autoincrement
  symbol: String(20), not null
  acquisition_date: String(20), not null
  qty: Float, not null
  cost_basis: Float, not null
  lot_method: String(10), default "FIFO"   # FIFO / HIFO / LIFO
  is_closed: Boolean, default False
  close_date: String(20), nullable
  close_price: Float, nullable
  realized_gain_loss: Float, nullable
  is_long_term: Boolean, nullable    # True if held > 365 days
  wash_sale_disallowed: Float, default 0.0

TABLE 4 — wash_sale_blacklist
  id: Integer, primary key, autoincrement
  symbol: String(20), not null, unique
  loss_realized_date: String(20), not null
  expiration_date: String(20), not null     # loss_date + 31 days
  loss_amount: Float, not null
  proxy_used: String(20), nullable

TABLE 5 — tax_harvest_log
  id: Integer, primary key, autoincrement
  harvest_date: String(20), not null
  symbol_sold: String(20), not null
  proxy_bought: String(20), not null
  qty: Float, not null
  loss_captured: Float, not null
  estimated_tax_saving: Float, nullable
  created_at: String(50), not null

TABLE 6 — strategy_performance
  id: Integer, primary key, autoincrement
  strategy_id: String(50), unique, not null
  display_name: String(100), not null
  asset_class: String(20), not null
  total_trades: Integer, default 0
  winning_trades: Integer, default 0
  win_rate: Float, default 0.0
  total_pnl: Float, default 0.0
  avg_hold_days: Float, default 0.0
  sharpe_ratio: Float, nullable
  max_drawdown: Float, default 0.0
  current_weight: Float, default 0.0   # 0.0 to 1.0 — set by Meta-Brain bandit
  bandit_alpha: Float, default 1.0     # Thompson Sampling Beta(alpha, beta)
  bandit_beta: Float, default 1.0
  is_enabled: Boolean, default True    # UI-controllable kill switch
  last_updated: String(50), not null

TABLE 7 — market_regime_log
  id: Integer, primary key, autoincrement
  log_date: String(20), unique, not null
  hmm_state: String(30), not null   # BULL_TREND / BEAR_TREND / SIDEWAYS_LOW / SIDEWAYS_HIGH / CRASH_RISK / RECOVERY
  hmm_probabilities: Text, not null  # JSON string of state probabilities
  vix_level: Float, nullable
  sp500_return_5d: Float, nullable
  yield_spread_10y2y: Float, nullable
  put_call_ratio: Float, nullable
  macro_score: Float, nullable
  created_at: String(50), not null

TABLE 8 — control_flags
  id: Integer, primary key, autoincrement
  flag_key: String(100), unique, not null
  flag_value: String(500), not null
  updated_by: String(50), default "SYSTEM"
  updated_at: String(50), not null

  PRE-POPULATE with these default rows on first run:
  ("trading_enabled", "true", "SYSTEM")
  ("shadow_mode", "true", "SYSTEM")         # Paper trading by default — SAFETY
  ("llm_analysis_enabled", "true", "SYSTEM")
  ("tlh_enabled", "true", "SYSTEM")
  ("crypto_enabled", "false", "SYSTEM")
  ("options_enabled", "false", "SYSTEM")
  ("meta_brain_enabled", "true", "SYSTEM")
  ("max_position_size_override", "", "SYSTEM")   # Empty = use config default
  ("halt_reason", "", "SYSTEM")
  ("engine_status", "STOPPED", "SYSTEM")

TABLE 9 — alpha_signals_log
  id: Integer, primary key, autoincrement
  signal_id: String(50), not null
  strategy_id: String(50), not null
  symbol: String(20), not null
  direction: String(10), not null
  strength: Float, not null           # 0.0 to 1.0
  conviction: String(10), not null    # LOW / MEDIUM / HIGH
  recommended_size: Float, nullable
  stop_price: Float, nullable
  take_profit_price: Float, nullable
  metadata_json: Text, nullable       # JSON blob of strategy-specific info
  acted_on: Boolean, default False
  blocked_by: String(100), nullable   # Which risk rule blocked it, if any
  outcome_pnl: Float, nullable        # Filled in when position closes
  created_at: String(50), not null

TABLE 10 — portfolio_snapshots
  id: Integer, primary key, autoincrement
  snapshot_time: String(50), unique, not null
  total_equity: Float, not null
  cash_balance: Float, not null
  positions_value: Float, not null
  daily_pnl: Float, default 0.0
  total_pnl: Float, default 0.0
  num_open_positions: Integer, default 0
  drawdown_pct: Float, default 0.0
  sharpe_rolling_30d: Float, nullable
  var_99: Float, nullable
  regime_state: String(30), nullable

TABLE 11 — compliance_audit_log
  id: Integer, primary key, autoincrement
  event_time: String(50), not null
  rule_name: String(100), not null
  symbol: String(20), nullable
  order_direction: String(10), nullable
  order_qty: Float, nullable
  outcome: String(20), not null    # BLOCKED / WARNED / PASSED
  reason: Text, not null
  strategy_id: String(50), nullable

FILE: engine/database/session.py
Create a SessionFactory using create_engine with SQLite.
Enable WAL mode via event listener: "PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;"
Provide get_session() context manager using Session.
Provide async_get_session() for FastAPI dependency injection.

FILE: engine/database/migrations.py
Function auto_migrate(engine) that calls Base.metadata.create_all(engine).
Then checks if control_flags has the default rows; if not, inserts them.
Called once at engine startup.

ACCEPTANCE CRITERIA:
- python -c "from engine.database.migrations import auto_migrate; ..." creates all 11 tables
- All columns have correct types; foreign key pragma is ON
- control_flags table has all 10 default rows after first run
- Running auto_migrate twice does not error or duplicate rows
```

---

## PHASE 2 — BROKER LAYER

```
Build the complete broker abstraction layer.

FILE: engine/brokers/base_broker.py
Create abstract base class BaseBroker(ABC) with these abstract async methods:
  - async get_quote(symbol: str) -> dict  # Returns {symbol, bid, ask, last, volume, timestamp}
  - async get_option_chain(symbol: str, expiry: str) -> list[dict]
  - async submit_order(order: OrderRequest) -> OrderResult
  - async cancel_order(broker_order_id: str) -> bool
  - async get_positions() -> list[dict]
  - async get_account_balance() -> dict  # {total_equity, cash, buying_power}
  - async get_order_status(broker_order_id: str) -> dict

Create these dataclasses in the same file:
  OrderRequest:
    symbol: str
    direction: str           # BUY / SELL / BUY_TO_OPEN / SELL_TO_CLOSE
    qty: float
    order_type: str          # MARKET / LIMIT / STOP
    limit_price: float | None = None
    stop_price: float | None = None
    asset_class: str = "EQUITY"
    strategy_id: str = ""
    time_in_force: str = "DAY"

  OrderResult:
    success: bool
    broker_order_id: str | None
    fill_price: float | None
    fill_qty: float | None
    status: str
    error_message: str | None
    raw_response: dict | None

Add a circuit_breaker decorator that:
  - Tracks consecutive errors per broker instance in self._error_count
  - If error_count >= 3 within 60 seconds, sets self._circuit_open = True
  - Logs a CRITICAL warning and stops routing orders to that broker
  - Resets after 5 minutes

Add retry_async decorator:
  - Retries up to 3 times with exponential backoff: 1s, 2s, 4s + random jitter
  - Only retries on aiohttp.ClientError and asyncio.TimeoutError

FILE: engine/brokers/schwab_broker.py
Implement SchwabBroker(BaseBroker) using the `schwab-py` open-source library.
  - Import: import schwab
  - OAuth2 flow: use schwab.auth.client_from_token_file() for stored tokens.
  - Token file stored at: C:\TradingSystem\schwab_token.json
  - If token file missing, run schwab.auth.client_from_manual_flow() once interactively.
  - Implement get_quote() using client.get_quote(symbol).json()
  - Implement submit_order() using client.place_order() with schwab.orders builder.
  - Handle Schwab-specific order status codes (FILLED, WORKING, REJECTED, CANCELLED).
  - Implement get_option_chain() using client.get_option_chain(symbol).
  - Implement get_account_balance() parsing Schwab's account JSON structure.
  - Log every API call with elapsed time in milliseconds.
  - Token refresh: check token expiry on every call; refresh proactively if < 5 min remaining.

FILE: engine/brokers/robinhood_broker.py
Implement RobinhoodBroker(BaseBroker) using `robin_stocks` library.
  - Import: import robin_stocks.robinhood as rh
  - Login: rh.login(username, password, mfa_code=pyotp.now(TOTP_SECRET)) — store session.
  - Re-login automatically if session expires (catch AuthenticationError).
  - Implement get_quote() using rh.stocks.get_latest_price() and rh.stocks.get_quotes().
  - Implement submit_order() using rh.orders.order() with correct order_type mapping.
  - Implement get_positions() using rh.account.build_holdings().
  - Implement get_account_balance() using rh.account.build_user_profile().
  - Handle fractional shares: Robinhood supports fractional; pass fractional=True when qty < 1.
  - Crypto routing: use rh.crypto.order_buy_crypto_by_price() for crypto symbols.
  - NOTE: Robinhood has no official options API via robin_stocks; log warning and return error for options orders.

FILE: engine/brokers/mock_broker.py
Implement MockBroker(BaseBroker) for Shadow Mode (paper trading):
  - Maintain an in-memory dict of virtual positions and a virtual cash balance (default $50,000).
  - Persist virtual state to the SQLite positions table with broker="MOCK".
  - get_quote(): delegate to a real market data function (yfinance) to get real prices.
  - submit_order(): simulate fills using last price + slippage model:
      MARKET order: fill at last_price * (1 + slippage) where slippage ~ N(0, 0.0003)
      LIMIT order: fill only if limit_price >= ask (buy) or limit_price <= bid (sell)
  - Track MockBroker virtual P&L separately in portfolio_snapshots with broker="MOCK".
  - Log every mock fill with prefix "[SHADOW]" so it's visually distinct in logs.

BROKER FACTORY:
Create engine/brokers/broker_factory.py:
  - get_broker(broker_name: str, config: Config) -> BaseBroker
  - Returns correct broker instance based on name string
  - Validates IS_LIVE flag: if IS_LIVE=false, always return MockBroker regardless of name

ACCEPTANCE CRITERIA:
- All three brokers instantiate without error
- MockBroker.submit_order(BUY 1 AAPL MARKET) returns OrderResult with success=True and fill_price set
- MockBroker virtual cash decreases by fill_price after buy
- SchwabBroker raises descriptive error (not generic exception) when SCHWAB_APP_KEY is empty
- circuit_breaker test: mock 3 consecutive aiohttp errors; confirm broker._circuit_open == True
```

---

## PHASE 3 — MARKET DATA ENGINE

```
Build the async market data ingestion engine.

FILE: engine/data/market_data.py

Use aiohttp for all async HTTP calls. Use yfinance for historical data (sync — run in executor).
Cache all fetched data to local Parquet files under data_cache/ for offline fallback.

Implement these async functions:

1. async get_historical_ohlcv(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame
   - Fetches via yfinance in a thread pool executor (asyncio.get_event_loop().run_in_executor)
   - Columns: open, high, low, close, volume — all lowercase
   - Returns DataFrame indexed by date
   - Cache to: data_cache/{symbol}_{period}_{interval}.parquet
   - If yfinance fails, load from cache (with staleness warning in log if > 1 day old)

2. async get_realtime_quote(symbol: str) -> dict
   - Try yfinance Ticker.fast_info first (most recent close/market price)
   - Return: {symbol, price, bid, ask, volume, market_cap, timestamp}
   - If market is closed, return last known price with is_market_open: False flag

3. async get_batch_quotes(symbols: list[str]) -> dict[str, dict]
   - Fetch multiple quotes concurrently using asyncio.gather()
   - Rate-limit: max 10 concurrent yfinance calls (use asyncio.Semaphore(10))

4. async calculate_indicators(df: pd.DataFrame) -> pd.DataFrame
   - Using pandas_ta, add these columns to the dataframe:
     - RSI(14): column "rsi_14"
     - MACD(12,26,9): columns "macd", "macd_signal", "macd_hist"
     - Bollinger Bands(20,2): "bbl", "bbu", "bbw" (width)
     - ATR(14): column "atr_14"
     - EMA(9), EMA(21), EMA(50): columns "ema_9", "ema_21", "ema_50"
     - ADX(14): column "adx_14"
     - OBV: column "obv"
     - Stochastic(14,3): "stoch_k", "stoch_d"
   - Return the enriched DataFrame (no NaN rows dropped — strategies handle NaN)

5. async get_vix_data() -> dict
   - Fetch ^VIX from yfinance
   - Return {vix_current, vix_5d_avg, vix_20d_avg, percentile_rank_1y}

6. async get_spy_data(lookback_days: int = 252) -> pd.DataFrame
   - Fetch SPY OHLCV + indicators for HMM training
   - Add column "daily_return" = close.pct_change()

7. async get_macro_data() -> dict
   - Fetch from FRED using requests (synchronous, run in executor):
     - 10Y Treasury: series "DGS10"
     - 2Y Treasury: series "DGS2"
     - Fed Funds Rate: series "FEDFUNDS"
     - CPI YoY: series "CPIAUCSL"
   - Return {yield_10y, yield_2y, yield_spread, fed_funds_rate, cpi_yoy}
   - FRED base URL: https://api.stlouisfed.org/fred/series/observations
   - Cache result for 24 hours

8. async get_economic_calendar_today() -> list[dict]
   - Scrape https://finance.yahoo.com/calendar/earnings using aiohttp + basic HTML parsing
   - Return list of {symbol, event_type, expected_date} for today + next 5 trading days
   - No external library needed — parse basic HTML

FILE: engine/data/options_data.py

1. async get_option_chain(symbol: str) -> pd.DataFrame
   - Use yfinance Ticker.option_chain(expiry) for nearest 3 expiry dates
   - Columns: contractSymbol, strike, expiry, option_type, bid, ask, iv, volume, openInterest
   - Calculate mid-price = (bid + ask) / 2
   - Return single DataFrame with all expiries stacked

2. calculate_greeks(option_row: pd.Series, spot_price: float, risk_free_rate: float) -> dict
   - Use py_vollib_vectorized to calculate Delta, Gamma, Theta, Vega, Rho
   - Input: spot, strike, expiry (as days_to_expiry float), iv, option_type ('c'/'p')
   - Return: {delta, gamma, theta, vega, rho, iv, intrinsic_value, time_value}

3. async get_portfolio_greeks(positions: list[dict]) -> dict
   - For all option positions, aggregate net Greeks
   - Return: {net_delta, net_gamma, net_theta, net_vega, positions_count}

ACCEPTANCE CRITERIA:
- get_historical_ohlcv("AAPL", "6mo", "1d") returns DataFrame with > 100 rows and all indicator columns
- get_batch_quotes(["AAPL","MSFT","GOOGL"]) completes in < 5 seconds
- Parquet cache file created after first fetch; second call reads from cache
- calculate_greeks returns delta between -1 and 1, theta is negative for long options
- get_vix_data() returns dict with all 4 keys
```

---

## PHASE 4 — RISK MANAGEMENT & TAX ENGINE

```
Build the multi-layer risk management and tax optimization system.

FILE: engine/risk/risk_manager.py

Create class RiskManager with a single async entry point:
  async def check_order(order: OrderRequest, portfolio_state: dict, db_session) -> RiskCheckResult

RiskCheckResult dataclass:
  approved: bool
  blocked_by: str | None   # Rule name that blocked it
  warnings: list[str]
  modified_qty: float | None  # If risk manager reduces position size

Implement ALL checks as private async methods called in sequence.
If ANY check returns False, immediately set approved=False, log to compliance_audit_log, and return.
ORDER OF CHECKS (must execute in this exact order):

CHECK 1 — _check_trading_enabled(db_session) -> bool
  Read control_flags table: if "trading_enabled" == "false" → BLOCK. Reason: "System halt by operator"

CHECK 2 — _check_shadow_mode(order, db_session) -> bool
  If "shadow_mode" == "true" AND order.broker != "MOCK" → BLOCK.
  Reason: "Shadow mode active — route to MockBroker only"

CHECK 3 — _check_pdt_rule(portfolio_state, db_session) -> bool
  Count trades with status=FILLED in last 5 calendar days with hold_time < 1 day (day-trades).
  If day_trade_count >= 3 AND total_equity < PDT_EQUITY_BUFFER → BLOCK.
  Reason: "PDT Rule: 3 day-trades used, equity below $25,000 buffer"

CHECK 4 — _check_wash_sale(order, db_session) -> tuple[bool, str | None]
  Query wash_sale_blacklist for order.symbol.
  If found and expiration_date > today → BLOCK if direction is BUY.
  Also check if we're selling at a loss AND bought same symbol within 30 days prior → BLOCK and log.
  Return proxy suggestion from PROXY_SWAP_MAP if available.

CHECK 5 — _check_position_concentration(order, portfolio_state) -> bool
  If order is BUY: calculate would-be position value / total_equity.
  If > MAX_SINGLE_POSITION_PCT → reduce qty to fit within limit (set modified_qty).
  Log warning but do NOT block; just resize.

CHECK 6 — _check_sector_concentration(order, portfolio_state) -> bool
  Get sector for order.symbol via yfinance Ticker.info["sector"].
  Calculate current sector exposure + new order exposure as % of NAV.
  If > MAX_SECTOR_PCT → BLOCK. Reason: "Sector concentration limit exceeded"

CHECK 7 — _check_liquidity(order) -> bool
  Fetch 20-day average volume for symbol.
  If order.qty * fill_price > 0.05 * avg_daily_volume_usd → BLOCK.
  Reason: "Order exceeds 5% of 20-day ADTV — liquidity risk"

CHECK 8 — _check_portfolio_correlation(order, portfolio_state) -> bool
  Fetch 60-day returns for order.symbol and all existing position symbols.
  Calculate Pearson correlation with existing holdings.
  If any existing position correlation > MAX_CORRELATION_THRESHOLD → WARN (do not block).
  Log warning with correlated symbol name.

CHECK 9 — _check_crypto_enabled(order, db_session) -> bool
  If order.asset_class == "CRYPTO" AND control_flags["crypto_enabled"] == "false" → BLOCK.

CHECK 10 — _check_options_enabled(order, db_session) -> bool
  If order.asset_class == "OPTION" AND control_flags["options_enabled"] == "false" → BLOCK.

CHECK 11 — _check_intraday_drawdown(portfolio_state, db_session) -> bool
  Get today's opening equity from portfolio_snapshots (earliest snapshot today).
  Calc drawdown = (opening_equity - current_equity) / opening_equity
  If drawdown > INTRADAY_DRAWDOWN_HALT_PCT → set trading_enabled=false in DB; BLOCK all orders.
  If drawdown > INTRADAY_DRAWDOWN_CLOSE_PCT → BLOCK all new entries (only allow exits).

CHECK 12 — _check_leverage(order, portfolio_state) -> bool
  Calculate total_notional_exposure / total_equity (after this order).
  If > MAX_PORTFOLIO_LEVERAGE → BLOCK. Reason: "Leverage limit exceeded"

FILE: engine/risk/tax_engine.py

Create class TaxEngine:

1. async record_lot(symbol: str, qty: float, cost_basis: float, lot_method: str = "FIFO", db_session)
   - Creates a new tax_lot record on every buy fill.

2. async close_lot(symbol: str, qty: float, sell_price: float, db_session) -> dict
   - Selects lots to close based on lot_method (FIFO = oldest first, HIFO = highest cost first)
   - Marks lots as closed; calculates realized_gain_loss per lot
   - Sets is_long_term = True if (close_date - acquisition_date).days > 365
   - Returns {total_realized_pnl, stcg, ltcg, lots_closed: list}

3. async scan_for_harvest_opportunities(portfolio_state: dict, db_session) -> list[dict]
   - For each open position with unrealized_pl < -TLH_MIN_LOSS_THRESHOLD:
     - Check wash sale blacklist: symbol not in blacklist
     - Check proxy exists in PROXY_SWAP_MAP
     - Return list of {symbol, unrealized_loss, proxy_ticker, estimated_tax_saving}
   - estimated_tax_saving = unrealized_loss * 0.35 (placeholder 35% marginal rate)

4. async execute_harvest(symbol: str, proxy: str, qty: float, broker: BaseBroker, db_session)
   - Sell symbol at market
   - Add to wash_sale_blacklist with expiration = today + 31 days
   - Immediately buy proxy at market
   - Log to tax_harvest_log

5. async get_ytd_tax_summary(db_session) -> dict
   - Aggregate all closed lots for current year
   - Return {stcg_total, ltcg_total, wash_sale_disallowed_total, harvested_losses, net_taxable_gains}

6. async generate_form_8949_csv(year: int, db_session) -> str
   - Returns CSV string in IRS Form 8949 format
   - Columns: Description, Date Acquired, Date Sold, Proceeds, Cost Basis, Adjustment Code, Gain/Loss

ACCEPTANCE CRITERIA:
- RiskManager blocks a BUY order for a symbol in wash_sale_blacklist
- RiskManager blocks trading when trading_enabled flag is "false"
- PDT check correctly counts day-trades in last 5 days
- TaxEngine.close_lot() with HIFO selects the highest-cost lot first
- scan_for_harvest_opportunities returns empty list when proxy unavailable
- generate_form_8949_csv returns valid CSV with correct columns
```

---

## PHASE 5 — STRATEGY IMPLEMENTATIONS

```
Build the complete strategy arsenal. All strategies inherit from BaseStrategy.

FILE: engine/strategies/base_strategy.py

Create abstract BaseStrategy(ABC):
  Required attributes (set in __init__):
    strategy_id: str
    display_name: str
    asset_class: str
    description: str
    default_weight: float

  Required abstract methods:
    @abstractmethod
    async def generate_signals(self, data: pd.DataFrame, portfolio_state: dict) -> list[SignalEvent]

    @abstractmethod
    def calculate_position_size(self, signal: SignalEvent, portfolio_state: dict) -> float

  Provided concrete methods:
    is_enabled(db_session) -> bool: reads strategy_performance.is_enabled for this strategy_id
    log_signal(signal, acted_on, blocked_by, db_session): writes to alpha_signals_log

Create SignalEvent dataclass:
  signal_id: str  (auto-generate UUID)
  strategy_id: str
  symbol: str
  direction: str           # BUY / SELL / HOLD / BUY_TO_OPEN / SELL_TO_CLOSE
  strength: float          # 0.0 to 1.0
  conviction: str          # LOW / MEDIUM / HIGH  (< 0.4 = LOW, 0.4-0.7 = MEDIUM, > 0.7 = HIGH)
  recommended_size: float  # Dollar amount
  stop_price: float | None
  take_profit_price: float | None
  metadata: dict
  created_at: str

Kelly position sizing helper:
  kelly_position_size(win_rate: float, avg_win: float, avg_loss: float, 
                      portfolio_equity: float, kelly_fraction: float = 0.25) -> float
  Formula: f = (win_rate/avg_loss - (1-win_rate)/avg_win) * kelly_fraction
  Cap at 10% of portfolio_equity; floor at $500.

FILE: engine/strategies/equity/trend_following.py
Class TrendFollowingStrategy(BaseStrategy):
  strategy_id = "EQ_TREND_FOLLOW"
  
  generate_signals logic:
  - Require minimum 60 rows in DataFrame
  - BUY signal conditions (ALL must be true):
      1. EMA-9 crosses above EMA-21 (current bar cross: ema_9[-1] > ema_21[-1] AND ema_9[-2] <= ema_21[-2])
      2. EMA-21 > EMA-50 (trend confirmation)
      3. ADX-14 > 25 (strong trend, not whipsaw)
      4. Price > EMA-50 (above long-term trend)
      5. RSI-14 between 45 and 75 (not overbought)
  - SELL signal conditions (ANY of these):
      1. EMA-9 crosses below EMA-21
      2. ADX < 20 (trend weakening)
      3. RSI > 78 (overbought exit)
  - Signal strength = ADX value / 100 (normalised)
  - Stop price = last close - (2 * ATR-14)
  - Take profit = last close + (4 * ATR-14)  [2:1 reward/risk]

FILE: engine/strategies/equity/mean_reversion.py
Class MeanReversionStrategy(BaseStrategy):
  strategy_id = "EQ_MEAN_REV"
  
  generate_signals logic:
  - BUY signal (Bollinger Band bounce):
      1. Price closes below BBL (lower band)
      2. RSI-14 < 32 (oversold)
      3. Stochastic-K < 25 (oversold confirmation)
      4. Next bar opens back above BBL (wait for confirmation)
      5. NOT in BEAR_TREND or CRASH_RISK regime
  - SELL signal:
      1. Price closes above BBU (upper band) OR
      2. Price reaches BBM (mean reversion complete) + RSI > 65
  - Strength = (BBM - current_price) / (BBM - BBL) — how far from mean
  - Stop = BBL - (0.5 * ATR-14)

FILE: engine/strategies/equity/stat_arb.py
Class StatArbStrategy(BaseStrategy):
  strategy_id = "EQ_STAT_ARB"
  PAIRS = [("SPY", "IVV"), ("QQQ", "ONEQ"), ("GLD", "IAU"), ("TLT", "IEF")]
  
  generate_signals logic (for each pair):
  - Fetch 90-day close prices for both legs
  - Run Engle-Granger cointegration test (statsmodels.coint)
  - If p-value < 0.05 (cointegrated):
      - Calculate spread = log(price_A) - beta * log(price_B)
      - Calculate Z-score of spread: (spread - mean) / std using 60-day rolling window
      - BUY leg A, SELL leg B when Z-score < -2.0
      - SELL leg A, BUY leg B when Z-score > +2.0
      - EXIT when Z-score crosses 0 (mean reversion complete)
  - Pair trade sizing: equal dollar amount each leg

FILE: engine/strategies/equity/flash_crash.py
Class FlashCrashStrategy(BaseStrategy):
  strategy_id = "EQ_FLASH_CRASH"
  TARGETS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA"]
  
  generate_signals logic:
  - Only active: 09:28 AM to 09:35 AM ET on market open
  - For each symbol: place 5 limit BUY orders at:
      [-5%, -8%, -12%, -16%, -20%] below previous close
  - Order type: LIMIT (passive — only fills if crash occurs)
  - Qty: $500 per level (configurable)
  - Cancel all unfilled flash-crash orders at 10:00 AM
  - Take-profit: prior close (mean reversion expected)

FILE: engine/strategies/equity/earnings_drift.py
Class EarningsDriftStrategy(BaseStrategy):
  strategy_id = "EQ_EARNINGS"
  
  generate_signals logic:
  - At 4:15 PM, check economic_calendar for earnings in next 1-3 days
  - For each earnings symbol with LLM sentiment_score > 65 (from llm_analyst):
      - BUY 3 days before earnings
      - SELL on day of earnings (before announcement — capture pre-announcement drift)
  - Position size: 2% of NAV per trade (earnings size capped)
  - Stop loss: -3% below entry

FILE: engine/strategies/cash_mgmt/money_market_sweep.py
Class MoneyMarketSweepStrategy(BaseStrategy):
  strategy_id = "CASH_SWEEP"
  
  generate_signals logic:
  - Runs at 3:50 PM ET every trading day
  - Get cash_balance from portfolio_state
  - If cash_balance > 1000 (leave $500 buffer):
      - Generate BUY signal for SWVXX (or config MONEY_MARKET_TICKER)
      - Qty = (cash_balance - 500) / current_nav (money market nav ≈ $1.00)
  - Runs at 9:31 AM ET: if holding SWVXX → SELL all to restore buying power

ACCEPTANCE CRITERIA:
- TrendFollowingStrategy.generate_signals() returns BUY on a mock DataFrame with all conditions met
- MeanReversionStrategy returns SELL when price is above BBU
- StatArbStrategy cointegration test runs without error on real SPY/IVV data
- FlashCrashStrategy only generates signals between 09:28 and 09:35
- MoneyMarketSweepStrategy generates BUY SWVXX when cash_balance = 5000
- All strategies handle DataFrames with NaN values without crashing (use .dropna() carefully)
- kelly_position_size never returns more than 10% of portfolio_equity
```

---

## PHASE 6 — META-BRAIN (AI ORCHESTRATION)

```
Build the central intelligence layer that orchestrates all strategies.

FILE: engine/meta_brain/regime_detector.py
Class MarketRegimeDetector:

  __init__:
    - self.hmm = hmmlearn.hmm.GaussianHMM(n_components=6, covariance_type="diag", n_iter=200)
    - self.state_labels = ["BULL_TREND","BEAR_TREND","SIDEWAYS_LOW","SIDEWAYS_HIGH","CRASH_RISK","RECOVERY"]
    - self.is_trained = False
    - self.last_train_date = None

  async train(self):
    - Fetch 2 years of SPY daily data
    - Fetch VIX data
    - Build feature matrix X with columns: [daily_return, log_volume, vix_norm, atr_norm, macd_hist_norm]
    - Normalise each column: (x - mean) / std
    - Fit self.hmm on X
    - Set self.is_trained = True
    - Log which state index maps to which label using heuristics:
        State with highest mean return → BULL_TREND
        State with lowest mean return → BEAR_TREND / CRASH_RISK (separate by VIX level)
    - Save trained model to data_cache/hmm_model.pkl (pickle)

  async load_or_train(self):
    - Try to load from data_cache/hmm_model.pkl
    - If file missing or > 7 days old → call self.train()

  async get_current_regime(self) -> dict:
    - Fetch last 60 days SPY + VIX data
    - Build feature vector for today
    - Predict state probabilities using hmm.predict_proba()
    - Return {
        state: str (most probable),
        probabilities: dict[str, float],
        bull_probability: float,
        crash_probability: float,
        vix_current: float
      }
    - Save result to market_regime_log table

  async get_regime_multipliers(self) -> dict[str, float]:
    - Returns per-strategy weight multipliers based on current regime:
      BULL_TREND:     {"EQ_TREND_FOLLOW": 1.5, "EQ_MEAN_REV": 0.5, "EQ_STAT_ARB": 1.0, "EQ_EARNINGS": 1.2}
      BEAR_TREND:     {"EQ_TREND_FOLLOW": 0.2, "EQ_MEAN_REV": 1.3, "EQ_STAT_ARB": 1.0, "EQ_EARNINGS": 0.3}
      SIDEWAYS_LOW:   {"EQ_TREND_FOLLOW": 0.3, "EQ_MEAN_REV": 1.5, "EQ_STAT_ARB": 1.5, "EQ_EARNINGS": 0.8}
      CRASH_RISK:     {"EQ_TREND_FOLLOW": 0.0, "EQ_MEAN_REV": 0.0, "EQ_STAT_ARB": 0.5, "EQ_EARNINGS": 0.0}
    (All others default to 1.0)

FILE: engine/meta_brain/allocator.py
Class ThompsonSamplingAllocator:

  async get_allocation(strategy_ids: list[str], regime_multipliers: dict, db_session) -> dict[str, float]:
    - For each strategy_id, fetch bandit_alpha and bandit_beta from strategy_performance table
    - Sample from Beta(alpha, beta) for each strategy
    - Multiply sampled value by regime_multiplier for that strategy
    - Zero out disabled strategies (is_enabled = False)
    - Normalise so weights sum to 1.0
    - Enforce minimum 5% floor for enabled strategies (redistribute from highest-weight)
    - Save updated weights to strategy_performance.current_weight
    - Return dict[strategy_id → weight]

  async update_bandit(strategy_id: str, trade_pnl: float, db_session):
    - If trade_pnl > 0: increment bandit_alpha by 1
    - If trade_pnl <= 0: increment bandit_beta by 1
    - Update record in strategy_performance

FILE: engine/meta_brain/llm_analyst.py
Class LLMAnalyst:

  __init__(config: Config):
    - self.client = ollama.Client(host=config.OLLAMA_BASE_URL)
    - self.model = config.OLLAMA_MODEL
    - self.is_available = False

  async check_availability(self):
    - Try ollama list; if successful set self.is_available = True
    - If Ollama not running: log warning; set is_available = False

  async analyze_news_sentiment(symbol: str, headlines: list[str]) -> dict:
    - Construct prompt:
      "Analyze these news headlines for {symbol}. 
       Return ONLY valid JSON (no markdown):
       {\"sentiment_score\": 0-100, \"direction\": \"BULLISH|BEARISH|NEUTRAL\",
        \"key_factors\": [\"factor1\",\"factor2\"], \"confidence\": 0.0-1.0,
        \"suggested_action\": \"BUY|SELL|HOLD\"}"
    - Call self.client.chat(model, messages=[{role:user, content:prompt}])
    - Parse JSON response; handle malformed JSON gracefully (return neutral defaults)
    - Cache result in alpha_signals_log metadata for 4 hours

  async analyze_earnings_call(symbol: str, transcript_text: str) -> dict:
    - Prompt: extract {"sentiment_score", "guidance_revision": "UP|DOWN|FLAT",
        "revenue_quality": 0-100, "management_tone": "CONFIDENT|CAUTIOUS|NEGATIVE",
        "surprise_factor": "BEAT|MISS|IN_LINE", "recommended_action": "BUY|SELL|HOLD"}
    - If transcript_text > 4000 chars: truncate to first 4000 (context window safety)

  async analyze_10k_risk(symbol: str, filing_text: str) -> dict:
    - Prompt: extract {"risk_score": 0-100 (100=high risk),
        "key_risks": ["risk1","risk2"], "year_over_year_change": "BETTER|WORSE|SAME"}

  async get_market_commentary(regime: dict, macro_data: dict) -> str:
    - Generate 2-sentence plain-English market commentary for dashboard display
    - Include regime state, VIX level, and top macro factor

FILE: engine/meta_brain/portfolio_optimizer.py
Class PortfolioOptimizer:

  async optimize_weights(symbols: list[str], lookback_days: int = 126) -> dict[str, float]:
    - Fetch historical prices for all symbols
    - Use PyPortfolioOpt EfficientFrontier:
        - Expected returns via mean_historical_return()
        - Covariance via CovarianceShrinkage().ledoit_wolf()
        - Objective: max_sharpe()
        - Weight bounds: (0.02, 0.25) per asset
    - Return cleaned weights dict

  async calculate_portfolio_var(portfolio_state: dict, confidence: float = 0.99) -> float:
    - Get 252-day return series for each position
    - Monte Carlo: simulate 5000 portfolio paths using Cholesky decomposition
    - Return 1-day VaR at confidence level as dollar amount

ACCEPTANCE CRITERIA:
- MarketRegimeDetector trains on SPY data without error; get_current_regime returns valid dict
- ThompsonSamplingAllocator weights sum to exactly 1.0 after normalisation
- Disabled strategies receive weight 0.0
- LLMAnalyst.check_availability returns False gracefully when Ollama is not running
- LLMAnalyst returns neutral defaults on invalid JSON from LLM
- PortfolioOptimizer weights are all between 0.02 and 0.25 and sum to 1.0
```

---

## PHASE 7 — SMART ORDER ROUTER & EXECUTION ENGINE

```
Build the execution pipeline: Smart Order Router and Execution Engine.

FILE: engine/execution/order_router.py
Class SmartOrderRouter:

  __init__(schwab: SchwabBroker, robinhood: RobinhoodBroker, mock: MockBroker, config: Config):
    - Store broker instances

  async route(order: OrderRequest, db_session) -> tuple[BaseBroker, str]:
    - Returns (broker_instance, routing_reason_string)
    
    ROUTING RULES (evaluate in order):
    
    Rule 0 — Shadow Mode:
      If control_flags["shadow_mode"] == "true" → return MockBroker, "shadow_mode_active"

    Rule 1 — Asset Class: Crypto
      If order.asset_class == "CRYPTO" → return RobinhoodBroker, "crypto_robinhood_only"

    Rule 2 — Asset Class: Options
      If order.asset_class == "OPTION" → return SchwabBroker, "options_schwab_preferred"

    Rule 3 — After-Hours Time Window
      Get current time in America/New_York
      If time < 09:29 OR time > 16:01 → return RobinhoodBroker, "extended_hours_robinhood"

    Rule 4 — Fractional Share
      If order.qty < 1.0 → return RobinhoodBroker, "fractional_share"

    Rule 5 — Standard Equity (default)
      → return SchwabBroker, "standard_equity_schwab"

    After routing: check if chosen broker has circuit_open == True.
    If circuit open: try fallback (Schwab → Robinhood, Robinhood → Schwab).
    If both circuits open: log CRITICAL and return None, "ALL_BROKERS_UNAVAILABLE"

FILE: engine/execution/execution_engine.py
Class ExecutionEngine:

  __init__(router, risk_manager, tax_engine, config):
    - Store dependencies

  async execute_signal(signal: SignalEvent, portfolio_state: dict, db_session) -> dict:
    
    STEP 1: Build OrderRequest from SignalEvent
      - Map signal.direction → order direction
      - Set order_type = MARKET (default); LIMIT if signal.metadata contains "limit_price"
      - Calculate final_qty using calculate_position_size() from the originating strategy

    STEP 2: Run Risk Manager
      result = await risk_manager.check_order(order, portfolio_state, db_session)
      If not result.approved:
        - Update signal in alpha_signals_log: acted_on=False, blocked_by=result.blocked_by
        - Return {"executed": False, "reason": result.blocked_by}
      If result.modified_qty: update order.qty = result.modified_qty

    STEP 3: Route Order
      broker, reason = await router.route(order, db_session)
      If broker is None: return {"executed": False, "reason": "all_brokers_unavailable"}

    STEP 4: Submit Order
      order_result = await broker.submit_order(order)

    STEP 5: Persist Result
      If order_result.success:
        - Insert row into trades table (status=FILLED)
        - Upsert positions table: update average_cost, current_qty, unrealized_pl
        - Call tax_engine.record_lot() for BUY orders
        - Call tax_engine.close_lot() for SELL orders
        - Update signal: acted_on=True
        - Update portfolio_snapshots
        - Log to alpha_signals_log with outcome metadata
      Else:
        - Insert row into trades table (status=REJECTED)
        - Log error with broker error message

    STEP 6: Update Bandit
      - Fetch strategy win rate from strategy_performance
      - Schedule bandit update when position eventually closes (store signal_id in position record)

    STEP 7: Return execution summary dict:
      {"executed": bool, "fill_price": float, "fill_qty": float, 
       "broker": str, "routing_reason": str, "trade_id": int}

  async update_positions_prices(portfolio_state: dict, db_session):
    - Fetch current quotes for all open positions
    - Update positions.last_price, unrealized_pl, unrealized_pl_pct
    - Trigger stop-loss check: if last_price <= position.stop_price → generate SELL signal
    - Trigger take-profit check: if last_price >= position.take_profit_price → generate SELL signal
    - Save updated portfolio_snapshots row

  async calculate_portfolio_state(db_session) -> dict:
    - Aggregate all open positions from positions table
    - Fetch live quotes for each
    - Return comprehensive portfolio_state dict:
      {
        total_equity: float,
        cash_balance: float,
        positions_value: float,
        positions: list[dict],   # full position details
        daily_pnl: float,
        total_pnl: float,
        num_positions: int,
        drawdown_pct: float,
        open_day_trades: int,    # for PDT check
        broker_balances: dict    # per-broker cash
      }

ACCEPTANCE CRITERIA:
- Shadow mode routes ALL orders to MockBroker regardless of other rules
- After-hours order (e.g. 8 PM ET) routes to RobinhoodBroker
- execute_signal with a blocked risk check returns executed=False and logs to compliance_audit_log
- Position table correctly updates average_cost on second BUY of same symbol
- Stop-loss trigger generates SELL signal and logs to alpha_signals_log
```

---

## PHASE 8 — SCHEDULER & DAILY CYCLE

```
Build the complete automated daily cycle using APScheduler.

FILE: engine/scheduler/jobs.py
Use APScheduler AsyncIOScheduler with timezone="America/New_York".

Create a class TradingScheduler that holds all job definitions.

IMPLEMENT THESE EXACT JOBS:

JOB 1 — pre_market_routine
  Schedule: CronTrigger(hour=4, minute=0, day_of_week="mon-fri")
  Logic:
    1. Set engine_status = "PRE_MARKET" in control_flags
    2. Verify broker connections (call get_account_balance on each; log result)
    3. Refresh Schwab OAuth token proactively
    4. Fetch macro data (FRED) and save to market_regime_log
    5. Run MarketRegimeDetector.get_current_regime() and save result
    6. Fetch economic calendar for today
    7. Run LLMAnalyst on any overnight news headlines for watchlist symbols
    8. Place FlashCrashStrategy limit orders for all target symbols
    9. Log: "[PRE_MARKET] Pre-market routine complete. Regime: {state}"

JOB 2 — market_open_prep
  Schedule: CronTrigger(hour=9, minute=28, day_of_week="mon-fri")
  Logic:
    1. Set engine_status = "MARKET_HOURS"
    2. Fetch all active positions; set OCO brackets (stop + take-profit) on Schwab
    3. Calculate opening portfolio state; save to portfolio_snapshots
    4. Run Optuna check: if last_optimization > 7 days ago → schedule overnight tuning task
    5. Log: "[MARKET_OPEN] Market open. Equity: ${equity:,.0f}. Positions: {n}"

JOB 3 — main_trading_cycle  [CORE LOOP]
  Schedule: IntervalTrigger(minutes=5, start_date="today 09:30", end_date="today 16:01")
             only on weekdays (add day_of_week filter)
  Logic (run in this exact order):
    1. Check trading_enabled flag; if false: log and skip
    2. Calculate current portfolio_state
    3. Get current regime and allocation weights from Meta-Brain
    4. For each strategy in STRATEGY_REGISTRY (that is enabled):
        a. Fetch required market data (async, concurrent)
        b. Calculate indicators
        c. Call strategy.generate_signals()
        d. For each signal with strength > 0.3:
           - Calculate position size
           - Execute through ExecutionEngine
    5. Call update_positions_prices()
    6. Save portfolio snapshot
    7. Log cycle summary: elapsed_ms, signals_generated, orders_executed, errors

JOB 4 — options_management
  Schedule: CronTrigger(hour=15, minute=0, day_of_week="mon-fri")
  Logic:
    - Fetch all open option positions from positions table
    - For 0DTE positions (option_expiry == today): close at MARKET immediately
    - For positions at 50% profit: close at MARKET (take profit early)
    - For positions at 200% loss: close at MARKET (stop loss)
    - Log actions taken

JOB 5 — after_hours_routine
  Schedule: CronTrigger(hour=16, minute=15, day_of_week="mon-fri")
  Logic:
    1. Set engine_status = "AFTER_HOURS"
    2. Update all ATR trailing stops (fetch ATR, calc new stop = close - 2*ATR)
    3. Run MoneyMarketSweepStrategy
    4. Run TaxEngine.scan_for_harvest_opportunities()
    5. For each harvest opportunity (if tlh_enabled == "true"):
        Execute harvest (sell loser, buy proxy)
    6. Calculate and save end-of-day portfolio snapshot
    7. Run PortfolioOptimizer.calculate_portfolio_var() and save to snapshot
    8. Log daily PnL summary

JOB 6 — nightly_maintenance
  Schedule: CronTrigger(hour=23, minute=55, day_of_week="mon-fri")
  Logic:
    1. Execute profit sweep: if total_equity > PROFIT_SWEEP_THRESHOLD:
         Calculate settled_cash_excess = total_equity - PROFIT_SWEEP_THRESHOLD
         Log: "PROFIT SWEEP: would transfer ${amount}" (actual ACH is manual — log only)
    2. Generate daily performance report (JSON) and save to logs/daily_report_{date}.json
    3. Retrain HMM if last_train_date > 7 days ago
    4. Backup SQLite: copy trading.db to data_cache/backups/trading_{date}.db
    5. Set engine_status = "OVERNIGHT"

JOB 7 — weekend_review
  Schedule: CronTrigger(day_of_week="sat", hour=9, minute=0)
  Logic:
    1. Run full portfolio rebalance analysis using PortfolioOptimizer
    2. Generate weekly performance summary JSON
    3. Check all wash sale expiry dates; remove expired ones from blacklist
    4. Retrain HMM (always on weekend)
    5. Update strategy_performance stats (recalculate win_rate, sharpe, max_dd) from trades table
    6. Run Optuna hyperparameter tuning if not run in last 7 days

JOB 8 — health_monitor
  Schedule: IntervalTrigger(minutes=1)  [runs 24/7]
  Logic:
    - Check all broker circuit_breaker states
    - Check last main_trading_cycle ran within expected time (during market hours)
    - Check DB write is working (update engine_status timestamp)
    - Log any anomalies at WARNING level

SCHEDULER STARTUP in engine/main.py:
  1. Call auto_migrate() to ensure DB schema is current
  2. Check IS_LIVE flag; log prominent warning if True
  3. Initialise all brokers via broker_factory
  4. Initialise MarketRegimeDetector and call load_or_train()
  5. Initialise all strategy instances and register in STRATEGY_REGISTRY
  6. Initialise ExecutionEngine, RiskManager, TaxEngine, LLMAnalyst
  7. Start APScheduler
  8. Start Engine FastAPI server on ENGINE_PORT
  9. Set engine_status = "RUNNING" in control_flags
  10. Run forever: asyncio.get_event_loop().run_forever()

ACCEPTANCE CRITERIA:
- Scheduler starts without error; all 8 jobs registered
- main_trading_cycle runs and logs "cycle summary" within first 5 minutes after market open
- health_monitor runs every minute and updates engine_status timestamp
- after_hours_routine runs tax harvest scan and logs results (even if no harvests needed)
- Engine API on localhost:8765 responds to GET /health with {"status": "ok"}
```

---

## PHASE 9 — ENGINE REST API

```
Build the Engine's FastAPI REST + WebSocket API on localhost:8765.

FILE: engine/api/engine_api.py
Use FastAPI with uvicorn. Run as a background asyncio task (not blocking the scheduler).

ENDPOINTS:

GET /health
  Returns: {"status": "ok", "engine_status": str, "timestamp": str, "is_live": bool, "shadow_mode": bool}

GET /portfolio
  Returns full portfolio_state dict from ExecutionEngine.calculate_portfolio_state()
  Include: total_equity, cash, positions_value, daily_pnl, total_pnl, num_positions, drawdown_pct, var_99

GET /positions
  Returns: list of all open positions from positions table with current prices, unrealized P&L

GET /trades?limit=100&offset=0
  Returns: paginated trade history from trades table, newest first

GET /signals?limit=50
  Returns: recent alpha signals from alpha_signals_log (last 50)

GET /strategies
  Returns: list from strategy_performance table with all metrics and is_enabled status

GET /regime
  Returns: latest row from market_regime_log with current regime + probabilities

GET /risk/summary
  Returns: {current_leverage, daily_drawdown_pct, var_99, open_day_trades, 
            sector_exposures: dict, wash_sale_count: int}

GET /tax/summary
  Returns: TaxEngine.get_ytd_tax_summary()

GET /tax/form8949?year=2024
  Returns: CSV file (FileResponse) of Form 8949 data

GET /logs?lines=100
  Returns: last N lines from logs/engine.log as JSON array of strings

POST /control/flag
  Body: {"key": str, "value": str}
  Updates control_flags table (used by UI)
  Validates key is one of the allowed flag names (whitelist validation)
  Returns: {"success": bool, "key": str, "new_value": str}

POST /control/strategy/{strategy_id}/toggle
  Toggles is_enabled on strategy_performance for given strategy_id
  Returns: {"strategy_id": str, "is_enabled": bool}

POST /control/halt
  Sets trading_enabled = "false" and halt_reason = "manual_halt" in control_flags
  Cancels all open limit orders via broker APIs
  Returns: {"halted": True, "reason": "manual_halt"}

POST /control/resume
  Sets trading_enabled = "true", clears halt_reason
  Returns: {"trading_enabled": True}

POST /control/shadow_mode
  Body: {"enabled": bool}
  Toggles shadow_mode flag
  Returns: {"shadow_mode": bool}

GET /performance/chart?days=30
  Returns: list of portfolio_snapshots rows for last N days
  Format: [{timestamp, total_equity, daily_pnl, drawdown_pct, regime_state}]

WebSocket: ws://localhost:8765/ws
  On connect: send current portfolio state immediately
  Then broadcast every 10 seconds:
    {"type": "portfolio_tick", "timestamp": str, "total_equity": float, 
     "daily_pnl": float, "positions_count": int, "engine_status": str}
  When a trade executes: broadcast immediately:
    {"type": "trade_executed", "symbol": str, "direction": str, "fill_price": float, "strategy_id": str}
  When regime changes: broadcast:
    {"type": "regime_change", "new_state": str, "probabilities": dict}

CORS: allow_origins=["http://localhost:8766"] only
Authentication: simple API key header check: X-API-Key must match a key stored in control_flags
  (Skip auth for development; make it optional via REQUIRE_API_KEY env var)

ACCEPTANCE CRITERIA:
- GET /health returns 200 with correct fields
- GET /portfolio returns valid portfolio_state JSON
- POST /control/flag with key="trading_enabled", value="false" updates DB and GET /health reflects it
- WebSocket connection receives tick within 10 seconds of connecting
- GET /tax/form8949 returns a valid CSV download response
```

---

## PHASE 10 — CONTROL UI (INDEPENDENT PROCESS)

```
Build the standalone Control UI as an independent Python process.
This process has NO imports from the engine/ package.
It communicates ONLY via HTTP to localhost:8765 and direct SQLite reads.

FILE: ui/ui_server.py
FastAPI app on port UI_PORT (default 8766).
Serves static files from ui/static/ directory.
Single route: GET / → serve ui/static/index.html
Mount static files at /static

FILE: ui/static/index.html + ui/static/dashboard.js + ui/static/styles.css

Design a DARK-THEMED, professional trading terminal dashboard.
Aesthetic: financial terminal, dark navy/black background, neon-green/cyan accents, monospace data fonts.
Think Bloomberg Terminal meets modern web UI.

LAYOUT (single HTML page, no external JS frameworks except Chart.js from CDN):

┌─────────────────────────────────────────────────────────────┐
│  HEADER: AQTA Engine Status  |  [●LIVE/●SHADOW] [■HALT] [▶RESUME]  │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Total Equity │  Daily P&L   │  Drawdown    │  Regime        │
│  $xx,xxx.xx  │  +$xxx.xx    │  -x.xx%      │  BULL_TREND ●  │
├──────────────┴──────────────┴──────────────┴────────────────┤
│  EQUITY CURVE (Chart.js line chart — 30 day history)        │
├─────────────────────────┬───────────────────────────────────┤
│  OPEN POSITIONS TABLE   │  STRATEGY CONTROLS                │
│  Symbol│P&L│Stop│Size   │  [●] EQ_TREND_FOLLOW  wt: 0.45  │
│  AAPL  │...│...│...    │  [●] EQ_MEAN_REV      wt: 0.25  │
│  ...   │...│...│...    │  [○] EQ_STAT_ARB      wt: 0.00  │
├─────────────────────────┤  [●] EQ_EARNINGS      wt: 0.15  │
│  RECENT SIGNALS LOG     │  [●] CASH_SWEEP        wt: 0.15  │
│  (auto-scrolling feed)  ├───────────────────────────────────┤
│                         │  SYSTEM CONTROLS                  │
│                         │  Shadow Mode: [ON/OFF toggle]     │
│                         │  LLM Analysis: [ON/OFF toggle]    │
│                         │  TLH Enabled: [ON/OFF toggle]     │
│                         │  Crypto: [ON/OFF toggle]          │
│                         │  Options: [ON/OFF toggle]         │
├─────────────────────────┴───────────────────────────────────┤
│  TRADE LOG (last 20 trades — auto-refresh every 30s)        │
│  Time | Symbol | Direction | Qty | Price | Strategy | P&L   │
├─────────────────────────────────────────────────────────────┤
│  TAX SUMMARY  STCG: $x,xxx  LTCG: $x,xxx  Saved: $x,xxx   │
└─────────────────────────────────────────────────────────────┘

IMPLEMENT IN dashboard.js:

const ENGINE_API = "http://localhost:8765";
const WS_URL = "ws://localhost:8765/ws";
let ws = null;
let equityCurveChart = null;

function connectWebSocket():
  - Create WebSocket to WS_URL
  - On message: parse JSON; update live ticker values (equity, daily_pnl, status)
  - On close: reconnect after 5 seconds; show "DISCONNECTED" badge in header
  - On error: show error in header status bar

async function refreshAll():
  - Call all GET endpoints concurrently using Promise.all([...fetch calls])
  - Update: portfolio summary, positions table, strategies table, tax summary, trade log

function renderEquityCurve(data):
  - Chart.js line chart (type: "line")
  - X-axis: timestamps; Y-axis: total_equity
  - Two datasets: "Portfolio Equity" (green line) and "Daily P&L" (secondary axis, bar)
  - Dark theme: backgroundColor black, gridlines dark gray, labels white/cyan
  - Smooth curves: tension: 0.4

function renderPositionsTable(positions):
  - Colour P&L column: green if positive, red if negative
  - Show stop_price with a small warning icon if price within 2% of stop
  - Click row to expand: show strategy_id, entry date, Greeks (if options)

function renderStrategiesPanel(strategies):
  - Each strategy: toggle switch (calls POST /control/strategy/{id}/toggle on click)
  - Show current weight as animated bar (width = weight * 100%)
  - Show win_rate and total_pnl inline
  - Disabled strategies show greyed out

function renderSignalsFeed(signals):
  - Live-scrolling list of last 20 signals
  - Colour by direction: BUY=green, SELL=red
  - Show: symbol, direction, strength (as ★ stars 1-5), acted_on status
  - If blocked: show blocked_by rule in red badge

function renderSystemControls():
  - Each toggle: calls POST /control/flag with correct key/value on change
  - Optimistic UI: update toggle state immediately; revert if API call fails
  - Show current value from control_flags

function renderTradeLog(trades):
  - Table with alternating row shading
  - Colour direction column: BUY=green bg, SELL=red bg
  - Commission and slippage shown in muted text
  - Broker shown as a small badge (SCHWAB / ROBINHOOD / MOCK)

function renderTaxSummary(tax):
  - STCG, LTCG, total realized, YTD harvested losses, estimated tax saving
  - "Download Form 8949" button: opens GET /tax/form8949 in new tab

HALT BUTTON:
  - Prominent red button "■ HALT TRADING" in header
  - On click: confirm dialog "This will halt all trading. Are you sure?"
  - Calls POST /control/halt
  - Header turns red; all toggles disabled while halted

RESUME BUTTON:
  - Only visible when halted
  - Calls POST /control/resume

AUTO-REFRESH:
  - refreshAll() on page load
  - setInterval(refreshAll, 30000)  — full refresh every 30 seconds
  - WebSocket handles live ticks between refreshes

RESPONSIVE: works on any screen ≥ 1280px wide. Minimum: ensure no horizontal scroll.

STYLING (styles.css):
  Background: #0a0e1a (deep navy)
  Card backgrounds: #0d1526
  Border: 1px solid #1e3a5f
  Primary accent: #00d4ff (cyan)
  Positive P&L: #00ff88 (green)
  Negative P&L: #ff4455 (red)
  Text primary: #e0e8ff
  Text muted: #5a7a9a
  Font stack: 'JetBrains Mono', 'Courier New', monospace (load JetBrains Mono from Google Fonts)
  All numbers: monospace font, right-aligned
  Toggle switches: CSS-only, custom styled
  Card hover: subtle blue glow border

ACCEPTANCE CRITERIA:
- ui_server.py starts on port 8766; browser opens dashboard
- Dashboard connects to WebSocket and shows live equity updates
- Strategy toggle calls correct API endpoint and updates UI immediately
- HALT button triggers confirm dialog; calls /control/halt; header turns red
- Equity curve chart renders with dark theme; no console errors
- Works when Engine is not running: shows "ENGINE OFFLINE" badge, retries connection
- Trade log shows last 20 trades with correct colour coding
```

---

## PHASE 11 — TESTING, HARDENING & DEPLOYMENT

```
Write the test suite, apply hardening, and create the Windows deployment setup.

FILE: tests/test_risk_manager.py
Write pytest tests for every RiskManager check:
  - test_trading_disabled_blocks_all_orders()
  - test_wash_sale_blocks_buy()
  - test_pdt_rule_blocks_fourth_daytrade()
  - test_position_concentration_resizes_order()
  - test_intraday_drawdown_halts_new_entries()
  - test_all_checks_pass_for_valid_order()
  Use pytest fixtures for db_session (in-memory SQLite), mock portfolio_state

FILE: tests/test_tax_engine.py
  - test_fifo_closes_oldest_lot_first()
  - test_hifo_closes_highest_cost_lot_first()
  - test_wash_sale_recorded_on_loss()
  - test_harvest_opportunity_requires_proxy()
  - test_form_8949_csv_has_correct_columns()

FILE: tests/test_strategies.py
  - test_trend_following_buy_signal_on_valid_crossover()
  - test_trend_following_no_signal_when_adx_below_25()
  - test_mean_reversion_buy_on_bollinger_lower_touch()
  - test_flash_crash_only_runs_at_market_open()
  - test_money_market_sweep_calculates_correct_qty()
  Use pytest fixture: generate_mock_ohlcv(n_rows, scenario)
    Scenarios: "bull_trend", "bear_trend", "sideways", "bollinger_squeeze"

FILE: tests/test_mock_broker.py
  - test_mock_buy_reduces_cash()
  - test_mock_limit_order_not_filled_when_price_above_limit()
  - test_circuit_breaker_opens_after_3_errors()

FILE: tests/test_engine_api.py
  Use httpx.AsyncClient with pytest-asyncio
  - test_health_endpoint_returns_200()
  - test_post_control_flag_updates_db()
  - test_strategy_toggle_changes_is_enabled()
  - test_halt_sets_trading_enabled_false()

HARDENING TASKS:

1. Structured logging setup (engine/utils/logger.py):
   - Use structlog with JSON renderer
   - Log to both console (colored, human-readable) and logs/engine.log (JSON)
   - Rotating file handler: max 10MB per file, keep 7 files
   - All log entries include: timestamp, level, module, function, message, extra_fields

2. Error handling audit:
   - Every async function must have try/except with specific exception types
   - Never catch bare Exception without re-raising or logging with traceback
   - All broker calls: catch aiohttp.ClientError, asyncio.TimeoutError, and broker-specific exceptions
   - Database errors: catch SQLAlchemy exceptions; rollback and re-raise

3. mypy type checking:
   - Add mypy.ini: strict = false, ignore_missing_imports = true
   - Fix all mypy errors in brokers/, risk/, strategies/, meta_brain/
   - All function signatures must have type annotations

4. ruff linting:
   - Add ruff.toml: line-length = 100, select = ["E","W","F","I"]
   - Fix all ruff warnings

5. Security hardening:
   - .env file loaded only at startup; Config object not re-read from env vars at runtime
   - Schwab token file (schwab_token.json): chmod 600 equivalent on Windows (icacls command)
   - SQLite DB file: restrict write access to current user only
   - API key for Engine API: generated on first run, stored in control_flags, required in UI requests

6. Windows deployment files:

   File: install_dependencies.bat
   @echo off
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   echo Install complete.

   File: first_run_setup.py
   - Run auto_migrate()
   - Prompt user to authenticate with Schwab (OAuth flow)
   - Prompt user to enter Robinhood credentials (save to .env)
   - Verify Ollama is running (optional — skip if not available)
   - Run MockBroker test order to confirm everything works
   - Print setup complete summary

   File: check_health.bat (run anytime to check system status)
   @echo off
   python -c "import httpx; r=httpx.get('http://localhost:8765/health'); print(r.json())"

   File: README.md
   Complete setup instructions:
   1. Install Python 3.11+ from python.org
   2. Install NSSM from nssm.cc
   3. Clone/copy project to C:\TradingSystem\
   4. Run install_dependencies.bat
   5. Copy .env.example to .env and fill in credentials
   6. Run python first_run_setup.py
   7. Test: run run_engine.bat (Ctrl+C to stop)
   8. Test: run run_ui.bat (opens http://localhost:8766)
   9. Production: run install_service.bat as Administrator
   10. Verify: check_health.bat

FINAL ACCEPTANCE CRITERIA:
   - pytest runs all tests; minimum 90% pass rate (some broker tests require credentials)
   - mypy reports 0 errors on engine/ and ui/ packages
   - ruff reports 0 warnings
   - python first_run_setup.py completes without errors in mock/shadow mode
   - run_engine.bat starts engine; health check returns {"status":"ok"}
   - run_ui.bat opens dashboard; equity curve renders; strategy toggles work
   - HALT button stops all trades; RESUME re-enables them
   - 30-minute smoke test: engine runs for 30 minutes, logs no CRITICAL errors,
     portfolio snapshot saved every 5 minutes, mock broker executes at least one signal
```

---

## PHASE 12 — OPPORTUNITY SCANNER & ALTERNATIVE DATA ENGINE

```
You are building Phase 12 of the AQTA trading system.
Prerequisite: Phases 0-11 are complete and all tests pass.
Platform: Windows, Python 3.11+, no Docker, no Redis, SQLite only.

TASK 1 — engine/scanner/stock_screener.py
Implement StockScreener class with these async methods:

async get_sp500_components() -> list[str]:
  - Scrape Wikipedia SP500 list: "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
  - Parse table with requests + html.parser (stdlib)
  - Extract Symbol column; clean (remove dots, replace with hyphens)
  - Cache to data_cache/sp500_components.json (refresh daily)

async get_premarket_movers(min_gap_pct: float = 2.0) -> list[dict]:
  - Use yfinance: for each symbol in sp500 subset (top 200 by market cap)
  - Get pre-market price vs prior close
  - Filter: abs(gap_pct) >= min_gap_pct
  - Return sorted by abs(gap_pct) descending
  - Include: {symbol, gap_pct, pre_market_price, prior_close, pre_market_volume}

async get_high_volume_stocks(volume_ratio_threshold: float = 2.0) -> list[str]:
  - For each SP500 component: fetch today's volume vs 20-day average
  - Return symbols where today_volume / avg_20d_volume > threshold
  - Run in executor (yfinance is sync) with Semaphore(20) for concurrency

async scan_finviz_screener(filters: dict) -> list[str]:
  - Use finvizfinance library (pip install finvizfinance)
  - Build filter params from dict (e.g. {"RSI": "os30", "Volume": "o1000000"})
  - Return list of matching symbols
  - Finviz free tier: scrape with 1-second delay between requests

async get_earnings_next_n_days(days: int = 5) -> list[dict]:
  - yfinance calendars for SP500 subset
  - Return {symbol, earnings_date, consensus_eps, prior_eps} sorted by date

TASK 2 — engine/scanner/opportunity_scanner.py
Implement OpportunityScanner with SetupOpportunity dataclass and run_full_scan().
  
SetupOpportunity:
  symbol: str
  asset_class: str
  opportunity_type: str  # e.g. "52WK_BREAKOUT", "RSI_OVERSOLD", "EARNINGS_DRIFT"
  composite_score: float
  technical_signals: list[str]  # human-readable list of triggered indicators
  catalyst_flags: dict          # {has_earnings, has_insider_buy, has_news, etc.}
  recommended_strategies: list[str]  # strategy_ids that can trade this setup
  data_snapshot: dict           # {price, volume_ratio, rsi, adx, atr, ...}
  created_at: str

async run_full_scan(portfolio_state: dict) -> list[SetupOpportunity]:
  1. Get scan universe: sp500 + ETF list + crypto list (combined ~600 symbols)
  2. Tier 1 filter: volume > $5M, spread < 0.5%, price $1-$5000
     (async batch: fetch quotes for all 600 in parallel, Semaphore(30))
  3. For survivors (~200): fetch OHLCV + calculate indicators (parallel)
  4. Score each using score_opportunity()
  5. Match strategies using REGIME_COMPATIBILITY_MATRIX
  6. Return top 25 sorted by composite_score desc
  7. Save all results to opportunity_scans table

score_opportunity(symbol, data, regime) -> float:
  Calculate weighted scores:
  - momentum_score = (rsi - 50) / 50 if direction is long else (50 - rsi) / 50
  - volume_score = min(volume_ratio / 3.0, 1.0)
  - trend_score = 1.0 if adx > 25 else adx/25
  - catalyst_score = sum of catalyst flags (0.2 each)
  - regime_fit = average regime compatibility for matched strategies
  composite = 0.25*momentum + 0.20*volume + 0.15*trend + 0.20*catalyst + 0.20*regime
  Return composite (0.0 to 1.0)

TASK 3 — engine/data/alternative_data.py
Implement AlternativeDataEngine:

async get_insider_trades(days_back: int = 7) -> list[dict]:
  - Scrape OpenInsider: http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=7&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=100&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=40&action=1
  - Parse HTML table; extract: symbol, insider_name, title, transaction_type, shares, value, date
  - Filter: transaction_type = "P - Purchase" (open market buy only, not options exercise)
  - Filter: value > 50000 (minimum $50k purchase)
  - Detect clusters: group by symbol; flag if 3+ insiders bought in 14 days

async get_congress_trades(days_back: int = 30) -> list[dict]:
  - Scrape https://www.capitoltrades.com/trades (free, public data)
  - Or use https://efts.sec.gov/LATEST/search-index?q=%22Form+4%22 (SEC EDGAR)
  - Extract: politician_name, symbol, transaction_type, amount_range, trade_date
  - Filter: transaction_type = "Purchase"
  - Return list sorted by trade_date desc

async get_reddit_mentions(symbols: list[str], subreddits: list = ["wallstreetbets","stocks","investing"]) -> dict[str, dict]:
  - Use PRAW (Python Reddit API Wrapper, free) with read-only credentials
  - Search last 6 hours of posts in each subreddit
  - Count mentions of each symbol; calculate mention_velocity (mentions/hour)
  - Calculate sentiment ratio: positive_posts / total_posts (keyword-based)
  - Return dict: {symbol: {mention_count, mention_velocity, sentiment_ratio, top_post_title}}

async get_finbert_sentiment(texts: list[str], symbols: list[str]) -> dict[str, float]:
  - Load FinBERT model locally (HuggingFace: ProsusAI/finbert)
  - Model loads once at startup (cache in memory); inference is fast
  - For each (text, symbol) pair: tokenize and predict {positive, negative, neutral}
  - Return {symbol: sentiment_score} where score = positive - negative (-1 to +1)

async get_google_trends_signals() -> dict[str, float]:
  - Use pytrends (free, no API key)
  - Keyword list: ["buy stocks", "stock market crash", "buy gold", "bitcoin buy",
                   "inflation hedge", "recession stocks", "dividend stocks"]
  - Get 7-day trend data; calculate velocity (this week vs last week)
  - Return {keyword: trend_velocity} — used by macro strategies

async get_13f_new_positions(top_n_funds: int = 20) -> list[dict]:
  - Use sec-edgar-downloader to fetch latest 13F filings
  - Focus on top 20 known hedge funds by AUM (Berkshire, Bridgewater, etc.)
  - Extract new positions (appeared in latest filing, not in prior)
  - Return: {fund_name, symbol, shares, value, date_filed}

async get_short_interest_data(symbols: list[str]) -> dict[str, dict]:
  - Scrape finviz.com/quote.ashx for each symbol
  - Extract: short_float_pct, short_ratio (days to cover), short_interest
  - Use aiohttp + asyncio; 0.5s delay between requests (be respectful)
  - Cache per symbol for 24 hours

ACCEPTANCE CRITERIA:
- get_sp500_components() returns list of 503 symbols (cached)
- run_full_scan() completes in < 120 seconds (async, concurrent fetches)
- get_insider_trades() returns at least 1 result from last 7 days (real data)
- get_finbert_sentiment() runs fully locally with no API key
- opportunity_scans table populated after first scan
```

---

## PHASE 13 — DAILY CYCLE MANAGER & PROFIT EXTRACTION

```
You are building Phase 13 of the AQTA trading system.
Prerequisite: Phases 0-12 complete.

TASK 1 — engine/brain/daily_pnl_manager.py
Implement DailyPnLManager class exactly as designed in PART VII of this document.

Add these additional methods:

async get_daily_status(db_session) -> dict:
  Returns complete current cycle state:
  {
    cycle_date, starting_capital, current_equity, daily_pnl, daily_pnl_pct,
    profit_target, profit_target_progress_pct,
    profit_locked_amount, profit_protected_pct,
    state, recovery_days_remaining, recovery_target, recovery_progress_pct,
    consecutive_profit_days, position_size_multiplier,
    current_max_new_entry_risk, extraction_eligible_amount
  }

async lock_in_profits(current_equity: float, db_session):
  Called every 5 minutes during market hours.
  If daily_pnl > profit_lock_threshold:
    - Set a "profit_floor" = current_equity - (daily_pnl * (1 - protect_pct))
    - Store profit_floor in control_flags
    - If current_equity drops below profit_floor → trigger soft halt (log, reduce sizing)

async run_end_of_day(db_session):
  3:55 PM ET job.
  1. Calculate final equity from all positions + cash
  2. Call end_of_day_settlement()
  3. Write to daily_cycle_log
  4. Update profit_wallet
  5. If profit extracted: log with timestamp and amount
  6. Update recovery_sessions if in recovery mode
  7. Send end-of-day summary to logs

TASK 2 — engine/brain/capital_allocator.py
Implement capital allocation across concurrent opportunities:

async allocate_capital(opportunities: list[RankedSetup], 
                       portfolio_state: dict,
                       daily_status: dict) -> list[AllocatedTrade]:
  
  RULES (apply in order):
  1. Total capital to deploy = current_cash * deployment_ratio
     deployment_ratio = 0.80 normally, 0.50 in RECOVERY_MODE, 0.70 in DRAWDOWN_ALERT
  
  2. Always keep 20% cash as liquidity buffer
  
  3. Per-trade allocation:
     Base size = kelly_fraction * win_rate * avg_win / avg_loss * portfolio_equity
     Apply position_size_multiplier from DailyPnLManager
     Cap at max_single_position_pct (10%) of portfolio
     Floor at $100 (minimum meaningful trade)
  
  4. Total risk budget: sum of (entry_price - stop_price) * qty <= 6% of equity
     If adding next trade would breach risk budget → stop allocating
  
  5. Correlation check: reject if new position correlation > 0.75 with any existing
  
  6. Max concurrent positions: 10 (configurable via control_flags)
  
  Return list of AllocatedTrade with final sizes, sorted by priority_score desc.

TASK 3 — engine/tax/tax_optimizer.py
Implement TaxAwarePortfolioManager:

select_optimal_lots(symbol, qty_to_sell, db_session) -> list[TaxLot]:
  - Evaluate FIFO, HIFO, LTCG_FIRST, LOSS_FIRST
  - Calculate net_after_tax proceeds for each method
  - Log decision to tax_optimization_decisions table
  - Return lots for method with highest net_after_tax proceeds

evaluate_gain_deferral(position, db_session) -> GainDeferralRecommendation:
  GainDeferralRecommendation: {should_defer, days_to_ltcg, potential_tax_saving,
                                hedge_cost_estimate, net_benefit, recommendation_text}
  Logic:
  - If position has gain AND days_held between 335 and 365 → evaluate deferral
  - tax_saving = gross_gain * (stcg_rate - ltcg_rate)  # ~15-17% saving
  - hedge_cost = estimated ATM put premium for remaining days (from options data)
  - if tax_saving > hedge_cost * 1.5 → recommend defer + hedge
  - else → recommend sell now

async evaluate_all_positions(db_session) -> list[GainDeferralRecommendation]:
  - Run evaluate_gain_deferral for every open position
  - Also run should_harvest_now for losing positions
  - Return prioritised action list

ACCEPTANCE CRITERIA:
- DailyPnLManager correctly transitions from NORMAL to RECOVERY when daily_pnl < 0
- position_size_multiplier = 0.5 in RECOVERY_MODE
- Capital allocator respects 20% cash buffer under all conditions
- Tax optimizer selects HIFO lot (saves most tax) over FIFO when applicable
- evaluate_gain_deferral recommends deferral when tax saving > hedge cost
- daily_cycle_log has one row per trading day after end_of_day runs
```

---

## PHASE 14 — ENHANCED STRATEGIES (ALL 50+ IMPLEMENTATIONS)

```
You are building Phase 14. Implement all remaining strategies not in Phases 1-11.
Each strategy follows the BaseStrategy ABC from Phase 5.
All use only free data sources.

For EACH of the following strategy files, implement the full class:

COPY TRADING STRATEGIES:
  engine/strategies/copy_trading/congress_trade.py — D1 strategy from PART IV
  engine/strategies/copy_trading/insider_follow.py — D2 strategy
  engine/strategies/copy_trading/institutional_13f.py — D7 strategy

SENTIMENT STRATEGIES:
  engine/strategies/sentiment/finbert_signal.py — D3 strategy
  engine/strategies/sentiment/wsb_momentum.py — D4 strategy
  engine/strategies/sentiment/google_trends_signal.py — D5 strategy

INTRADAY STRATEGIES:
  engine/strategies/intraday/opening_range_breakout.py — A1 strategy
    - Requires 15-minute OHLCV bars (yfinance intraday free)
    - ORB calculated from 9:30-9:44 candles
    - Signals generated at 9:45 AM and every 15 min until 11:30 AM only
  
  engine/strategies/intraday/vwap_momentum.py — A2 strategy
    - VWAP calculated from open each day (cumulative)
    - Only generates signals between 9:45 AM and 2:30 PM
  
  engine/strategies/intraday/gap_and_go.py — A3 strategy
    - Uses pre-market data from yfinance
    - LLM sentiment gate: requires FinBERT score > 0.5 on news
  
  engine/strategies/intraday/unusual_volume.py — A7 strategy

OPTIONS STRATEGIES (Schwab only):
  engine/strategies/options/zero_dte_condor.py — C1 strategy
  engine/strategies/options/earnings_iv_crush.py — C2 strategy
  engine/strategies/options/cash_secured_put.py — C4 strategy

MACRO STRATEGIES:
  engine/strategies/macro/rate_rotation.py — F1 strategy
  engine/strategies/macro/vix_mean_reversion.py — F2 strategy
  engine/strategies/macro/commodity_equity_signal.py — F6 strategy

QUANT STRATEGIES:
  engine/strategies/quant/volatility_regime.py — E2 strategy
  engine/strategies/quant/factor_momentum.py — E5 strategy
  engine/strategies/quant/lead_lag_sector.py — E6 strategy

For each strategy class, also implement:
  get_required_data_sources() -> list[str]: what data it needs
  get_optimal_regime() -> list[str]: which regimes it prefers
  get_typical_hold_period() -> str: "INTRADAY" / "SWING_1_3D" / "POSITION_5_30D"
  get_risk_profile() -> str: "CONSERVATIVE" / "MODERATE" / "AGGRESSIVE"

Register ALL strategies in engine/config.py STRATEGY_REGISTRY dict.

ACCEPTANCE CRITERIA:
- All 25 new strategy classes instantiate without error
- Each strategy returns valid SignalEvent on appropriate mock data
- CongressTradeStrategy only generates signals when acting_on_public_data=True
  (i.e., filing is already public — 48h+ after filing date)
- ORBStrategy never generates signals outside 9:45-11:30 AM window
- All strategies have type annotations and pass mypy check
```

---

## PHASE 15 — FULL INTEGRATION & SYSTEM VALIDATION

```
You are building Phase 15. Final integration, validation, and hardening.

TASK 1 — Integration Test: Full Daily Cycle Simulation
Create tests/test_full_cycle.py:
  
test_full_day_simulation():
  1. Reset database to clean state with $10,000 virtual capital
  2. Set IS_LIVE=false, shadow_mode=true
  3. Run pre_market_routine job manually
  4. Run opportunity_scanner.run_full_scan() — verify returns SetupOpportunity list
  5. Run main_trading_cycle 3 times (simulating 9:35, 9:40, 9:45 AM)
  6. Verify: at least 1 signal generated, risk-checked, routed to MockBroker
  7. Verify: trade logged to trades table, position in positions table
  8. Run after_hours_routine manually
  9. Run end_of_day settlement
  10. Verify: daily_cycle_log has 1 row; profit_wallet updated if profitable

test_recovery_mode_activation():
  1. Manually set daily_pnl to -$200 in DailyPnLManager state
  2. Run end_of_day_settlement()
  3. Verify: state = RECOVERY_MODE, recovery_days_remaining = 5
  4. Verify: position_size_multiplier = 0.5
  5. Run next day cycle; verify smaller position sizes

test_tax_optimizer_lot_selection():
  Create 3 lots: AAPL lot1 (180 days, cost $150, qty 10),
                  AAPL lot2 (400 days, cost $140, qty 10),
                  AAPL lot3 (30 days, cost $160, qty 10)
  Current price: $180. Sell 15 shares.
  - FIFO would sell lot1 + 5 of lot3 → mostly STCG
  - HIFO would sell lot3 (all) + 5 of lot1 → some STCG, rest depends
  - LTCG_FIRST would sell lot2 (LTCG) + 5 of lot1 → best rate for lot2
  - LOSS_FIRST: no losses here → defaults to LTCG_FIRST
  Verify select_optimal_lots() picks LTCG_FIRST (lot2 taxed at 15%, others at 35%)
  Verify tax_optimization_decisions table has the decision logged

test_zero_dte_condor_signal():
  Mock VIX = 17, IV Rank = 65%, time = 9:35 AM, mode = shadow
  ORB strategy should generate SELL (condor setup) on SPY
  Verify: signal has both call and put strike metadata, premium > 0

TASK 2 — Performance Benchmarking
Create tools/backtest_runner.py:
  Backtesting framework using historical yfinance data:
  - Load 1-year historical data for SP500 top 100 by volume
  - Run OpportunityScanner and all strategies against historical data
  - Simulate fills with realistic slippage (0.05% market orders)
  - Track: daily_pnl, max_drawdown, sharpe_ratio, win_rate per strategy
  - Output backtest_results_{start}_{end}.json + CSV
  - Compare: with vs without tax optimization (net vs gross returns)

Run backtest: last 252 trading days
  Report expected outputs:
  - Annualized return (target: > 50% on $10k starting capital)
  - Max drawdown (target: < 15%)
  - Win rate (target: > 58%)
  - Sharpe Ratio (target: > 1.5)
  - Average daily PnL (target: $150-$300 on $10k)
  - Tax efficiency: net return / gross return (target: > 85%)

TASK 3 — Final README and Quick Start Guide
Update README.md with:
  System overview diagram (ASCII)
  Prerequisites: Python 3.11, NSSM, Ollama (optional), Robinhood + Schwab accounts
  5-step quick start
  First-run safety checklist (confirm shadow_mode=true before any live trading)
  Strategy descriptions table (all 50+ strategies, one line each)
  Control UI guide (screenshots descriptions)
  Tax guide (how lot selection works, what Form 8949 export contains)
  Troubleshooting: common errors and fixes
  Performance expectations: realistic daily returns, risk disclosure

TASK 4 — Risk Disclosure Comments
Add to engine/main.py startup:
  Print prominent WARNING block:
  "╔══════════════════════════════════════════════════════════════╗
   ║  AQTA TRADING SYSTEM — RISK DISCLOSURE                      ║
   ║  This system trades real money. All trading involves risk.  ║
   ║  Past performance does not guarantee future results.        ║
   ║  You may lose money. Consult a financial advisor.           ║
   ║  Currently running in: SHADOW MODE (paper trading)          ║
   ║  To enable live trading, set IS_LIVE=true in .env           ║
   ╚══════════════════════════════════════════════════════════════╝"

FINAL ACCEPTANCE CRITERIA:
  ✓ Full day simulation test passes end-to-end
  ✓ Recovery mode activates on loss day; correct sizing in recovery
  ✓ Tax optimizer saves > 20% estimated tax vs naive FIFO (backtest)
  ✓ Backtest runs on 1 year of data in < 10 minutes
  ✓ All 50+ strategies registered and have backtest results
  ✓ README covers all setup steps; non-developer can follow it
  ✓ System runs 24+ hours in shadow mode with no unhandled exceptions
  ✓ UI shows all 6 new panels; all controls functional
  ✓ Form 8949 CSV export is valid and includes wash-sale adjustments
```

---

## APPENDIX — COPILOT AGENT BEHAVIOUR RULES

> **Include this block at the top of EVERY Phase prompt you send to Copilot:**

```
AGENT RULES — enforce throughout this session:

1. SEQUENTIAL EXECUTION: Complete every task in the numbered list before proceeding.
   Do not skip tasks. Do not combine tasks unless explicitly instructed.

2. TYPING: Every function must have full type annotations. Use Python 3.11+ syntax
   (e.g. `str | None` not `Optional[str]`).

3. ASYNC FIRST: All I/O operations (database, HTTP, file) must be async.
   Use `asyncio.get_event_loop().run_in_executor()` for blocking libraries (yfinance, robin_stocks).

4. ERROR HANDLING: Every async function must have try/except blocks.
   Log errors with structlog at the appropriate level (WARNING for recoverable, ERROR for data loss risk, CRITICAL for trading halts).

5. NO DOCKER / NO REDIS: Do not suggest, import, or reference Docker, Redis, Celery,
   RabbitMQ, or any containerization technology. All infrastructure is SQLite + APScheduler.

6. NO EXTERNAL PAID SERVICES: Use only open-source libraries and free-tier API endpoints
   (yfinance, FRED public API, SEC EDGAR public API). Do not suggest Polygon.io, Alpaca paid tiers,
   Bloomberg, or any paid data vendor.

7. WINDOWS COMPATIBILITY: All file paths must use os.path.join() or pathlib.Path().
   Do not use forward-slash hardcoded paths. Use Windows-compatible subprocess calls.

8. SHADOW MODE SAFETY: IS_LIVE defaults to false. If IS_LIVE=true,
   print a PROMINENT WARNING in the logs at startup. Never change IS_LIVE from within code.

9. DATABASE CONSISTENCY: Every write operation must use a try/except with db_session.rollback()
   in the except block. Never leave uncommitted transactions.

10. ACCEPTANCE CRITERIA ARE MANDATORY: After completing all tasks in a Phase,
    provide the exact commands to verify each Acceptance Criterion and their expected output.
    Do not declare a Phase complete until all criteria can be verified.
```

## QUICK REFERENCE — KEY FILES SUMMARY

| Phase | Key File | Purpose |
|---|---|---|
| 0 | `engine/config.py` | All configuration, loaded once at startup |
| 1 | `engine/database/models.py` | All 11 SQLAlchemy table definitions |
| 1 | `shared/trading.db` | The ONLY file shared between Engine and UI |
| 2 | `engine/brokers/schwab_broker.py` | Schwab OAuth2 + order execution |
| 2 | `engine/brokers/robinhood_broker.py` | RH auth + extended hours + crypto |
| 2 | `engine/brokers/mock_broker.py` | Shadow mode paper trading |
| 3 | `engine/data/market_data.py` | All async data fetching + indicators |
| 4 | `engine/risk/risk_manager.py` | 12-step pre-trade check pipeline |
| 4 | `engine/risk/tax_engine.py` | Lot tracking, TLH, Form 8949 |
| 5 | `engine/strategies/*.py` | All strategy implementations |
| 6 | `engine/meta_brain/regime_detector.py` | HMM 6-state market regime |
| 6 | `engine/meta_brain/allocator.py` | Thompson Sampling bandit allocator |
| 6 | `engine/meta_brain/llm_analyst.py` | Ollama local LLM integration |
| 7 | `engine/execution/execution_engine.py` | Signal → risk check → broker → DB |
| 8 | `engine/scheduler/jobs.py` | All APScheduler job definitions |
| 9 | `engine/api/engine_api.py` | REST + WebSocket API on :8765 |
| 10 | `ui/ui_server.py` | Independent UI server on :8766 |
| 10 | `ui/static/index.html` | Terminal-style trading dashboard |
| 11 | `tests/` | Full test suite |