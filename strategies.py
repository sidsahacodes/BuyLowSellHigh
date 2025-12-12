import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


# ================================================================
# Base Strategy Class
# ================================================================

class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    Defines a standard interface for generating signals and positions.
    """

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Implemented by each specific strategy.
        Must return df with a 'signal' column containing:
            +1 = long
            -1 = short
             0 = flat / hold
        """
        pass

    def finalize_positions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes signals, fills missing values, and ensures no lookahead bias.
        """

        # Ensure a signal column exists
        if "signal" not in df.columns:
            raise ValueError("Strategy did not produce a 'signal' column.")

        # Ensure each row has a trade signal (default = 0)
        df["signal"] = df["signal"].fillna(0).astype(float).clip(-1, 1)

        # Executed position = previous bar's signal
        df["position"] = df["signal"].shift(1).fillna(0)

        return df


# ================================================================
# Strategy 1: Buy Low, Sell High (Your Intended Strategy)
# ================================================================

class BuyLowSellHighStrategy(BaseStrategy):
    """
    Buy-Low-Sell-High strategy (mean reversion flavor).
    - Buy when price is below its moving average by a threshold.
    - Sell (short) when price is above its moving average by a threshold.
    - Hold otherwise.
    """

    def __init__(self, lookback=20, pct_threshold=0.003):
        """
        lookback: number of bars used to compute moving average
        pct_threshold: percent deviation from the moving average needed to trigger a trade
        """
        self.lookback = lookback
        self.pct_threshold = pct_threshold

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy().sort_values("Datetime")

        # Moving average
        df["ma"] = df["Close"].rolling(self.lookback).mean()

        # Percent deviation from moving average
        df["dev"] = (df["Close"] - df["ma"]) / df["ma"]

        df["signal"] = 0

        # Buy when price is sufficiently low
        df.loc[df["dev"] < -self.pct_threshold, "signal"] = 1

        # Short when price is sufficiently high
        df.loc[df["dev"] > self.pct_threshold, "signal"] = -1

        return self.finalize_positions(df)


# ================================================================
# Strategy 2: Classic Mean Reversion Strategy
# ================================================================

class MeanReversionStrategy(BaseStrategy):
    """
    Z-score based mean reversion strategy.
    - Long when price is far below mean (oversold)
    - Short when far above mean (overbought)
    """

    def __init__(self, lookback=20, threshold=1.5):
        self.lookback = lookback
        self.threshold = threshold

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy().sort_values("Datetime")

        df["ma"] = df["Close"].rolling(self.lookback).mean()
        df["std"] = df["Close"].rolling(self.lookback).std()

        df["z"] = (df["Close"] - df["ma"]) / df["std"]

        df["signal"] = 0
        df.loc[df["z"] > self.threshold, "signal"] = -1   # overbought → short
        df.loc[df["z"] < -self.threshold, "signal"] = 1   # oversold → long

        return self.finalize_positions(df)


# ================================================================
# Strategy 3: Breakout Strategy
# ================================================================

class BreakoutStrategy(BaseStrategy):
    """
    Breakout Strategy:
    - Long when price breaks above recent resistance.
    - Short when price breaks below recent support.
    - Hold otherwise.
    """

    def __init__(self, lookback=24):
        self.lookback = lookback

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy().sort_values("Datetime")

        df["high_roll"] = df["High"].rolling(self.lookback).max()
        df["low_roll"]  = df["Low"].rolling(self.lookback).min()

        df["signal"] = 0
        df.loc[df["Close"] > df["high_roll"].shift(1), "signal"] = 1
        df.loc[df["Close"] < df["low_roll"].shift(1), "signal"] = -1

        return self.finalize_positions(df)


# ================================================================
# Strategy 4: Custom Strategy (User-Defined Logic)
# ================================================================

class CustomStrategy(BaseStrategy):
    """
    A wrapper that allows the user to plug in any custom rule function.
    The custom function must output a df with a 'signal' column.
    """

    def __init__(self, rule_fn):
        """
        rule_fn: function(df) -> df with 'signal' column
        """
        self.rule_fn = rule_fn

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy().sort_values("Datetime")
        df = self.rule_fn(df)
        return self.finalize_positions(df)

