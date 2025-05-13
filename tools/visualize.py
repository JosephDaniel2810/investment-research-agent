import yfinance as yf
import matplotlib.pyplot as plt
from agents.tool import function_tool

@function_tool
def plot_price_history(ticker: str, period: str) -> None:
    """
    Fetches historical closing prices for the given ticker and period,
    then displays a matplotlib line chart of the closing prices.

    Args:
        ticker: Stock symbol (e.g. "AAPL").
        period: Data range (e.g. "1mo", "3mo", "6mo", "1y").
    """
    # Use a default period if none provided
    if not period:
        period = "1mo"

    # Download historical data
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        print(f"No data found for {ticker} in period '{period}'")
        return

    # Plot closing prices
    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist['Close'], marker='o', linestyle='-')
    plt.title(f"{ticker} Closing Prices — Last {period}")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()