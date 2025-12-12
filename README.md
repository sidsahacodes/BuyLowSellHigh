# Buy Low, Sell High — Intraday Mean Reversion Strategy

This project explores an intraday **mean-reversion trading strategy** using hourly equity data.  
The strategy is based on the intuition that prices tend to revert toward a recent average after short-term deviations.

The goal of the project is not to find a single optimal rule, but to understand **how strategy performance depends on parameter choices** and how those choices vary across assets.

---

## Strategy Intuition

At each point in time, the strategy compares the current price to a recent moving average:

- If the price is **significantly below** its recent average, the strategy enters a **long** position.
- If the price is **significantly above** its recent average, the strategy enters a **short** position.
- If the price is close to its average, the strategy **holds** no position.

This allows the strategy to take **long, short, or neutral** positions depending on market conditions.

---

## Backtesting Framework

A custom backtesting engine simulates:
- Signal generation at each hourly timestamp  
- Position changes and portfolio returns  
- A buy-and-hold benchmark for comparison  

Key performance metrics include:
- Final portfolio value  
- Sharpe ratio  
- Maximum drawdown  
- Number of trades  

---

## Parameter Sensitivity Analysis

The strategy is evaluated across a grid of:
- **Lookback windows** (how far back the moving average is computed)
- **Deviation thresholds** (how large a deviation must be to trigger a trade)

Results are visualized using:
- Equity curve comparisons
- Heatmaps showing how performance varies across parameters

---

## Assets Analyzed

The analysis is conducted independently for:
- AAPL
- MSFT
- AMZN

This highlights how the same strategy behaves differently across assets with distinct volatility and intraday dynamics.

---

## Key Findings

- Optimal parameters are **asset-specific**
- Small parameter changes can lead to large differences in performance
- Robust performance appears in **regions** of the parameter space rather than at a single optimal point

These results emphasize the importance of robustness and adaptation when designing short-horizon trading strategies.

