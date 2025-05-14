import yfinance as yf
from agents.tool import function_tool

@function_tool
def compute_metrics(ticker: str) -> str:
    """
    Compute key financial metrics for the given stock ticker:
    - P/E Ratio (trailing)
    - EPS (trailing twelve months)
    - Average daily trading volume
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    pe_ratio = info.get("trailingPE")
    eps = info.get("trailingEps")
    avg_volume = info.get("averageVolume")

    return (
        f"Metrics for {ticker}:\n"
        f"P/E Ratio: {pe_ratio if pe_ratio is not None else 'N/A'}\n"
        f"EPS (TTM): {eps if eps is not None else 'N/A'}\n"
        f"Average Volume: {avg_volume if avg_volume is not None else 'N/A'}"
    )