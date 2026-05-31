\# AUTONOMOUS QUANTITATIVE TRADING ARCHITECTURE (AQTA)

\## Comprehensive System Specification \& Master Blueprint (Granular Edition)



\---



\## 1. SYSTEM OVERVIEW \& OPERATING DOCTRINE



The Autonomous Quantitative Trading Architecture (AQTA) is an enterprise-grade, multi-asset, multi-broker quantitative trading platform. It is designed to operate 24/7/365 unattended, maximizing risk-adjusted returns through machine learning, alternative data, and strict tax-aware risk management.



\### 1.1 Capital Framework \& Daily Cycle Rules

The system operates on a strict daily capital reset cycle, treating each trading day as an independent compounding event.

\*   \*\*Capital Base:\*\* $10,000 baseline per cycle.

\*   \*\*Daily Profit Targets:\*\*

&#x20;   \*   \*Minimum:\* $150 (1.5%)

&#x20;   \*   \*Ideal:\* $300 (3.0%)

&#x20;   \*   \*Stretch:\* $500 (5.0%)

\*   \*\*Profit Extraction Rule:\*\* If end-of-day (EOD) equity > $10,000 + Minimum Target, the excess is extracted to a virtual `profit\_wallet`. Real settled cash remains in the brokerage until a weekly ACH transfer threshold (e.g., `PROFIT\_SWEEP\_THRESHOLD = 30000`) is met.

\*   \*\*Profit Lock Mechanism:\*\* If intraday profit reaches $2,000, the system protects 60% of it (`profit\_protect\_pct = 0.60`). A soft halt is triggered if equity drops below this locked floor.

\*   \*\*Loss Limits:\*\*

&#x20;   \*   \*Soft Halt:\* -$150 (-1.5%) intraday triggers a 50% reduction in position sizing.

&#x20;   \*   \*Hard Halt:\* -$300 (-3.0%) intraday triggers a full system halt.



\### 1.2 Zero-Loss Protocol \& Recovery Mode

If a day ends with a negative PnL, capital is not extracted, and the system enters \*\*Recovery Mode\*\*:

\*   \*\*Duration:\*\* Up to 5 trading days (`recovery\_max\_days = 5`).

\*   \*\*Target:\*\* Recover the exact loss amount + 10% buffer (`recovery\_target = abs(daily\_pnl) \* 1.1`).

\*   \*\*Risk Adjustment:\*\* Position sizes are halved (`recovery\_risk\_multiplier = 0.5`).

\*   \*\*Strategy Bias:\*\* Shifts allocation toward conservative, mean-reversion, and hedged strategies.

\*   \*\*Compounding Mode:\*\* Conversely, if the system achieves 5 consecutive profitable days, the position size multiplier increases to 1.2x.



\### 1.3 Target KPIs \& Performance Benchmarks

\*   \*\*Annualized Sharpe Ratio:\*\* > 3.0 (monthly rolling).

\*   \*\*Maximum Drawdown:\*\* < 8% portfolio-wide.

\*   \*\*Win Rate:\*\* > 55% across all strategies (rolling 90-day).

\*   \*\*Average Hold Period:\*\* 2–15 days (equities).

\*   \*\*Options PnL:\*\* > 30% of total PnL derived from theta decay.

\*   \*\*Execution Latency:\*\* < 5ms for Smart Order Routing (SOR).

\*   \*\*System Uptime:\*\* > 99.5%.



\---



\## 2. ARCHITECTURE \& TECHNOLOGY STACK



AQTA supports two deployment tiers: a zero-install Windows-native local deployment, and a containerized enterprise cloud deployment.



\### 2.1 Tier 1: Local Windows Deployment (Zero-Cost Infra)

\*   \*\*Runtime:\*\* Python 3.11+ (asyncio-native).

\*   \*\*Database:\*\* SQLite 3 (WAL mode, foreign keys ON) + SQLAlchemy 2.0.30.

\*   \*\*Task Scheduling:\*\* APScheduler 3.10.4 (AsyncIOScheduler).

\*   \*\*API \& UI:\*\* FastAPI 0.111.0 + Uvicorn 0.30.0. Vanilla HTML/CSS/JS (no Node/npm).

\*   \*\*Process Management:\*\* NSSM (Non-Sucking Service Manager) to run the Trading Engine as a Windows background service.



\### 2.2 Tier 2: Enterprise Cloud Deployment

\*   \*\*Containerization:\*\* Docker, Docker Compose, Kubernetes.

\*   \*\*Database \& State:\*\* PostgreSQL 16 (primary DB), TimescaleDB (tick data), Redis 7 (pub/sub, Celery broker, state flags).

\*   \*\*Task Scheduling:\*\* Celery 5 + Redis Beat Scheduler.

\*   \*\*Storage:\*\* AWS S3 / MinIO (for Parquet feature stores and DB backups).

\*   \*\*Observability:\*\* Prometheus (metrics), Grafana (dashboards), `structlog` (JSON logging to CloudWatch/ELK), PagerDuty (alerts).

\*   \*\*CI/CD:\*\* GitHub Actions (lint -> mypy -> pytest -> build Docker -> push to ECR).



\### 2.3 Core Python Libraries

\*   \*\*Data \& Math:\*\* `pandas 2.2.2`, `numpy 1.26.4`, `scipy 1.13.0`, `pandas-ta 0.3.14b`.

\*   \*\*ML \& Quant:\*\* `scikit-learn 1.5.0`, `hmmlearn 0.3.2`, `statsmodels 0.14.2`, `pyportfolioopt 1.5.5`, `riskfolio-lib`, `cvxpy`.

\*   \*\*Options:\*\* `py\_vollib\_vectorized 0.1.2`, `QuantLib-Python`.

\*   \*\*LLM:\*\* `ollama 0.2.1` (local), `transformers` (Hugging Face FinBERT), `anthropic`, `openai`.

\*   \*\*Brokers \& Crypto:\*\* `schwab-py 1.2.0`, `robin\_stocks 3.0.4`, `ib\_insync`, `alpaca-trade-api`, `ccxt`, `web3`.

\*   \*\*Async I/O:\*\* `aiohttp 3.9.5`, `aiofiles`, `websockets 12.0`, `httpx`.



\### 2.4 Directory Structure

```text

C:\\TradingSystem\\

├── engine\\

│   ├── api\\             # engine\_api.py (FastAPI on :8765)

│   ├── brain\\           # opportunity\_ranker.py, daily\_pnl\_manager.py, capital\_allocator.py

│   ├── brokers\\         # base\_broker.py, schwab\_broker.py, robinhood\_broker.py, mock\_broker.py, ibkr\_broker.py

│   ├── data\\            # market\_data.py, options\_data.py, macro\_data.py, alternative\_data.py

│   ├── database\\        # models.py, session.py, migrations.py

│   ├── execution\\       # order\_router.py, execution\_engine.py

│   ├── meta\_brain\\      # regime\_detector.py, allocator.py, llm\_analyst.py, portfolio\_optimizer.py

│   ├── risk\\            # risk\_manager.py, compliance.py

│   ├── scanner\\         # opportunity\_scanner.py, stock\_screener.py

│   ├── scheduler\\       # jobs.py

│   ├── strategies\\      # base\_strategy.py, equity/, options/, crypto/, macro/, quant/, intraday/

│   ├── tax\\             # tax\_engine.py, tax\_optimizer.py

│   ├── main.py          # Entry point

│   └── config.py        # Config dataclass, env vars

├── ui\\

│   ├── ui\_server.py     # FastAPI on :8766

│   └── static\\          # index.html, dashboard.js, styles.css

├── shared\\              # trading.db (SQLite)

├── logs\\                # Rotating JSON logs

├── data\_cache\\          # Parquet feature store, sp500\_components.json

└── tests\\               # pytest suite

```



\---



\## 3. DATABASE SCHEMA \& STATE MANAGEMENT



The system uses SQLAlchemy 2.0 declarative syntax. All timestamps are UTC ISO-8601 strings.



\### 3.1 Core Trading Tables

\*   \*\*`trades`\*\*: `id` (PK), `symbol`, `asset\_class` (EQUITY/OPTION/CRYPTO/ETF/CASH), `broker`, `strategy\_id`, `direction` (BUY/SELL/BTO/STC), `qty`, `order\_type`, `limit\_price`, `fill\_price`, `commission`, `slippage\_bps`, `status` (PENDING/FILLED/CANCELLED/REJECTED), `broker\_order\_id`, `fill\_timestamp`, `created\_at`, `notes`.

\*   \*\*`positions`\*\*: `id` (PK), `symbol` (Unique), `asset\_class`, `broker`, `current\_qty`, `average\_cost`, `last\_price`, `unrealized\_pl`, `unrealized\_pl\_pct`, `realized\_pl`, `days\_held`, `strategy\_id`, `stop\_price`, `take\_profit\_price`, `delta`, `theta`, `vega`, `gamma`, `option\_expiry`, `option\_strike`, `option\_type`, `last\_updated`.

\*   \*\*`orders`\*\*: `id` (PK), `parent\_trade\_id`, `broker\_order\_id`, `status`, `fills\_json`, `routing\_reason`, `latency\_ms`.



\### 3.2 Tax \& Compliance Tables

\*   \*\*`tax\_lots`\*\*: `id` (PK), `symbol`, `acquisition\_date`, `qty`, `cost\_basis`, `lot\_method` (FIFO/HIFO/LIFO), `is\_closed`, `close\_date`, `close\_price`, `realized\_gain\_loss`, `is\_long\_term`, `wash\_sale\_disallowed`.

\*   \*\*`wash\_sale\_blacklist`\*\*: `id` (PK), `symbol` (Unique), `loss\_realized\_date`, `expiration\_date` (+31 days), `loss\_amount`, `proxy\_used`.

\*   \*\*`tax\_harvest\_log`\*\*: `id` (PK), `harvest\_date`, `symbol\_sold`, `proxy\_bought`, `qty`, `loss\_captured`, `estimated\_tax\_saving`, `created\_at`.

\*   \*\*`compliance\_audit\_log`\*\*: `id` (PK), `event\_time`, `rule\_name`, `symbol`, `order\_direction`, `order\_qty`, `outcome` (BLOCKED/WARNED/PASSED), `reason`, `strategy\_id`.

\*   \*\*`tax\_optimization\_decisions`\*\*: `id` (PK), `decision\_time`, `symbol`, `position\_pnl`, `holding\_days`, `lot\_method\_chosen`, `alternative\_considered`, `gross\_pnl`, `estimated\_tax\_cost`, `net\_pnl\_after\_tax`, `decision\_reason`, `actual\_tax\_saving\_vs\_fifo`.



\### 3.3 Intelligence \& ML Tables

\*   \*\*`strategy\_performance`\*\*: `id` (PK), `strategy\_id` (Unique), `display\_name`, `asset\_class`, `total\_trades`, `winning\_trades`, `win\_rate`, `total\_pnl`, `avg\_hold\_days`, `sharpe\_ratio`, `max\_drawdown`, `current\_weight`, `bandit\_alpha`, `bandit\_beta`, `is\_enabled`, `last\_updated`.

\*   \*\*`market\_regime\_log`\*\*: `id` (PK), `log\_date` (Unique), `hmm\_state`, `hmm\_probabilities` (JSON), `vix\_level`, `sp500\_return\_5d`, `yield\_spread\_10y2y`, `put\_call\_ratio`, `macro\_score`, `created\_at`.

\*   \*\*`alpha\_signals\_log`\*\*: `id` (PK), `signal\_id`, `strategy\_id`, `symbol`, `direction`, `strength` (0.0-1.0), `conviction` (LOW/MEDIUM/HIGH), `recommended\_size`, `stop\_price`, `take\_profit\_price`, `metadata\_json`, `acted\_on`, `blocked\_by`, `outcome\_pnl`, `created\_at`.

\*   \*\*`opportunity\_scans`\*\*: `id` (PK), `scan\_time`, `symbol`, `opportunity\_type`, `composite\_score`, `technical\_signals\_json`, `catalyst\_flags\_json`, `recommended\_strategies\_json`, `acted\_on`, `outcome\_pnl`.

\*   \*\*`alternative\_signals`\*\*: `id` (PK), `signal\_time`, `source` (INSIDER/CONGRESS/REDDIT/FINBERT/GOOGLE\_TRENDS), `symbol`, `signal\_type`, `signal\_value`, `confidence`, `acted\_on`, `outcome\_pnl\_if\_acted`.

\*   \*\*`feature\_store`\*\*: `symbol`, `date`, `rsi`, `macd`, `atr`, `vix`, `sentiment\_score`, `dark\_pool\_vol`, `funding\_rate`, `on\_chain\_flow`, `parquet\_path`.



\### 3.4 Capital \& System State Tables

\*   \*\*`portfolio\_snapshots`\*\*: `id` (PK), `snapshot\_time` (Unique), `total\_equity`, `cash\_balance`, `positions\_value`, `daily\_pnl`, `total\_pnl`, `num\_open\_positions`, `drawdown\_pct`, `sharpe\_rolling\_30d`, `var\_99`, `regime\_state`.

\*   \*\*`daily\_cycle\_log`\*\*: `id` (PK), `cycle\_date`, `starting\_capital`, `ending\_equity`, `daily\_pnl`, `daily\_pnl\_pct`, `profit\_extracted`, `profit\_wallet\_cumulative`, `cycle\_state` (NORMAL/RECOVERY/HALTED), `num\_trades`, `winning\_trades`, `losing\_trades`, `largest\_win`, `largest\_loss`, `strategies\_used` (JSON), `regime\_state`, `notes`.

\*   \*\*`profit\_wallet`\*\*: `id` (PK), `extraction\_date`, `amount`, `cumulative\_balance`, `cycle\_state\_at\_extraction`, `daily\_pnl\_at\_extraction`, `notes`.

\*   \*\*`recovery\_sessions`\*\*: `id` (PK), `start\_date`, `trigger\_loss`, `recovery\_target`, `days\_allowed`, `days\_used`, `amount\_recovered`, `status` (IN\_PROGRESS/SUCCESS/TIMEOUT/ABANDONED), `strategy\_adjustments\_json`.

\*   \*\*`control\_flags`\*\*: `id` (PK), `flag\_key` (Unique), `flag\_value`, `updated\_by`, `updated\_at`. (Pre-populated: `trading\_enabled=true`, `shadow\_mode=true`, `llm\_analysis\_enabled=true`, `tlh\_enabled=true`, `crypto\_enabled=false`, `options\_enabled=false`, `meta\_brain\_enabled=true`, `engine\_status=STOPPED`).

\*   \*\*`hedge\_positions`\*\*: `id` (PK), `symbol`, `hedge\_type` (SPY\_PUT/VXX/INVERSE\_ETF), `qty`, `cost`, `current\_value`, `hedge\_ratio`, `portfolio\_delta\_offset`, `opened\_at`, `closed\_at`, `pnl`.



\---



\## 4. DATA INGESTION \& ALTERNATIVE DATA ENGINE



All data fetching is asynchronous. Blocking libraries (e.g., `yfinance`) are executed via `asyncio.get\_event\_loop().run\_in\_executor()`. Data is cached locally in Parquet files (`data\_cache/`).



\### 4.1 Market Data (`engine/data/market\_data.py`)

\*   \*\*Historical OHLCV:\*\* Fetched via `yfinance` (fallback) or `polygon.io` (primary). Cached as `{symbol}\_{period}\_{interval}.parquet`.

\*   \*\*Real-Time Quotes:\*\* Fetched via `yfinance` `Ticker.fast\_info`, Finnhub WebSockets, or Polygon WebSockets. Normalizes to `QuoteEvent` dataclass (`symbol, price, bid, ask, volume, timestamp\_ns, source`).

\*   \*\*Batch Quotes:\*\* Uses `asyncio.gather()` with `asyncio.Semaphore(10)` for rate limiting.

\*   \*\*Indicators (`pandas\_ta`):\*\* Calculates RSI(14), MACD(12,26,9), Bollinger Bands(20,2), ATR(14), EMA(9,21,50), ADX(14), OBV, Stochastic(14,3).

\*   \*\*Macro Data:\*\* Fetched synchronously from FRED API (DGS10, DGS2, FEDFUNDS, CPIAUCSL). Cached for 24 hours.

\*   \*\*Economic Calendar:\*\* Scrapes Yahoo Finance / Investing.com for earnings and FOMC events.



\### 4.2 Options Data (`engine/data/options\_data.py`)

\*   \*\*Options Chain:\*\* Fetched via `yfinance` `Ticker.option\_chain(expiry)` or Polygon Options API + CBOE CFE feed.

\*   \*\*Greeks Calculation:\*\* Uses `py\_vollib\_vectorized` to calculate Delta, Gamma, Theta, Vega, and Rho based on spot, strike, days\_to\_expiry, IV, and risk-free rate.

\*   \*\*Portfolio Greeks:\*\* Aggregates net Greeks across all open option positions.



\### 4.3 Alternative Data (`engine/data/alternative\_data.py`)

\*   \*\*Insider Trades:\*\* Scrapes OpenInsider. Filters for "P - Purchase", value > $50,000. Detects cluster buys (3+ insiders in 14 days).

\*   \*\*Congressional Trades:\*\* Scrapes CapitolTrades / QuiverQuant API. Filters for "Purchase".

\*   \*\*Reddit Sentiment:\*\* Uses PRAW to scan `r/wallstreetbets`, `r/stocks`, `r/investing`. Calculates `mention\_velocity` and `sentiment\_ratio`.

\*   \*\*FinBERT Sentiment:\*\* Uses local Hugging Face `ProsusAI/finbert` model. Tokenizes news/headlines and returns a score from -1.0 to +1.0.

\*   \*\*Google Trends:\*\* Uses `pytrends` to track 7-day velocity for keywords like "buy stocks", "stock market crash", "buy gold".

\*   \*\*13F Filings:\*\* Uses `sec-edgar-downloader` to fetch filings for top 20 hedge funds, extracting new positions.

\*   \*\*Short Interest:\*\* Scrapes Finviz for `short\_float\_pct`, `short\_ratio`, and `short\_interest`.

\*   \*\*On-Chain Data:\*\* Glassnode API for BTC/ETH exchange netflows and miner data.



\---



\## 5. BROKER INTEGRATION \& SMART ORDER ROUTING



\### 5.1 Universal Broker Interface (`BaseBroker`)

Abstract base class requiring: `get\_quote()`, `get\_option\_chain()`, `submit\_order()`, `cancel\_order()`, `get\_positions()`, `get\_account\_balance()`, `get\_order\_status()`.

\*   \*\*Circuit Breaker:\*\* Decorator tracks consecutive errors. If `error\_count >= 3` in 60s, sets `\_circuit\_open = True`, logs CRITICAL, and pauses routing to that broker for 5 minutes.

\*   \*\*Retry Policy:\*\* Exponential backoff (1s, 2s, 4s + jitter) for `aiohttp.ClientError` and `asyncio.TimeoutError`.



\### 5.2 Broker Implementations

1\.  \*\*SchwabBroker:\*\* Uses `schwab-py`. OAuth2 PKCE flow with token auto-refresh (proactive refresh if < 5 min remaining). Handles standard equities and options.

2\.  \*\*RobinhoodBroker:\*\* Uses `robin\_stocks`. Handles TOTP via `pyotp`. Supports fractional shares (`fractional=True` if qty < 1), 24/5 extended hours, and crypto routing.

3\.  \*\*IBKRBroker:\*\* Uses `ib\_insync`. Direct market access for equities, futures, FX, and complex options. Used for orders > $100k notional.

4\.  \*\*AlpacaBroker:\*\* Supports paper/live modes, crypto, and portfolio margin.

5\.  \*\*CoinbaseBroker:\*\* Advanced Trade API for crypto spot and perpetuals.

6\.  \*\*MockBroker (Shadow Mode):\*\* Maintains in-memory virtual positions and cash (default $50,000). Simulates fills using real market data. Market orders fill at `last\_price \* (1 + slippage)` where slippage \~ N(0, 0.0003).



\### 5.3 Smart Order Router (SOR) \& Execution Engine

The `SmartOrderRouter.route()` method evaluates rules in order:

1\.  \*\*Shadow Mode:\*\* If `control\_flags\["shadow\_mode"] == "true"` -> `MockBroker`.

2\.  \*\*Crypto:\*\* If `asset\_class == "CRYPTO"` -> `CoinbaseBroker` or `RobinhoodBroker`.

3\.  \*\*Options:\*\* If `asset\_class == "OPTION"` -> `SchwabBroker` or `IBKRBroker`.

4\.  \*\*Size:\*\* If order > $100k notional -> `IBKRBroker`.

5\.  \*\*After-Hours:\*\* If time < 09:29 or > 16:01 ET -> `RobinhoodBroker` or `AlpacaBroker`.

6\.  \*\*Fractional:\*\* If `qty < 1.0` -> `RobinhoodBroker`.

7\.  \*\*Standard Equity:\*\* Queries eligible brokers, routes to best bid/ask, defaults to `SchwabBroker`.



\*\*Execution Algorithms:\*\*

\*   \*\*TWAP:\*\* Splits large orders into time-weighted slices over a configurable window.

\*   \*\*VWAP:\*\* Slices orders per 5-min volume histograms to minimize market impact.

\*   \*\*Iceberg:\*\* Shows only 10% of order size, auto-refilling as fills arrive.



\---



\## 6. THE META-BRAIN (AI \& QUANT CORE)



\### 6.1 Market Regime Detector (`engine/meta\_brain/regime\_detector.py`)

\*   \*\*Model:\*\* `hmmlearn.hmm.GaussianHMM(n\_components=6, covariance\_type="diag", n\_iter=200)`.

\*   \*\*Features:\*\* 2 years of SPY daily data. Feature matrix `X`: `\[daily\_return, log\_volume, vix\_norm, atr\_norm, macd\_hist\_norm, yield\_spread\_10y2y, put\_call\_ratio]`.

\*   \*\*States:\*\* `BULL\_TREND`, `BEAR\_TREND`, `SIDEWAYS\_LOW\_VOL`, `SIDEWAYS\_HIGH\_VOL`, `CRASH\_RISK`, `RECOVERY`.

\*   \*\*Output:\*\* Returns current state, probability distribution, and regime multipliers (e.g., BULL\_TREND multiplies Trend Following by 1.5, Mean Reversion by 0.5).



\### 6.2 Opportunity Scanner \& Screener (`engine/scanner/`)

\*   \*\*Universe:\*\* S\&P 500 (scraped from Wikipedia), 11 SPDR sector ETFs, leveraged ETFs, crypto majors.

\*   \*\*Tier 1 Filters:\*\* `avg\_daily\_volume > $5M`, `$1 < price < $5000`, `bid\_ask\_spread < 0.5%`, `ATR/Price > 0.5%`.

\*   \*\*Tier 2 Scoring (`score\_opportunity`):\*\*

&#x20;   \*   `momentum\_score`: Normalized RSI distance from 50.

&#x20;   \*   `volume\_score`: `min(today\_volume / avg\_20d\_volume / 3.0, 1.0)`.

&#x20;   \*   `trend\_score`: `1.0` if ADX > 25, else `ADX/25`.

&#x20;   \*   `catalyst\_score`: Sum of binary flags (earnings, insider buy, news) \* 0.2.

&#x20;   \*   `composite\_score`: `0.25\*momentum + 0.20\*volume + 0.15\*trend + 0.20\*catalyst + 0.20\*regime`.

\*   Outputs `SetupOpportunity` dataclass to the Strategy Matcher.



\### 6.3 Capital Allocator (`engine/meta\_brain/allocator.py`)

\*   \*\*Contextual Thompson Sampling:\*\* Maintains a Beta distribution `Beta(alpha, beta)` for each `(strategy\_id, regime)` pair.

\*   \*\*Update Rule:\*\* Win -> `alpha += 1`, Loss -> `beta += 1`.

\*   \*\*Allocation:\*\* Samples from the posterior, multiplies by the regime compatibility matrix and a 14-day recency weight. Normalizes weights to sum to 1.0, enforcing a minimum 5% floor (`min\_weight=0.05`) for enabled strategies.



\### 6.4 Multi-LLM Analyst (`engine/meta\_brain/llm\_analyst.py`)

\*   \*\*Primary:\*\* `ollama.Client(host=OLLAMA\_BASE\_URL)` running `llama3.3` or `mistral-large`.

\*   \*\*Prompts:\*\*

&#x20;   \*   \*News:\* Extract `{"sentiment\_score": 0-100, "direction": "BULLISH|BEARISH", "confidence": 0.0-1.0}`.

&#x20;   \*   \*Earnings:\* Extract `{"guidance\_revision": "UP|DOWN", "surprise\_factor": "BEAT|MISS"}`.

&#x20;   \*   \*10-K:\* Extract `{"risk\_score": 0-100, "key\_risks": \[]}`.

\*   \*\*Ensemble Voting:\*\* If local LLM and fallback cloud LLM (Anthropic) disagree by > 30 points, the system abstains.



\### 6.5 Portfolio Optimizer (`engine/meta\_brain/portfolio\_optimizer.py`)

\*   \*\*PyPortfolioOpt:\*\* Uses `mean\_historical\_return()` and `CovarianceShrinkage().ledoit\_wolf()`. Objective: `max\_sharpe()`. Weight bounds: `(0.02, 0.25)` per asset.

\*   \*\*Riskfolio-Lib:\*\* Calculates CVaR-constrained mean-variance frontier.

\*   \*\*Monte Carlo VaR:\*\* Simulates 5,000 portfolio paths using Cholesky decomposition to calculate 1-day 99% VaR.



\---



\## 7. STRATEGY ARSENAL (50+ STRATEGIES)



All strategies inherit from `BaseStrategy(ABC)` and implement `generate\_signals(df, portfolio\_state) -> list\[SignalEvent]` and `calculate\_position\_size()`. Default sizing uses the Kelly Criterion: `f = (win\_rate/avg\_loss - (1-win\_rate)/avg\_win) \* 0.25`, capped at 10% of equity.



\### 7.1 Equity Momentum \& Intraday (EQ-01 to EQ-07, A1-A7)

\*   \*\*EQ-01 / Trend Following:\*\* BUY if EMA-9 crosses above EMA-21, EMA-21 > EMA-50, ADX-14 > 25, RSI 45-75. Stop: `close - 2\*ATR`. TP: `close + 4\*ATR`.

\*   \*\*A1 / Opening Range Breakout (ORB):\*\* Calculates high/low of 9:30-9:45 candles. BUY if price breaks ORB high with volume > 2x average. Signals generated only until 11:30 AM.

\*   \*\*A2 / VWAP Momentum:\*\* BUY on first pullback to VWAP if price > VWAP, VWAP slope > 0, and RSI bounces from 45-55.

\*   \*\*A3 / Gap-and-Go:\*\* Pre-market gap > 3%. Requires float < 100M or LLM news sentiment > 70. Enter at 9:32 AM if holding above prior close.

\*   \*\*A4 / Relative Strength Rotation:\*\* Ranks 11 SPDR ETFs by 5d/20d momentum. Long top 3, short bottom 1.

\*   \*\*A6 / 52-Week High Breakout:\*\* Scan for new 52-week highs with volume > 2x. Enter on first intraday pullback.

\*   \*\*A7 / Unusual Volume Spike:\*\* Volume > 3x 20-day average without news.



\### 7.2 Equity Mean Reversion (B1-B6)

\*   \*\*EQ-03 / Mean Reversion:\*\* BUY if close < Lower Bollinger Band (BBL), RSI-14 < 32, Stoch-K < 25, and next bar opens above BBL. SELL if close > BBU.

\*   \*\*B1 / BB Squeeze Breakout:\*\* Detects BB Width at 6-month low. Enters on breakout confirmed by MACD histogram turning positive.

\*   \*\*B2 / RSI Divergence:\*\* Price makes new low, RSI makes higher low. Confirmed by MACD cross.

\*   \*\*B3 / Oversold Large-Cap Bounce:\*\* S\&P 500 stocks with RSI < 28, price < BBL, no earnings in 5 days.

\*   \*\*B4 / Intraday VWAP Deviation:\*\* Fades deviations > 1.5% from VWAP by 11:00 AM.

\*   \*\*B5 / Monday Gap Fade:\*\* Fades Monday open gaps > 0.5% without macro catalysts.



\### 7.3 Options Strategies (OP-01 to OP-06, C1-C7)

\*   \*\*OP-01 / 0DTE Iron Condor:\*\* SPX/SPY daily. Entry: VIX < 18, IV Rank > 50%. Sells 16-delta OTM call/put, buys wings 2 strikes further. Closes at 50% profit or 200% loss, or at 15:00 ET.

\*   \*\*OP-02 / Volatility Skew Arb:\*\* Buys cheap skew (low put/call IV ratio), hedges with VIX futures.

\*   \*\*OP-03 / Covered Call Yield:\*\* Writes 30 DTE, 0.30 delta calls on existing long equity holdings held > 1 day. Rolls at 21 DTE.

\*   \*\*OP-04 / Protective Put:\*\* Buys 90 DTE, 0.10 delta puts on SPY. Size = 2% NAV/year.

\*   \*\*OP-06 / Earnings IV Crush:\*\* Sells straddle day before earnings if IV Rank > 80%. Closes 30 mins before market close on earnings day.

\*   \*\*C4 / Cash-Secured Put:\*\* Sells OTM puts 5-10% below current price, 30-45 DTE on target acquisition stocks.

\*   \*\*C6 / Poor Man's Covered Call:\*\* Buys deep ITM LEAPS (0.80 delta, 6-12 mo), sells short-dated OTM calls against it.



\### 7.4 Copy Trading \& Sentiment (D1-D7)

\*   \*\*D1 / Congress Trade Replication:\*\* Scrapes OpenInsider/housestockwatcher. Replicates purchases > $15,000 within 48 hours of public filing. Size: 1% NAV.

\*   \*\*D2 / Insider Cluster Buy:\*\* Scrapes OpenInsider. Triggers if 3+ officers buy > $50,000 in open market within 14 days.

\*   \*\*D3 / FinBERT Sentiment:\*\* Runs local Hugging Face FinBERT on NewsAPI/Reddit. BUY if sentiment > 0.6, SELL if < -0.4.

\*   \*\*D4 / WSB Reddit Momentum:\*\* Scans PRAW every hour. Triggers if mention count spikes > 3 SD and short interest is high.

\*   \*\*D5 / Google Trends Catalyst:\*\* Maps rising search velocity (e.g., "buy gold") to ETFs (GLD).

\*   \*\*D7 / Institutional 13F:\*\* Tracks top 20 hedge funds' new positions via SEC EDGAR. Buys within 30 days of filing.



\### 7.5 Quantitative \& Statistical Arbitrage (EQ-02, E1-E8)

\*   \*\*EQ-02 / Stat Arb Pairs:\*\* Runs Engle-Granger cointegration test (p < 0.05) on 200+ ETF pairs. Calculates spread Z-score (60-day rolling). BUY leg A / SELL leg B if Z < -2.0. Exit at 0.

\*   \*\*E2 / Volatility Regime Switching:\*\* Ratio of 20-day realized vol to VIX. If RV/IV < 0.7, sell premium. If > 1.3, buy options.

\*   \*\*E3 / Cross-Asset Correlation Break:\*\* Tracks 20-day correlation (e.g., BTC/NASDAQ). Trades divergence > 2 SD.

\*   \*\*E5 / Factor Momentum:\*\* Scores S\&P 500 on Value (P/E, P/B), Momentum (12-1 mo), Quality (ROE). Long top quintile, short bottom quintile.

\*   \*\*E6 / Lead-Lag Sector:\*\* Trades lagging sectors in the direction of leading sectors (e.g., Tech leads Consumer Discretionary by 3 days).



\### 7.6 Macro \& Thematic (FX-03, F1-F6)

\*   \*\*F1 / Rate-Sensitive Rotation:\*\* If 10Y Treasury yield rises > 5bps, rotate from XLK (Tech) to XLF (Financials)/XLV (Value).

\*   \*\*F2 / VIX Mean Reversion:\*\* VIX > 28 -> buy SPY. VIX < 13 -> buy VXX.

\*   \*\*F3 / Fed Calendar:\*\* Buys VXX 3 days before FOMC; sells at open on FOMC day.

\*   \*\*F4 / CPI Release:\*\* If consensus CPI > prior, buy energy/short TLT.

\*   \*\*F5 / Gold/Dollar Inverse:\*\* If DXY falls > 0.5%, buy GLD.

\*   \*\*F6 / Commodity-to-Equity:\*\* If Oil futures (CL=F) rise > 1.5%, buy XLE.



\### 7.7 Crypto, FX, \& Fixed Income (CR-01 to CR-05, FX-01 to FX-02, FI-01 to FI-02)

\*   \*\*CR-01 / Crypto Trend:\*\* 4H MACD histogram + OBV divergence on BTC/ETH.

\*   \*\*CR-02 / CEX/DEX Arb:\*\* Compares Coinbase spot vs Uniswap V3. Executes via Web3 if spread > 0.3%.

\*   \*\*CR-03 / Funding Rate Harvest:\*\* Holds long BTC perps on Bybit/Coinbase if funding rate > 0.01%/8h.

\*   \*\*CR-04 / On-Chain Whale Alert:\*\* Glassnode exchange outflow > 3 SD spike -> bullish signal.

\*   \*\*FX-01 / G10 Carry:\*\* Long AUD/USD + NZD/USD vs short USD/JPY + CHF.

\*   \*\*FI-01 / Duration Ladder:\*\* Rotates 4-week, 3-month, 6-month T-bills.



\### 7.8 Cash Management \& Hedging (CM-01, CM-02, EQ-04)

\*   \*\*CM-01 / Money Market Sweep:\*\* At 15:50 ET, if cash > $1000, buys SWVXX (Schwab) or VMFXX (Vanguard) leaving a $500 buffer. Sells at 09:31 AM.

\*   \*\*EQ-04 / Flash Crash:\*\* At 09:28 AM, places 5 limit BUY orders at -5%, -8%, -12%, -16%, -20% below prior close for SPY/QQQ. Cancels at 10:00 AM.

\*   \*\*Hedge Ladder:\*\* Maintains 1-2 far OTM SPY puts (5% OTM, 30-60 DTE). Allocates 5-10% to SQQQ if HMM regime is BEAR\_TREND or CRASH\_RISK.



\---



\## 8. RISK MANAGEMENT \& COMPLIANCE ENGINE



The `RiskManager` executes a strict, ordered 12-step pipeline (`engine/risk/risk\_manager.py`). If any check fails, the order is blocked, logged to `compliance\_audit\_log`, and execution halts.



\### 8.1 Pre-Trade Risk Pipeline

1\.  \*\*System Halt:\*\* Blocks if `control\_flags\["trading\_enabled"] == "false"`.

2\.  \*\*Shadow Mode:\*\* Blocks live broker routing if `shadow\_mode == "true"`.

3\.  \*\*PDT Rule (FINRA 4210):\*\* Counts FILLED trades in the last 5 calendar days with hold\_time < 1 day. Blocks the 4th trade if total equity < `PDT\_EQUITY\_BUFFER` ($26,500).

4\.  \*\*Wash-Sale (IRC §1091):\*\* Queries `wash\_sale\_blacklist`. Blocks BUYs if expiration > today. Blocks SELLs at a loss if the same symbol was bought within 30 days. Offers proxy swap from `PROXY\_SWAP\_MAP` (e.g., SPY->VOO).

5\.  \*\*Position Concentration:\*\* If order value / total equity > `MAX\_SINGLE\_POSITION\_PCT` (0.10), resizes `modified\_qty` to fit the limit.

6\.  \*\*Sector Concentration:\*\* Uses yfinance `info\["sector"]`. Blocks if sector exposure > `MAX\_SECTOR\_PCT` (0.35).

7\.  \*\*Liquidity:\*\* Blocks if `order.qty \* fill\_price > 0.05 \* avg\_daily\_volume\_usd` (20-day ADTV).

8\.  \*\*Portfolio Correlation:\*\* Calculates 60-day Pearson correlation. Warns if `r > MAX\_CORRELATION\_THRESHOLD` (0.75) with existing holdings.

9\.  \*\*Crypto Toggle:\*\* Blocks CRYPTO if `crypto\_enabled == "false"`.

10\. \*\*Options Toggle:\*\* Blocks OPTION if `options\_enabled == "false"`.

11\. \*\*Intraday Drawdown:\*\* Calculates `(opening\_equity - current\_equity) / opening\_equity`. If > `INTRADAY\_DRAWDOWN\_HALT\_PCT` (0.02), blocks new entries. If > `INTRADAY\_DRAWDOWN\_CLOSE\_PCT` (0.04), liquidates all day-trades.

12\. \*\*Leverage (Reg-T):\*\* Calculates `total\_notional\_exposure / total\_equity`. Blocks if > `MAX\_PORTFOLIO\_LEVERAGE` (2.0x overnight, 4x intraday).



\### 8.2 Real-Time \& Post-Trade Risk

\*   \*\*ATR Trailing Stops:\*\* Updated daily. `stop = close - (2 \* ATR-14)`.

\*   \*\*Profit-Lock Ratchet:\*\* Once a position reaches +20% unrealized PnL, the stop price is ratcheted up to +10% to guarantee profit.

\*   \*\*Reg SHO Locate:\*\* Placeholder check for short-sale locate confirmation with prime brokers.

\*   \*\*MiFID II Best Execution:\*\* Logs all venue quotes considered before routing.

\*   \*\*Insider Trading Guardrail:\*\* Cross-references LLM-extracted SEC 8-K material events; blocks trading in affected tickers for 72 hours.



\---



\## 9. TAX OPTIMIZATION ENGINE



The `TaxAwarePortfolioManager` (`engine/tax/tax\_optimizer.py`) treats net-after-tax return as the primary metric.



\### 9.1 Lot Selection Intelligence

For every SELL order, the engine evaluates four accounting methods to maximize `net\_after\_tax` proceeds:

1\.  \*\*FIFO:\*\* First-In, First-Out (IRS default).

2\.  \*\*HIFO:\*\* Highest-In, First-Out (minimizes current capital gains).

3\.  \*\*LTCG\_FIRST:\*\* Prioritizes lots held > 365 days to secure 0/15/20% long-term rates instead of 22-37% short-term rates.

4\.  \*\*LOSS\_FIRST:\*\* Prioritizes losing lots to harvest losses and defer gains.

The chosen method is logged to `tax\_optimization\_decisions` along with the `actual\_tax\_saving\_vs\_fifo`.



\### 9.2 Tax-Loss Harvesting (TLH) \& Proxy Swaps

\*   \*\*Scan:\*\* Runs at 16:15 ET. Identifies open positions with `unrealized\_pl < -TLH\_MIN\_LOSS\_THRESHOLD` (-$500).

\*   \*\*Execution:\*\* Sells the loser at market, adds to `wash\_sale\_blacklist` (expiry = today + 31 days), immediately buys the proxy from `PROXY\_SWAP\_MAP`, and logs to `tax\_harvest\_log`.

\*   \*\*Estimated Saving:\*\* `loss\_captured \* 0.35` (assuming 35% marginal rate).



\### 9.3 Gain Deferral Optimizer

\*   Evaluates profitable short-term positions held between 335 and 365 days.

\*   Calculates `tax\_saving = gross\_gain \* (stcg\_rate - ltcg\_rate)`.

\*   Calculates `hedge\_cost` (estimated ATM put premium for remaining days).

\*   If `tax\_saving > hedge\_cost \* 1.5`, recommends holding the asset and buying a protective put to lock in the gain without triggering a constructive sale.



\### 9.4 Reporting \& Year-End Planning

\*   \*\*Quarterly Estimates:\*\* Projects tax liability ahead of April 15, June 15, Sept 15, Jan 15 deadlines.

\*   \*\*December Mode:\*\* Aggressive TLH scan if projected STCG > $5,000.

\*   \*\*Form 8949 Export:\*\* Generates an IRS-compatible CSV of all closed lots, grouping short-term (Group A) and long-term (Group D), and applying wash-sale adjustments in Column G.



\---



\## 10. DAILY CYCLE \& TASK SCHEDULING



The system is orchestrated by APScheduler (Local) or Celery Beat (Enterprise) using `America/New\_York` timezone.



\### 10.1 The 24-Hour Schedule (`engine/scheduler/jobs.py`)

1\.  \*\*`pre\_market\_routine` (04:00 ET, Mon-Fri):\*\*

&#x20;   \*   Sets `engine\_status = "PRE\_MARKET"`.

&#x20;   \*   Refreshes OAuth tokens; verifies broker balances.

&#x20;   \*   Fetches FRED macro data, economic calendar, and SEC filings.

&#x20;   \*   Runs `OpportunityScanner.run\_premarket\_scan()`.

&#x20;   \*   Runs LLMAnalyst on overnight news.

&#x20;   \*   Places FlashCrashStrategy limit orders.

2\.  \*\*`market\_open\_prep` (09:28 ET, Mon-Fri):\*\*

&#x20;   \*   Sets `engine\_status = "MARKET\_HOURS"`.

&#x20;   \*   Sets OCO brackets on all active positions.

&#x20;   \*   Calculates opening portfolio state; saves to `portfolio\_snapshots`.

3\.  \*\*`main\_trading\_cycle` (09:30 - 16:01 ET, every 5 mins, Mon-Fri):\*\*

&#x20;   \*   Checks `trading\_enabled` flag.

&#x20;   \*   Calculates `portfolio\_state`.

&#x20;   \*   Runs `OpportunityScanner.run\_full\_scan()`.

&#x20;   \*   Meta-Brain updates regime and allocation weights.

&#x20;   \*   For each enabled strategy: fetches data, calculates indicators, generates signals.

&#x20;   \*   For signals with strength > 0.3: calculates size, runs RiskManager, routes via ExecutionEngine.

&#x20;   \*   Calls `update\_positions\_prices()` (triggers stops/take-profits).

&#x20;   \*   Calls `DailyPnLManager.lock\_in\_profits()`.

4\.  \*\*`options\_management` (15:00 ET, Mon-Fri):\*\*

&#x20;   \*   Closes 0DTE options at MARKET.

&#x20;   \*   Closes options at 50% profit or 200% loss.

5\.  \*\*`daily\_settlement` (15:55 ET, Mon-Fri):\*\*

&#x20;   \*   Calls `DailyPnLManager.end\_of\_day\_settlement()`. Updates `daily\_cycle\_log` and `profit\_wallet`. Transitions to RECOVERY\_MODE if daily PnL is negative.

6\.  \*\*`after\_hours\_routine` (16:15 ET, Mon-Fri):\*\*

&#x20;   \*   Sets `engine\_status = "AFTER\_HOURS"`.

&#x20;   \*   Updates ATR trailing stops.

&#x20;   \*   Runs `MoneyMarketSweepStrategy`.

&#x20;   \*   Runs `TaxAwarePortfolioManager.evaluate\_all\_positions()` (TLH scan).

&#x20;   \*   Calculates EOD VaR and saves snapshot.

7\.  \*\*`crypto\_after\_hours` (17:00 - 09:00 ET, every 15 mins):\*\*

&#x20;   \*   Runs CR-01 trend strategy on 4H candles. Monitors funding rates.

8\.  \*\*`nightly\_maintenance` (23:55 ET, Mon-Fri):\*\*

&#x20;   \*   Executes profit sweep log (ACH transfer alert).

&#x20;   \*   Generates daily performance report (JSON/HTML/PDF).

&#x20;   \*   Retrains HMM if > 7 days old.

&#x20;   \*   Runs Optuna hyperparameter tuning on last 90 days.

&#x20;   \*   Backs up SQLite DB to `data\_cache/backups/`.

9\.  \*\*`weekend\_review` (Sat 08:00 ET):\*\*

&#x20;   \*   Full portfolio rebalance via PyPortfolioOpt.

&#x20;   \*   Clears expired wash-sale blacklists.

&#x20;   \*   Updates `strategy\_performance` stats (win\_rate, sharpe, max\_dd).

10\. \*\*`health\_monitor` (Every 1 min, 24/7):\*\*

&#x20;   \*   Checks broker circuit breakers, DB write latency, and updates heartbeat timestamp.



\---



\## 11. CONTROL UI \& OBSERVABILITY



The Control UI is an independent FastAPI process (`ui/ui\_server.py` on port 8766) serving a single-page HTML/JS dashboard. It communicates with the Engine API (`engine/api/engine\_api.py` on port 8765).



\### 11.1 Engine API Endpoints

\*   `GET /health`: Returns `{status, engine\_status, timestamp, is\_live, shadow\_mode}`.

\*   `GET /portfolio`: Returns full `portfolio\_state` dict (equity, cash, daily\_pnl, drawdown\_pct, var\_99).

\*   `GET /positions`, `GET /trades`, `GET /signals`, `GET /strategies`, `GET /regime`.

\*   `GET /tax/summary`: Returns YTD STCG, LTCG, harvested losses.

\*   `GET /tax/form8949`: Returns CSV FileResponse.

\*   `POST /control/flag`: Updates `control\_flags` table.

\*   `POST /control/strategy/{id}/toggle`: Toggles `is\_enabled`.

\*   `POST /control/halt`: Sets `trading\_enabled=false`, cancels open limit orders.

\*   `POST /control/resume`: Sets `trading\_enabled=true`.

\*   \*\*WebSocket (`ws://localhost:8765/ws`):\*\* Broadcasts `portfolio\_tick` every 10s, `trade\_executed` immediately on fill, and `regime\_change`.



\### 11.2 Dashboard UI Panels (Dark Theme, JetBrains Mono)

1\.  \*\*Header:\*\* Live equity, Daily PnL, Drawdown, Regime State, and a prominent red `■ HALT TRADING` button.

2\.  \*\*Daily Cycle Tracker:\*\* Shows Starting Capital ($10,000), Current Equity, Profit Target progress bar, Profit Locked amount, Cycle State (NORMAL/RECOVERY), and cumulative Profit Wallet.

3\.  \*\*Equity Curve:\*\* Chart.js line chart (30-day history) comparing portfolio equity vs SPY/BTC.

4\.  \*\*Opportunity Scanner Feed:\*\* Live-scrolling list of top 5 setups (Rank, Symbol, Type, Score, Strategy).

5\.  \*\*Open Positions Table:\*\* Symbol, P\&L (green/red), Stop Price (with warning icon if within 2%), Size. Expandable for Greeks.

6\.  \*\*Strategy Performance Matrix:\*\* Toggles for each strategy, showing 7d PnL, Win Rate, Thompson Sampling Weight (animated bar), and Regime compatibility checkmarks.

7\.  \*\*Tax Dashboard:\*\* YTD STCG/LTCG, Harvested Losses, Net Tax Liability, Tax Efficiency vs Naive FIFO, and "Download Form 8949" button.

8\.  \*\*Alternative Data Feed:\*\* Auto-scrolling log of Insider buys, Congress trades, Reddit spikes, and FinBERT sentiment.

9\.  \*\*Recovery Mode Tracker:\*\* (Visible only in recovery) Shows Trigger Loss, Recovery Target, Recovered So Far, Days Used, and Position Size Multiplier (0.5x).

10\. \*\*Parameter Overrides:\*\* Live inputs to adjust Daily Profit Target, Max Daily Loss, Position Size Multiplier, and Risk Per Trade without restarting the engine.

