import pandas as pd
import numpy as np

class Backtester:
    """
    Generic backtester for long/short/flat strategies.

    Requirements of the input DataFrame:
    - Must contain 'Datetime', 'Close', and 'position' columns
    - position ∈ { -1, 0, +1 } and is already shifted (no lookahead)
    """

    def __init__(self, df, initial_capital=100_000):
        self.df = df.copy().sort_values("Datetime")
        self.initial_capital = initial_capital

    def run(self):
        df = self.df

        # 1. Compute returns
        df["returns"] = df["Close"].pct_change()

        # 2. Strategy returns (returns * position)
        df["strategy_returns"] = df["returns"] * df["position"]

        # 3. Cumulative equity curve
        df["equity"] = (1 + df["strategy_returns"]).cumprod() * self.initial_capital

        # 4. Buy & hold benchmark
        df["buy_hold"] = (1 + df["returns"]).cumprod() * self.initial_capital

        # 5. Compute Sharpe Ratio
        sharpe = self._compute_sharpe(df["strategy_returns"])

        # 6. Compute Max Drawdown
        max_dd = self._compute_max_drawdown(df["equity"])

        # 7. Compute trade metrics
        trade_stats = self._compute_trade_stats(df)

        results = {
            "final_equity": df["equity"].iloc[-1],
            "buy_hold_final": df["buy_hold"].iloc[-1],
            "sharpe_ratio": sharpe,
            "max_drawdown": max_dd,
            "trade_stats": trade_stats,
            "df": df
        }

        return results

    # ==========================================================
    # Metrics
    # ==========================================================

    def _compute_sharpe(self, returns, periods_per_year=252*6.5):  
        """
        Hourly data → approx 6.5 hours per day × 252 days.
        Sharpe = mean / std * sqrt(periods)
        """
        if returns.std() == 0:
            return 0
        return (returns.mean() / returns.std()) * np.sqrt(periods_per_year)

    def _compute_max_drawdown(self, equity_curve):
        rolling_max = equity_curve.cummax()
        dd = (equity_curve - rolling_max) / rolling_max
        return dd.min()

    def _compute_trade_stats(self, df):
        """
        Counts trades, wins, losses, win rate.
        A trade begins when position changes.
        """
        df["pos_change"] = df["position"].diff().fillna(0)
        trade_entries = df[df["pos_change"] != 0]

        num_trades = len(trade_entries)

        # Measure PnL between position changes
        df["pnl"] = df["strategy_returns"] * self.initial_capital
        trade_pnls = []

        current_pnl = 0
        prev_pos = df["position"].iloc[0]

        for _, row in df.iterrows():
            if row["position"] == prev_pos:
                current_pnl += row["pnl"]
            else:
                trade_pnls.append(current_pnl)
                current_pnl = 0
            prev_pos = row["position"]

        if current_pnl != 0:
            trade_pnls.append(current_pnl)

        trade_pnls = np.array(trade_pnls)

        wins = (trade_pnls > 0).sum()
        losses = (trade_pnls < 0).sum()

        win_rate = wins / max(1, (wins + losses))

        return {
            "num_trades": num_trades,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "avg_pnl": trade_pnls.mean() if len(trade_pnls) > 0 else 0
        }

