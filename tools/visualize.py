import yfinance as yf
import matplotlib.pyplot as plt
from agents.tool import function_tool

def _plot_price_history(ticker: str, period: str):
    # default period
    if not period:
        period = "1mo"
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    if hist.empty:
        print(f"No data found for {ticker} in period '{period}'")
        return None
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hist.index, hist['Close'], marker='o', linestyle='-')
    ax.set_title(f"{ticker} Closing Prices — Last {period}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.grid(True)
    fig.tight_layout()
    return fig

@function_tool
def plot_price_history(ticker: str, period: str):
    return _plot_price_history(ticker, period)