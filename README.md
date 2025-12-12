# Buy Low, Sell High — Intraday Mean Reversion Strategy

This project implements and evaluates an intraday **mean-reversion trading strategy** using hourly equity data.  
The strategy systematically identifies short-term price deviations from a moving average and generates **long, short, or hold signals** accordingly.

The analysis focuses on **parameter sensitivity**, robustness across assets, and comparison against a buy-and-hold benchmark.

---

## Strategy Overview

At each time step, the strategy computes the **percentage deviation** of price from a rolling moving average:

PercentageDeviation_t = (Close_t − MA_t) / MA_t

A trading signal is generated based on a threshold τ:

- **Long (+1)** if PercentageDeviation_t < −τ  
- **Short (−1)** if PercentageDeviation_t > τ  
- **Hold (0)** if −τ ≤ PercentageDeviation_t ≤ τ  

This framework allows the strategy to express **long, short, and neutral positions**.

---

## Backtesting Framework

The backtester simulates:
- Position changes based on generated signals  
- Hourly returns and cumulative equity  
- Buy-and-hold benchmark for comparison  

Performance metrics include:
- Final equity  
- Sharpe ratio  
- Maximum drawdown  
- Number of trades  

---

## Parameter Grid Search

The strategy is evaluated across a grid of parameters:

- **Lookback windows:** multiple short- and medium-term horizons  
- **Thresholds (τ):** varying sensitivity to price deviations  

Results are visualized using:
- Equity curve comparisons  
- Heatmaps of final equity, Sharpe ratio, and trade frequency  

---

## Assets Analyzed

The analysis is conducted independently for:
- AAPL  
- MSFT  
- AMZN  

This allows comparison of strategy behavior across assets with different volatility and intraday dynamics.

---

## Key Findings

- Optimal parameters are **asset-specific**  
- Small changes in lookback or τ can lead to large performance differences  
- No single parameter configuration is robust across all assets  
- Performance is best evaluated by identifying **stable regions**, not single optima  

These results highlight the importance of adaptive or volatility-scaled parameters in short-horizon strategies.

---

## Project Structure

BuyLowSellHigh/
├── strategies.py # Signal generation logic
├── backtester.py # Backtesting engine
├── notebooks/ # Analysis and visualization notebooks
├── data/ # Input data (not tracked)
└── README.md
