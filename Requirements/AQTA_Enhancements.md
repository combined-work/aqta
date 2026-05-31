---

# AUTONOMOUS QUANTITATIVE TRADING ARCHITECTURE (AQTA)
## Comprehensive System Specification & Master Blueprint (Enhanced Local Edition)

---

## 1. SYSTEM OVERVIEW & OPERATING DOCTRINE

The Autonomous Quantitative Trading Architecture (AQTA) is an enterprise-grade, multi-asset quantitative trading platform engineered specifically for **high-performance local deployment**. It operates 24/7/365 unattended, maximizing risk-adjusted returns through statistical arbitrage, alternative data, and strict tax-aware risk management.

### 1.1 Capital Framework & Daily Cycle Rules
*   **Capital Base:** Configurable starting capital (e.g., BASE_CAPITAL = 10000). All risk, sizing, and targets are strictly percentage-based relative to `x`.
*   **Daily Profit Targets:** Minimum: $300 (3.0%) | Maximum: Uncapped (System utilizes trailing stops to let runners run indefinitely).
*   **Profit Extraction Rule:** If EOD equity > x + 3.0%, the excess is extracted to a virtual `profit_wallet`.
*   **Profit Lock Mechanism:** At $2,000 intraday profit, 60% is protected (`profit_protect_pct = 0.60`).
*   **Loss Limits:**
    *   *Soft Halt:* -1.5% of `x` intraday triggers a 50% reduction in position sizing.
    *   *Hard Halt:* -3.0% of `x` intraday triggers a full system halt and liquidation of day trades.

### 1.2 Zero-Loss Protocol & Recovery Mode
If a day ends with negative PnL, the system enters **Recovery Mode**:
*   **Duration:** Up to `x` trading days (Configurable, e.g., `RECOVERY_MAX_DAYS = 5`).
*   **Target:** Recover exact loss + 10% buffer.
*   **Risk Adjustment:** Position sizes halved (`multiplier = 0.5`). Shifts to mean-reversion and hedged strategies.

### 1.3 LLM-Optional Graceful Degradation
The system is designed to operate at 100% efficiency without Large Language Models. The system features a 3-tier NLP engine to ensure 100% uptime regardless of hardware constraints:
1.  **Tier 1: LLM (Optional):** Uses local Ollama (Llama 3) for deep contextual reasoning on 10-Ks and earnings calls.
   **LLM Enabled (`llm_mode = "LOCAL" | "CLOUD"`):** Uses Ollama (Llama 3) or Anthropic for deep contextual sentiment, 10-K risk extraction, and complex earnings call parsing.
   **LLM Disabled (`llm_mode = "DISABLED"`):** System automatically falls back to TIER 2 and TIER 3 deterministic NLP (NLTK/VADER for sentiment), regex-based SEC filing parsing, and numerical EPS surprise data from standard APIs.
2.  **Tier 2: SLM (Small Language Models - Default):** Uses highly accurate, quantized local models (e.g., `ProsusAI/finbert` or `DistilRoBERTa-financial`) running via ONNX runtime. These provide deterministic, ultra-fast (<50ms) sentiment scoring without the heavy GPU overhead of an LLM.
3.  **Tier 3: Deterministic Fallback:** If models fail to load, falls back to `NLTK/VADER` and regex-based keyword extraction.
---

## 2. ARCHITECTURE & TECHNOLOGY STACK (LOCAL-FIRST)

The system is a hyper-optimized, zero-install Windows/Linux native deployment. It uses a monolithic async architecture to eliminate network latency between microservices.

### 2.1 Hybrid State Management (Redis + Asyncio)
To achieve microsecond latency for intraday calculations while maintaining local simplicity, AQTA uses a hybrid state manager (`StateCacheManager`):
*   **Primary In-Memory Store:** **Redis 7**. Used for all fast calculations, tick data aggregation, order book snapshots, and pub/sub event routing.
*   **Graceful Fallback:** If the Redis service is missing or crashes, the system automatically falls back to native Python `asyncio` in-memory dictionaries and `asyncio.Queue`.
*   **EOD Persistence:** At 23:55 ET, a background task dumps all critical Redis state (rolling correlations, strategy performance metrics, ML feature arrays) into the persistent **SQLite 3** database for historical backtesting and next-day initialization.

### 2.2 Core Infrastructure
*   **Runtime:** Python 3.11+ (Strict `asyncio` concurrency).
*   **Database:** SQLite 3 (Configured for high concurrency: `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA cache_size=-64000;`) + SQLAlchemy 2.0.
*   **In-Memory State:** Redis and Python `asyncio` native state managers.
*   **Task Scheduling:** APScheduler 3.10.4 (AsyncIOScheduler) running in the main event loop.
*   **API & UI:** FastAPI + Uvicorn. Vanilla HTML/CSS/JS (No Node/npm required).
*   **Process Management:** NSSM (Windows) or Systemd (Linux) to run as a background daemon.

### 2.3 Core Python Libraries
*   **Data & Math:** `pandas`, `numpy`, `scipy`, `pandas-ta`, `numba` (for JIT compiling heavy math).
*   **ML & Quant:** `scikit-learn`, `hmmlearn`, `statsmodels`, `pyportfolioopt`, `filterpy` (Kalman filters).
*   **NLP (Non-LLM):** `nltk`, `vaderSentiment` (for fallback sentiment analysis).
*   **Brokers:** `schwab-py`, `robin_stocks`, `ib_insync`, `ccxt`.

---

## 3. DATABASE SCHEMA & STATE MANAGEMENT
*(Inherits all tables from the original spec, with the following enhancements)*

### 3.1 Enhanced Intelligence Tables
*   **`llm_fallback_log`**: Tracks when the system bypassed LLM analysis. `id`, `timestamp`, `symbol`, `data_source`, `vader_score`, `regex_extracted_value`, `action_taken`.
*   **`strategy_correlation_matrix`**: `id`, `date`, `matrix_json` (Stores 30-day rolling Pearson correlation of daily returns between all active strategies to prevent overlapping risk).
*   **`dark_pool_prints`**: `id`, `timestamp`, `symbol`, `price`, `volume`, `notional_value`, `is_sweep`.

---

## 4. STRATEGY ARSENAL (EXPANDED TO 70+ STRATEGIES)

All strategies inherit from `BaseStrategy(A, B, C, D, E, F, G)`. Sizing uses the Kelly Criterion capped at 10% of equity.

### 4.0 Dynamic Strategy Loader
On system initialization, the `StrategyLoader` attempts to instantiate all 80+ strategies.
*   **Dependency Check:** Each strategy runs a `health_check()` method (e.g., pinging a specific API, checking for required historical data, verifying broker permissions).
*   **Failure Handling:** If a strategy fails to load, it does *not* crash the system. It is marked as `STATUS = "DISABLED_ERROR"` in the database.
*   **UI Integration:** In the UI, disabled strategies are greyed out. Hovering over the strategy displays a tooltip with:
    *   *Reason:* e.g., "Glassnode API timeout" or "Missing 2 years of SPY tick data."
    *   *Resolution Steps:* e.g., "Check API key in config.py" or "Run `python scripts/fetch_history.py --symbol SPY`".

### 4.1 Equity Momentum & Intraday (A1-A11)
*   **A1 / Opening Range Breakout (ORB):** Breaks 9:30-9:45 high/low with >2x volume.
*   **A2 / VWAP Momentum:** First pullback to VWAP if price > VWAP and slope > 0.
*   **A3 / Gap-and-Go:** Pre-market gap > 3%, holds prior close.
*   **A4 / Relative Strength Rotation:** Ranks 11 SPDR ETFs by 5d/20d momentum.
*   **A6 / 52-Week High Breakout:** Enters on first intraday pullback of new high.
*   **A7 / Unusual Volume Spike:** Volume > 3x 20-day average without news.
*   *(NEW)* **A8 / VWAP MACD Crossover:** Intraday trend following. BUY when 1-min MACD crosses zero line *while* price is above VWAP.
*   *(NEW)* **A9 / Opening Drive Momentum:** Detects extreme volume in the first 5 minutes (top 1% historical). Buys in direction of the 5-min candle, tight trailing stop.
*   *(NEW)* **A10 / EOD Imbalance Fade:** Scrapes Market-On-Close (MOC) imbalances at 15:50 ET. If imbalance is > $500M BUY, shorts the stock at 15:55 ET anticipating a reversion at the bell.
*   *(NEW)* **A11 / T-WAP Trend Follow:** Calculates a dynamic TWAP from the open. Buys bounces off the TWAP line if the broader market (SPY) tick index is > +500.
*   *(NEW)* **A12 / Pre-Market Catalyst Drift (04:00 - 09:30 ET):** Scans for stocks gapping > 5% in the pre-market with volume > 100k shares. Buys pullbacks to the pre-market VWAP.
*   *(NEW)* **A13 / After-Hours Earnings Momentum (16:00 - 20:00 ET):** Parses EPS/Revenue beats instantly at 16:01 ET using SLM. If beat > 10% and guidance is raised, buys immediately in the after-hours session.

### 4.2 Equity Mean Reversion (B1-B8)
*   **B1 / BB Squeeze Breakout:** BB Width at 6-month low, confirmed by MACD.
*   **B2 / RSI Divergence:** Price makes new low, RSI makes higher low.
*   **B3 / Oversold Large-Cap Bounce:** S&P 500 stocks with RSI < 28, price < BBL.
*   **B4 / Intraday VWAP Deviation:** Fades deviations > 1.5% from VWAP by 11:00 AM.
*   **B5 / Monday Gap Fade:** Fades Monday open gaps > 0.5% without macro catalysts.
*   *(NEW)* **B6 / Connors RSI Pullback:** Uses CRSI (combines RSI, win/loss streak, and ROC). BUY when CRSI < 10 on a stock above its 200-day SMA.
*   *(NEW)* **B7 / Standard Deviation Channel Fade:** Calculates 60-day linear regression channel. Sells short when price hits +2 StdDev upper band; buys at -2 StdDev lower band.
*   *(NEW)* **B8 / Volume Profile POC Reversion:** Calculates intraday Point of Control (price with highest volume). If price drifts > 1% from POC on low volume, fades back to POC.
*   *(NEW)* **B9 / Extended Hours Liquidity Fade:** Detects massive, low-liquidity price spikes in the after-hours session (often caused by fat fingers or retail panic). Fades the spike back to the 16:00 ET closing price.

### 4.3 Copy Trading & Sentiment (D1-D10)
*   **D1 / Congress Trade Replication:** Replicates purchases > $15,000 within 48 hours.
*   **D2 / Insider Cluster Buy:** 3+ officers buy > $50,000 within 14 days.
*   **D3 / NLP Sentiment (LLM/VADER):** Uses LLM if enabled, otherwise VADER on NewsAPI. BUY if score > 0.6.
*   **D4 / WSB Reddit Momentum:** PRAW scan for mention count spikes > 3 SD.
*   **D5 / Google Trends Catalyst:** Maps rising search velocity to ETFs.
*   **D7 / Institutional 13F:** Tracks top 20 hedge funds' new positions.
*   *(NEW)* **D8 / Social Media Cashtag Velocity:** Scrapes StockTwits/X for ticker velocity. Triggers if message volume increases 500% in 1 hour with positive VADER sentiment.
*   *(NEW)* **D9 / C-Suite Conviction Buy:** Specific filter for CEO/CFO open-market buys > $250,000. Double weight allocation compared to standard insider buys.
*   *(NEW)* **D10 / Dark Pool Print Tracking:** Monitors FINRA TRF data. If a single off-exchange print exceeds 5% of daily average volume, follows the direction of the subsequent 5-minute candle.
*   *(NEW)* **D11 / SLM News Flash:** Subscribes to real-time news WebSockets (e.g., Benzinga/Polygon). Feeds headlines into local ONNX FinBERT. If `sentiment > 0.9` and `confidence > 0.95`, executes a market order within 50ms, front-running retail reaction.

### 4.4 Quantitative & Statistical Arbitrage (E1-E9)
*   **E1 / Stat Arb Pairs:** Engle-Granger cointegration (p < 0.05). Trades Z-score < -2.0.
*   **E2 / Volatility Regime Switching:** RV/IV ratio trading.
*   **E3 / Cross-Asset Correlation Break:** Trades divergence > 2 SD (e.g., BTC vs NASDAQ).
*   **E5 / Factor Momentum:** Long top quintile Value/Momentum, short bottom.
*   **E6 / Lead-Lag Sector:** Trades lagging sectors in direction of leading sectors.
*   *(NEW)* **E7 / Index Rebalancing Arb:** Buys stocks announced for S&P 500 inclusion the day of the announcement; sells at the MOC on the effective date.
*   *(NEW)* **E8 / ETF Component Dispersion:** Calculates implied price of SPY based on its top 50 holdings. If SPY deviates > 0.1% from its basket, buys the cheaper asset and shorts the expensive one.
*   *(NEW)* **E9 / Kalman Filter Smoothing:** Uses a Kalman filter to estimate the "true" underlying price of a noisy asset. Buys when actual price drops significantly below the Kalman estimate.
*   *(NEW)* **E10 / Overnight Index Arbitrage:** Compares the closing price of SPY at 20:00 ET with the continuous trading of ES (S&P 500 Futures). If ES drifts > 0.5% overnight without macro news, queues a SPY order for the 04:00 ET pre-market open to capture the convergence.

### 4.5 Macro & Thematic (F1-F9)
*   **F1 / Rate-Sensitive Rotation:** 10Y yield rises -> rotate Tech to Financials.
*   **F2 / VIX Mean Reversion:** VIX > 28 -> buy SPY. VIX < 13 -> buy VXX.
*   **F3 / Fed Calendar:** Buys VXX 3 days before FOMC; sells at open on FOMC day.
*   **F4 / CPI Release:** Trades energy/bonds based on consensus vs actual.
*   **F5 / Gold/Dollar Inverse:** DXY falls > 0.5% -> buy GLD.
*   **F6 / Commodity-to-Equity:** Oil rises > 1.5% -> buy XLE.
*   *(NEW)* **F7 / Yield Curve Inversion Play:** Tracks 2Y/10Y spread. If inversion deepens, shorts Russell 2000 (IWM) and buys Mega-cap Tech (QQQ).
*   *(NEW)* **F8 / Energy Inventory Surprise:** Parses weekly EIA crude report. If draw is 2x larger than consensus, buys USO and XLE immediately.
*   *(NEW)* **F9 / Currency-Hedged Equity:** If DXY (Dollar Index) is in a strong uptrend (ADX > 30), shifts international equity exposure (EFA/EEM) to currency-hedged equivalents (HEFA).
*   *(NEW)* **F10 / Global Session Handoff:** Analyzes the close of the Asian session (Nikkei) and European mid-day (FTSE/DAX). If both are up > 1.5%, applies a bullish multiplier to all US pre-market momentum strategies.

### 4.6 Cash Management & Hedging (CM-01 to CM-04, EQ-04, EQ-05)
*   **CM-01 / Money Market Sweep:** Sweeps idle cash to SWVXX/VMFXX overnight.
*   **EQ-04 / Flash Crash:** Places limit BUY orders -5% to -20% below prior close.
*   **Hedge Ladder:** Maintains 1-2 far OTM SPY puts based on HMM regime.
*   *(NEW)* **CM-03 / T-Bill Laddering:** Automatically buys 4-week Treasury bills with 30% of idle cash, rolling them over at maturity to capture risk-free yield without locking up capital long-term.
*   *(NEW)* **CM-04 / Dividend Capture:** Scans for high-yield stocks 1 day before ex-dividend. Buys stock, sells ATM call to hedge delta, captures dividend, and unwinds position.
*   *(NEW)* **EQ-05 / Tail Risk Convexity:** When VIX < 12 and SPY is at ATH, allocates 0.5% of portfolio to 60-DTE VIX calls (15 strike). Acts as cheap portfolio insurance against black swan events.
*   *(NEW)* **CM-05 / Margin Interest Minimizer:** Actively manages Reg-T margin. If intraday leverage is used, the system automatically liquidates the lowest-conviction positions at 15:55 ET to ensure overnight cash balance is positive, avoiding broker margin interest charges.

---

## 5. THE META-BRAIN (AI & QUANT CORE)

### 5.1 Market Regime Detector (HMM)
*   **Model:** `hmmlearn.hmm.GaussianHMM(n_components=6)`.
*   **Features:** SPY daily return, log volume, VIX, ATR, Yield Spread.
*   **States:** `BULL_TREND`, `BEAR_TREND`, `SIDEWAYS_LOW_VOL`, `SIDEWAYS_HIGH_VOL`, `CRASH_RISK`, `RECOVERY`.

### 5.2 Contextual Capital Allocator
*   Uses **Thompson Sampling** (Multi-Armed Bandit).
*   Maintains a Beta distribution `Beta(alpha, beta)` for each `(strategy_id, regime)` pair.
*   *Enhancement:* Incorporates the **Strategy Correlation Matrix**. If two strategies have a correlation > 0.8, the allocator penalizes the weight of the lower-performing one to ensure true diversification.

### 5.3 Deterministic NLP Fallback Engine (Replaces mandatory LLM)
If `llm_mode == "DISABLED"`:
*   **News Sentiment:** Uses `vaderSentiment`. A compound score > 0.5 is BULLISH, < -0.5 is BEARISH.
*   **Earnings:** Queries Finnhub/AlphaVantage for `actual_eps` vs `estimate_eps`. Calculates percentage surprise.
*   **SEC Filings:** Uses regex to count occurrences of risk keywords ("bankruptcy", "subpoena", "delisting") in 8-K filings.

---

## 6. RISK MANAGEMENT & COMPLIANCE ENGINE

*(Inherits the 12-step pipeline from the original spec, adding the following)*

### 6.1 Advanced Local Risk Checks
13. **Flash Crash Correlation:** If > 30% of open positions drop > 2% within a 5-minute window, triggers a `PORTFOLIO_CIRCUIT_BREAKER`, halting new entries and tightening all trailing stops to 0.5%.
14. **Liquidity Dry-Up Guard:** Before market orders, checks the real-time bid-ask spread. If spread > 3x the 20-day average spread, the order is converted to a Limit order at the mid-price to prevent severe slippage.
15. **Strategy Drawdown Halt:** If a specific strategy (e.g., A1) loses money on 5 consecutive trades, it is locally quarantined (weight set to 0) for 48 hours, regardless of the Meta-Brain's Thompson Sampling allocation.

---

## 7. ENHANCED CONTROL UI & OBSERVABILITY

The Control UI is served via FastAPI on port 8766. It is a zero-dependency, single-page application using vanilla JS, CSS Grid, and Chart.js, communicating via local WebSockets.

### 7.1 Dashboard UI Panels (Dark Theme, JetBrains Mono)
1.  **Header & Master Kill Switch:** Live equity, Daily PnL, Regime State, and a massive red `■ HALT TRADING` button (triggers instant cancellation of all open orders).
2.  **System Topology & Resource Monitor *(NEW)*:** Real-time gauges for Local CPU usage, RAM, SQLite lock contention (ms), and API rate-limit consumption per broker.
3.  **LLM Status & Fallback Indicator *(NEW)*:** Shows current NLP mode (`Ollama Llama3` vs `VADER Fallback`). Displays confidence scores of the latest parsed news.
4.  **Strategy Heatmap *(NEW)*:** A visual correlation matrix grid showing which strategies are currently overlapping in trade direction.
5.  **Daily Cycle Tracker:** Starting Capital, Current Equity, Profit Target progress bar, Profit Locked amount, and cumulative Profit Wallet.
6.  **Equity Curve & Trade Replay *(NEW)*:** Chart.js line chart comparing portfolio vs SPY. Clicking a point on the chart opens a "Trade Replay" modal showing exactly what indicators triggered a trade at that timestamp.
7.  **Opportunity Scanner Feed:** Live-scrolling list of top 5 setups (Rank, Symbol, Type, Score, Strategy).
8.  **Open Positions & Greeks:** Symbol, P&L, Stop Price. Expandable to show real-time Delta, Theta, and Gamma for options.
9.  **Tax & TLH Dashboard:** YTD STCG/LTCG, Harvested Losses, Net Tax Liability, and "Download Form 8949" button.
10. **Parameter Overrides:** Live inputs to adjust Daily Profit Target, Max Daily Loss, and Position Size Multiplier without restarting the Python process.


The Control UI is a Single Page Application (SPA) divided into logical tabs. It uses WebSockets for real-time updates.

### 7.2 Tab 1: Main Terminal (The Cockpit)
*   **Header:** Live Base Capital (`x`), Current Equity, Daily PnL ($ and %), Regime State, and the `■ HALT TRADING` master switch.
*   **Daily Cycle Tracker:** Starting Capital, Profit Target progress bar (3.0%), Profit Locked amount, and cumulative Profit Wallet.
*   **Live Open Positions Table:**
    *   Columns: Symbol, Strategy, Size, Entry Price, Current Price, **Live PnL ($)**, **Live PnL (%)**, Stop Price.
    *   *Feature:* PnL flashes green/red on every tick via Redis pub/sub.
*   **Equity Curve:** Real-time Chart.js line chart comparing portfolio vs SPY/BTC.
*   **Opportunity Scanner Feed:** Live-scrolling list of top setups.

### Tab 2: Strategy Command Center
*   **Categorized Accordions:** Strategies grouped by type (Momentum, Mean Reversion, Stat Arb, etc.).
*   **Strategy Rows:**
    *   **Status Toggle:** Switch to enable/disable the strategy on the fly.
    *   **Health Status:** Green dot (Healthy), Grey dot (Disabled), Red dot (Error).
    *   **Hover Tooltip:** If Red, hovering shows: `Error: Polygon API Timeout. Resolution: Check network connection or API key.`
    *   **Live Parameter Tuning/Threshold Inputs:** Inline input fields to adjust strategy-specific parameters (e.g., `RSI Threshold: [30]`, `Min Volume: [1000000]`) without restarting the engine.

### Tab 3: Risk & Meta-Brain
*   **Meta-Brain Allocator:** Bar chart showing current Thompson Sampling weights for all active strategies.
*   **Strategy Correlation Matrix:** A visual heatmap showing which strategies are currently overlapping in trade direction.
*   **Opportunity Scanner Feed:** Live-scrolling list of top setups (Rank, Symbol, Type, Score, Strategy).
*   **Alternative Data Feed:** Auto-scrolling log of Insider buys, Congress trades, Reddit spikes, and Dark Pool prints.
*   **Margin & Leverage Monitor:** Tracks Reg-T leverage (Max 4x intraday, 2x overnight) and alerts if CM-05 Margin Minimizer is scheduled to trigger.

### Tab 4: System Health
*   **System Topology & Resource Monitor:** Real-time gauges for Local CPU usage, RAM, Redis Memory Usage, SQLite lock contention (ms), and API rate-limit consumption per broker.
*   **NLP Engine Status:** Shows current mode (`Tier 1 LLM`, `Tier 2 SLM`, or `Tier 3 VADER`) and recent parsed headlines with confidence scores.

### Tab 5: Tax, Ledger & Daily Cycle
*   **Daily Cycle Tracker:** Starting Capital, Profit Target progress bar, Profit Locked amount, and cumulative Profit Wallet.
*   **Trade History & Replay:** Searchable ledger of all closed trades. Clicking a trade opens a "Trade Replay" modal showing exactly what indicators triggered the trade at that timestamp.
*   **Tax & TLH Dashboard:** YTD STCG/LTCG, Harvested Losses, Net Tax Liability, and Tax Efficiency vs Naive FIFO.
*   **Form 8949 Generator:** One-click export of IRS-formatted CSV for tax filing.
*   **EOD Redis Sync Log:** Shows the status and latency of the nightly Redis-to-SQLite persistence task.


---

## 8. DAILY CYCLE & TASK SCHEDULING (LOCAL APSCHEDULER)

Because the system is local, it relies on `APScheduler` running inside the FastAPI event loop.
The APScheduler runs continuously from Sunday 00:00 ET to Saturday 00:00 ET, managing the transition between trading sessions and database states.

*   **04:00 ET:** `pre_market_routine` (Token refresh, macro data fetch, local DB vacuum/optimization, Activates A12, F10. Begins 24/5 continuous trading loop).
*   **09:28 ET:** `market_open_prep` (Set OCO brackets, calculate opening state).
*   **09:30 ET:** `regular_market_open` (Standard volume strategies activate).
*   **09:30 - 16:01 ET:** `main_trading_cycle` (Runs every 1 minute. Fetches data, runs Meta-Brain, generates signals, executes via SOR).
*   **15:50 ET:** `moc_imbalance_scan` (Runs Strategy A10).
*   **15:55 ET:** `margin_minimizer` (Runs CM-05 to clear overnight margin).
*   **16:00 ET:** `after_hours_transition` (Activates A13, B9).
*   **16:15 ET:** `after_hours_routine` (Tax-Loss Harvesting scan, Money Market Sweep).
*   **20:00 ET:** `daily_settlement` (Locks profits, updates cycle log, halts trading until 04:00 ET next day).
*   **23:55 ET:** `nightly_maintenance` (Dumps Redis state to SQLite, Generates PDF reports, backs up SQLite DB to local `.bak` file, retrains HMM locally using `numba` optimized routines).