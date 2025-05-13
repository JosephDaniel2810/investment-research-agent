import yfinance as yf
from agents.tool import function_tool

@function_tool
def fetch_stock_data(ticker: str) -> str:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d")

    if hist.empty:
        return f"No data found for {ticker}"

    latest = hist.iloc[-1]
    return (
        f"Stock: {ticker}\n"
        f"Date: {latest.name.date()}\n"
        f"Open: {latest['Open']:.2f}\n"
        f"Close: {latest['Close']:.2f}\n"
        f"Volume: {latest['Volume']}\n"
    )