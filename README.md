# Buy Low, Sell High — Intraday Mean Reversion Strategy

This project implements and evaluates an intraday **mean-reversion trading strategy** using hourly equity data.  
The strategy identifies short-term price deviations from a moving average and generates **long, short, or hold** signals.

---

## Strategy Overview

At each timestamp, we compute the **percentage deviation** of the current price from its rolling moving average:

PercentageDeviation_t = (Close_t - MA_t) / MA_t

Where:
- Close_t = closing price at time t
- MA_t = rolling moving average of Close over the last `lookback` periods

---

## Trading Rules

Let `tau` (τ) be the deviation threshold.

1. **Long (+1)** if:  
   PercentageDeviation_t < -tau

2. **Short (-1)** if:  
   PercentageDeviation_t >  tau

3. **Hold (0)** if:  
   -tau <= PercentageDeviation_t <= tau

---

## Backtesting Framework

The backtester simulates:
- Position changes based on generated signals  
- Hourly returns and cumulative equity  
- A buy-and-hold benchmark for comparison  

Metrics reported:
- Final equity  
- Sharpe ratio  
- Maximum drawdown  
- Number of trades  

---

## Parameter Grid Search

We evaluate the strategy across a grid of:
- **Lookback windows** (short and medium horizons)
- **Thresholds (tau)** controlling sensitivity to deviations

Results are visualized using:
- Equity curve comparisons vs buy-and-hold
- Heatmaps of final equity, Sharpe ratio, and trade frequency

---

## Assets Analyzed

The analysis is run independently for:
- AAPL
- MSFT
- AMZN

---

## Key Findings

- Optimal parameters are **not consistent across different stocks**
- Small changes in lookback or tau can materially change outcomes
- Robust performance is best identified by **stable regions** in the heatmaps, not single “best” parameter points
