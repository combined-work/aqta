# AQTA Implementation Gap Analysis

## 1. Capital Framework & State Machine
- [x] DailyPnLManager implementation
- [x] Dynamic target calculation (% based)
- [x] Override logic (USD/PCT)
- [x] Profit lock mechanism
- [ ] Recovery Mode duration and risk adjustment (halving sizes)
- [ ] Compounding Mode triggering (5-day streak)

## 2. NLP Engine (3-Tier)
- [x] Tier 3 (VADER) implementation
- [ ] Tier 2 (SLM - FinBERT/ONNX) - Placeholder exists, needs model loading logic
- [ ] Tier 1 (LLM - Ollama/Cloud) - Placeholder exists
- [ ] Automatic fallback and logging to `llm_fallback_log`

## 3. Risk Engine (15-Step Pipeline)
- [x] Step 1: System Halt Guard
- [x] Step 2: Shadow Mode Router
- [ ] Step 3: Emergency Halt Guard (Improving)
- [x] Step 4: Intraday Drawdown Check
- [x] Step 5: PDT Rule (Count logic needs completion)
- [ ] Step 6: Wash-Sale (Check logic needs completion)
- [x] Step 7: Position Concentration
- [ ] Step 8: Sector Concentration
- [ ] Step 9: Liquidity Filter
- [ ] Step 10: Portfolio Correlation Check
- [x] Step 11: Asset Class Toggle Check
- [ ] Step 12: Leverage (Reg-T)
- [ ] Step 13: Flash Crash Correlation Spike (NEW)
- [ ] Step 14: Liquidity Dry-Up Guard (NEW)
- [ ] Step 15: Strategy Drawdown Halt (NEW)

## 4. State Management
- [ ] `StateCacheManager` (Redis + Asyncio Fallback)

## 5. Database & Analytics
- [x] SQLite schema (18 tables)
- [ ] DuckDB Analytics layer initialization
- [ ] SQLite -> DuckDB ETL logic (`sync_to_duckdb`)

## 6. Strategies
- [x] BaseStrategy interface
- [x] StrategyLoader (Dynamic loading)
- [x] Momentum (EQ-01, A1, A2)
- [ ] Mean Reversion (B1-B14) - Need more
- [ ] Options (OP-01-OP-12) - Need framework
- [ ] Crypto (CR-01-CR-07) - Need framework
- [ ] Macro (F1-F18) - Need framework
- [ ] Sentiment (D1-D16) - Need framework
- [ ] Health Check implementation in all strategies

## 7. Execution & Scheduler
- [x] ExecutionEngine (batch execution)
- [x] SmartOrderRouter (8-rule chain)
- [x] 16-step daily schedule using APScheduler
- [ ] Filling the `pass` statements in scheduler jobs with actual logic

## 8. UI (10-Tab SPA)
- [x] Overview Tab
- [x] Strategies Tab
- [x] Positions Tab
- [ ] Analytics Tab
- [ ] Options Tab
- [ ] Scanner Tab
- [ ] Tax Tab
- [ ] Backtest Tab
- [x] System Health Tab (Basic)
- [ ] Settings Tab
- [ ] Trade Replay Modal
- [ ] Real-time updates via WebSockets for all components

## 9. Tax Optimization
- [x] TaxEngine (Lot selection methods)
- [ ] TLH opportunity cost analysis
- [ ] IRS Form 8949 generation

## 10. Deployment & Scripts
- [x] first_run_setup.py
- [ ] Windows .bat / Linux .sh scripts for run/health-check
