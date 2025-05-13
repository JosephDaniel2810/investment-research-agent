import matplotlib.pyplot as plt
import yfinance as yf
from dotenv import load_dotenv
from agents import Agent, Runner
from tools.fetch_stock_data import fetch_stock_data
from tools.compute_metrics import compute_metrics
from tools.visualize import plot_price_history
from tools.technical_indicators import plot_sma, plot_ema, plot_rsi, plot_macd

# Load API key
load_dotenv()

# Prompt user for inputs
ticker = input("Enter a stock ticker (e.g. AAPL, TSLA): ").strip().upper()
action = input(
    "Choose an action: data, metrics, chart, sma, ema, rsi, macd, or all: "
).strip().lower()

# Build the natural-language query
if action == "data":
    query = f"Get me the latest stock data for {ticker}"
elif action == "metrics":
    query = f"Compute the financial metrics for {ticker}"
elif action == "chart":
    period = input("Enter chart period (e.g. 1mo, 3mo, 6mo, 1y): ").strip()
    query = f"Show me a closing price chart for {ticker} over the last {period}"
elif action == "sma":
    period = input("Enter period for SMA (e.g. 1mo, 3mo): ").strip()
    window = input("Enter SMA window (e.g. 20): ").strip()
    query = f"Plot the SMA({window}) for {ticker} over the last {period}"
elif action == "ema":
    period = input("Enter period for EMA (e.g. 1mo, 3mo): ").strip()
    span = input("Enter EMA span (e.g. 20): ").strip()
    query = f"Plot the EMA({span}) for {ticker} over the last {period}"
elif action == "rsi":
    period = input("Enter period for RSI (e.g. 1mo, 3mo): ").strip()
    window = input("Enter RSI window (e.g. 14): ").strip()
    query = f"Plot the RSI({window}) for {ticker} over the last {period}"
elif action == "macd":
    period = input("Enter period for MACD (e.g. 1mo, 3mo): ").strip()
    fast = input("Enter fast EMA span (e.g. 12): ").strip()
    slow = input("Enter slow EMA span (e.g. 26): ").strip()
    signal = input("Enter signal EMA span (e.g. 9): ").strip()
    query = (
        f"Plot the MACD({fast},{slow}) and signal({signal}) for {ticker} over the last {period}"
    )
elif action == "all":
    period = input("Enter chart period (e.g. 1mo, 3mo, 6mo, 1y): ").strip()
    query = (
        f"Get me the latest stock data and financial metrics for {ticker}, "
        f"and show me a closing price chart and plot SMA(20), EMA(20), RSI(14), MACD(12,26,9) over the last {period}"
    )
else:
    print("Invalid action. Exiting.")
    exit(1)

# Instantiate the FinanceBot agent with all tools
agent = Agent(
    name="FinanceBot",
    instructions=(
        "You are a financial research analyst. You have tools to: "
        "fetch raw data, compute metrics, visualize price history, and plot technical indicators."
    ),
    tools=[
        fetch_stock_data,
        compute_metrics,
        plot_price_history,
        plot_sma,
        plot_ema,
        plot_rsi,
        plot_macd,
    ],
)

# Run the agent and print text output
result = Runner.run_sync(agent, query)
print(result.final_output)

# Block here to show any and all matplotlib figures opened by tool calls
plt.show()