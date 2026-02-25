# SIMTRADE – Crypto Trading Strategies (Reconstructed Version)

This repository contains a reconstructed implementation of the trading strategies I developed for the **SIMTRADE (Tri-university Simulated Crypto Trading Contest, Aug–Sep 2024)**.

The original submission code and contest environment are no longer accessible due to the discontinuation and website failure of the SIMTRADE platform. As a result, this repository is based on my personal records and memory of the strategies, logic structure, and risk controls implemented during the competition.

## What’s included

- Volatility-adjusted momentum strategy (BTC)
- Z-score based mean-reversion strategy (BTC)
- Transaction cost modeling (simple fee factor)
- Stop-loss and take-profit risk controls
- Event-driven execution loop using an exchange-style API (via `NUSwapConnector`)

## Files

- `momentum_bitcoin.py` — momentum strategy implementation
- `mean_rev_bitcoin.py` — mean-reversion strategy implementation

## Notes / Disclaimer

This code is intended for educational and simulation purposes (as used in SIMTRADE).  
While the exact original codebase has been lost, this reconstruction reflects the strategic logic, parameter design, and risk management framework used during the contest.