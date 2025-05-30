import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from agents.tool import function_tool

def _plot_sma(ticker: str, period: str, window: int):
    data = yf.Ticker(ticker).history(period=period)
    if data.empty:
        print(f"No data for {ticker} in period '{period}'")
        return None
    sma = data['Close'].rolling(window=window).mean()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(data.index, data['Close'], label='Close')
    ax.plot(data.index, sma, label=f'SMA {window}')
    ax.set_title(f"{ticker} Close and SMA({window}) — Last {period}")
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

@function_tool
def plot_sma(ticker: str, period: str, window: int):
    return _plot_sma(ticker, period, window)

def _plot_ema(ticker: str, period: str, span: int):
    data = yf.Ticker(ticker).history(period=period)
    if data.empty:
        print(f"No data for {ticker} in period '{period}'")
        return None
    ema = data['Close'].ewm(span=span, adjust=False).mean()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(data.index, data['Close'], label='Close')
    ax.plot(data.index, ema, label=f'EMA {span}')
    ax.set_title(f"{ticker} Close and EMA({span}) — Last {period}")
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

@function_tool
def plot_ema(ticker: str, period: str, span: int):
    return _plot_ema(ticker, period, span)

def _plot_rsi(ticker: str, period: str, window: int):
    data = yf.Ticker(ticker).history(period=period)
    if data.empty:
        print(f"No data for {ticker} in period '{period}'")
        return None
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    fig, ax = plt.subplots(figsize=(10,3))
    ax.plot(data.index, rsi, label='RSI')
    ax.axhline(70, color='red', linestyle='--')
    ax.axhline(30, color='green', linestyle='--')
    ax.set_title(f"{ticker} RSI({window}) — Last {period}")
    ax.set_xlabel('Date')
    ax.set_ylabel('RSI')
    ax.grid(True)
    fig.tight_layout()
    return fig

@function_tool
def plot_rsi(ticker: str, period: str, window: int):
    return _plot_rsi(ticker, period, window)

def _plot_macd(ticker: str, period: str, fast_span: int, slow_span: int, signal_span: int):
    data = yf.Ticker(ticker).history(period=period)
    if data.empty:
        print(f"No data for {ticker} in period '{period}'")
        return None
    fast_ema = data['Close'].ewm(span=fast_span, adjust=False).mean()
    slow_ema = data['Close'].ewm(span=slow_span, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal = macd.ewm(span=signal_span, adjust=False).mean()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(data.index, macd, label='MACD')
    ax.plot(data.index, signal, label='Signal')
    ax.set_title(f"{ticker} MACD({fast_span},{slow_span}) & Signal({signal_span}) — Last {period}")
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

@function_tool
def plot_macd(ticker: str, period: str, fast_span: int, slow_span: int, signal_span: int):
    return _plot_macd(ticker, period, fast_span, slow_span, signal_span)