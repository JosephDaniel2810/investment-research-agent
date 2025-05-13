import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from agents.tool import function_tool

@function_tool
def plot_sma(ticker: str, period: str, window: int) -> None:
    """
    Plot the simple moving average (SMA) over the specified window.

    Args:
        ticker: Stock symbol (e.g. "AAPL").
        period: Data range (e.g. "3mo", "6mo", "1y").
        window: Window size for SMA (e.g. 20).
    """
    data = yf.Ticker(ticker).history(period=period)
    if data.empty:
        print(f"No data for {ticker} in period '{period}'")
        return
    sma = data['Close'].rolling(window=window).mean()
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data['Close'], label='Close')
    plt.plot(data.index, sma, label=f'SMA {window}')
    plt.title(f"{ticker} Close and SMA({window}) — Last {period}")
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=False)


@function_tool
def plot_ema(ticker: str, period: str, span: int) -> None:
    """
    Plot the exponential moving average (EMA) over the specified span.

    Args:
        ticker: Stock symbol
        period: Data range
        span: Span for EMA (e.g. 20)
    """
    data = yf.Ticker(ticker).history(period=period)
    if data.empty:
        print(f"No data for {ticker} in period '{period}'")
        return
    ema = data['Close'].ewm(span=span, adjust=False).mean()
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data['Close'], label='Close')
    plt.plot(data.index, ema, label=f'EMA {span}')
    plt.title(f"{ticker} Close and EMA({span}) — Last {period}")
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=False)

@function_tool
def plot_rsi(ticker: str, period: str, window: int) -> None:
    """
    Plot the Relative Strength Index (RSI).

    Args:
        ticker: Stock symbol
        period: Data range
        window: Window size for RSI calculation (e.g. 14)
    """
    data = yf.Ticker(ticker).history(period=period)
    if data.empty:
        print(f"No data for {ticker} in period '{period}'")
        return
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    plt.figure(figsize=(10,3))
    plt.plot(data.index, rsi, label='RSI')
    plt.axhline(70, color='red', linestyle='--')
    plt.axhline(30, color='green', linestyle='--')
    plt.title(f"{ticker} RSI({window}) — Last {period}")
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=False)

@function_tool
def plot_macd(ticker: str, period: str, fast_span: int, slow_span: int, signal_span: int) -> None:
    """
    Plot the MACD indicator with signal line.

    Args:
        ticker: Stock symbol
        period: Data range
        fast_span: Fast EMA span (e.g. 12)
        slow_span: Slow EMA span (e.g. 26)
        signal_span: Signal line EMA span (e.g. 9)
    """
    data = yf.Ticker(ticker).history(period=period)
    if data.empty:
        print(f"No data for {ticker} in period '{period}'")
        return
    fast_ema = data['Close'].ewm(span=fast_span, adjust=False).mean()
    slow_ema = data['Close'].ewm(span=slow_span, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal = macd.ewm(span=signal_span, adjust=False).mean()
    plt.figure(figsize=(10,5))
    plt.plot(data.index, macd, label='MACD')
    plt.plot(data.index, signal, label='Signal')
    plt.title(f"{ticker} MACD({fast_span},{slow_span}) & Signal({signal_span}) — Last {period}")
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=False)