import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import timedelta
from agents.tool import function_tool

def _predict_price(ticker: str, period: str = "1mo"):
    # Map period to number of days
    period_map = {"1mo": 21, "6mo": 126, "1y": 252}  # trading days
    if period not in period_map:
        print("Invalid period. Choose from: 1mo, 6mo, 1y.")
        return None
    pred_days = period_map[period]
    # Fetch historical data (last 5 years)
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5y")
    if hist.empty:
        print(f"No data found for {ticker}")
        return None
    hist = hist.dropna(subset=["Close"]).copy()
    hist.reset_index(inplace=True)
    # Prepare data for regression
    hist["Day"] = np.arange(len(hist))
    X = hist[["Day"]].values
    y = hist["Close"].values
    # Train linear regression
    model = LinearRegression()
    model.fit(X, y)
    # Predict future days
    last_day = hist["Day"].iloc[-1]
    future_days = np.arange(last_day + 1, last_day + pred_days + 1)
    X_future = future_days.reshape(-1, 1)
    y_pred = model.predict(X_future)
    # Build future dates
    last_date = hist["Date"].iloc[-1]
    freq = pd.infer_freq(hist["Date"])
    if freq is None:
        freq = "B"  # fallback to business day
    future_dates = pd.bdate_range(start=last_date + timedelta(days=1), periods=pred_days)
    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(hist["Date"], hist["Close"], label="Historical Close")
    ax.plot(future_dates, y_pred, label=f"Predicted Close ({period})", linestyle="--")
    ax.set_title(f"{ticker} Price Prediction — Next {period}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

@function_tool
def predict_price(ticker: str, period: str = "1mo"):
    return _predict_price(ticker, period) 