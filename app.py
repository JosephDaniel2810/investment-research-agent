import streamlit as st
from tools.compute_metrics import _compute_metrics, compute_metrics
from tools.visualize import _plot_price_history, plot_price_history
from tools.technical_indicators import _plot_sma, _plot_ema, _plot_rsi, _plot_macd, plot_sma, plot_ema, plot_rsi, plot_macd
from tools.predict_price import _predict_price, predict_price
from agents import Agent, Runner
from tools.fetch_stock_data import _fetch_stock_data, fetch_stock_data
import matplotlib.pyplot as plt
import re
import yfinance as yf
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# OpenAI API setup
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    openai.api_key = openai_api_key

def get_ticker_from_openai(company_name):
    if not openai_api_key:
        return "Error: OpenAI API key not found. Please set it in your .env file."
    prompt = f"What is the stock ticker symbol for {company_name} (US market, if possible)? Only return the ticker symbol."
    try:
        client = openai.OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0
        )
        ticker = response.choices[0].message.content.strip().split()[0].upper()
        return ticker
    except Exception as e:
        return f"Error: {e}"

# --- THEME: Set dark mode and blue accent ---
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem;}
    .gradient-header {
        background: linear-gradient(90deg, #0f2027 0%, #2c5364 100%);
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 24px 0 rgba(0,0,0,0.2);
    }
    .gradient-header h1 {
        color: #00BFFF;
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 0.2em;
        letter-spacing: 2px;
    }
    .gradient-header p {
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    .section-title {
        color: #FF3333;
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }
    .st-emotion-cache-1v0mbdj p {color: #00BFFF;}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Lottie Animation Loader ---
def load_lottieurl(url: str):
    import requests
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

try:
    from streamlit_lottie import st_lottie
    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_2glqweqs.json"  # Up arrow
    lottie_json = load_lottieurl(lottie_url)
    st.markdown(
        """
        <div class='gradient-header'>
            <div style='display: flex; align-items: center;'>
                <div style='flex: 0 0 120px;'>
        """,
        unsafe_allow_html=True
    )
    st_lottie(lottie_json, speed=1, width=120, height=90, key="stock_arrow")
    st.markdown(
        """
                </div>
                <div style='flex: 1; padding-left: 1.5rem;'>
                    <h1>📈 Stock Market <span style='color:#FFD700;'>AI Bot</span></h1>
                    <p>AI-powered <span style='color:#00FFB0;'>research</span>, <span style='color:#FF69B4;'>metrics</span>, and <span style='color:#FFA500;'>predictions</span> for modern investors.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
except ImportError:
    st.warning("Install streamlit-lottie for animated graphics: pip install streamlit-lottie")
    st.markdown(
        """
        <div class='gradient-header'>
            <h1>📈 Stock Market <span style='color:#FFD700;'>AI Bot</span></h1>
            <p>AI-powered <span style='color:#00FFB0;'>research</span>, <span style='color:#FF69B4;'>metrics</span>, and <span style='color:#FFA500;'>predictions</span> for modern investors.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Sidebar Branding
st.sidebar.image("https://img.icons8.com/ios-filled/100/000000/artificial-intelligence.png", width=80)
st.sidebar.title("Stock Market AI Bot")
st.sidebar.markdown("AI-powered research, metrics, and predictions.")
st.sidebar.markdown("---")
st.sidebar.markdown("<span style='color:#00BFFF;'>Created By Joseph Daniel</span> | <span style='color:#FFD700;'>Powered by OpenAI & Streamlit</span>", unsafe_allow_html=True)

# --- Ticker Search by Company Name ---
search_icon_url = "https://img.icons8.com/ios-filled/50/000000/search--v1.png"  # small search icon
st.markdown("<div class='section-title'>Search Stock Ticker by Company Name</div>", unsafe_allow_html=True)
st.markdown(f"<img src='{search_icon_url}' width='20' style='vertical-align:middle;margin-right:8px;'/> <span style='font-size:1.1em;'>Enter a company name (e.g. Apple, Microsoft):</span>", unsafe_allow_html=True)
company_name = st.text_input("Company name", "", label_visibility="collapsed")
if st.button("Search Ticker (AI)") and company_name.strip():
    ticker = get_ticker_from_openai(company_name)
    if ticker.startswith("Error"):
        st.error(ticker)
    else:
        st.session_state["autofill_ticker"] = ticker
        st.success(f"Selected ticker: {ticker}. You can now use it below.")

def get_autofill_ticker():
    return st.session_state.get("autofill_ticker", "AAPL")

with st.form(key="input_form"):
    analyse_gif_url = "https://media.giphy.com/media/26ufnwz3wDUli7GU0/giphy.gif"  # analyze/target
    st.image(analyse_gif_url, width=60)
    st.markdown("<div class='section-title'>Analyze a Stock</div>", unsafe_allow_html=True)
    ticker = st.text_input("Enter a stock ticker (e.g. AAPL, TSLA):", value=get_autofill_ticker())
    action = st.selectbox("Choose an action:", [
        "data", "metrics", "chart", "sma", "ema", "rsi", "macd", "predict", "all"
    ])
    period = st.selectbox("Select period:", ["1mo", "3mo", "6mo", "1y"])
    submitted = st.form_submit_button("Analyze")

# Initialize dynamic metrics
price_val = "N/A"
pe_val = "N/A"
vol_val = "N/A"
price_delta = ""
pe_delta = ""
vol_delta = ""

# Main Dashboard
if submitted:
    error_flag = False
    data = None
    metrics = None
    # Fetch data and metrics for dynamic cards
    if action in ["data", "all", "metrics", "chart", "sma", "ema", "rsi", "macd", "predict"]:
        data = _fetch_stock_data(ticker)
        metrics = _compute_metrics(ticker)
        # Parse price and volume from data
        if data is None or "No data found" in str(data):
            st.error(f"No data found for ticker '{ticker}'. Please enter a valid stock symbol.")
            error_flag = True
        else:
            # Extract price and volume
            price_match = re.search(r"Close: ([\d.]+)", str(data))
            vol_match = re.search(r"Volume: ([\d,]+)", str(data))
            if price_match:
                price_val = f"${price_match.group(1)}"
            if vol_match:
                vol_val = vol_match.group(1)
        # Parse P/E from metrics
        if metrics is not None and "P/E Ratio:" in str(metrics):
            pe_match = re.search(r"P/E Ratio: ([\d.]+|N/A)", str(metrics))
            if pe_match:
                pe_val = pe_match.group(1)
    # Show error and skip further processing if error
    if error_flag:
        st.stop()
    # Action-specific outputs
    stock_gif_url = "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"  # stock market/graph
    st.image(stock_gif_url, width=60)
    st.markdown("<div class='section-title'>Results</div>", unsafe_allow_html=True)
    if action == "data":
        st.subheader(f"Latest Stock Data for {ticker}")
        st.write(data)
    elif action == "metrics":
        st.subheader(f"Key Metrics for {ticker}")
        st.write(metrics)
    elif action == "chart":
        st.subheader(f"{ticker} Price Chart")
        fig = _plot_price_history(ticker, period)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No chart data found for ticker '{ticker}'.")
    elif action == "sma":
        st.subheader(f"{ticker} SMA Chart")
        window = 20
        fig = _plot_sma(ticker, period, window)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No SMA data found for ticker '{ticker}'.")
    elif action == "ema":
        st.subheader(f"{ticker} EMA Chart")
        span = 20
        fig = _plot_ema(ticker, period, span)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No EMA data found for ticker '{ticker}'.")
    elif action == "rsi":
        st.subheader(f"{ticker} RSI Chart")
        window = 14
        fig = _plot_rsi(ticker, period, window)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No RSI data found for ticker '{ticker}'.")
    elif action == "macd":
        st.subheader(f"{ticker} MACD Chart")
        fast, slow, signal = 12, 26, 9
        fig = _plot_macd(ticker, period, fast, slow, signal)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No MACD data found for ticker '{ticker}'.")
    elif action == "predict":
        st.subheader(f"{ticker} Price Prediction")
        fig = _predict_price(ticker, period)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No prediction data found for ticker '{ticker}'.")
    elif action == "all":
        st.subheader(f"Comprehensive Analysis for {ticker}")
        st.write(data)
        st.write(metrics)
        fig = _plot_price_history(ticker, period)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No chart data found for ticker '{ticker}'.")
        fig = _plot_sma(ticker, period, 20)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No SMA data found for ticker '{ticker}'.")
        fig = _plot_ema(ticker, period, 20)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No EMA data found for ticker '{ticker}'.")
        fig = _plot_rsi(ticker, period, 14)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No RSI data found for ticker '{ticker}'.")
        fig = _plot_macd(ticker, period, 12, 26, 9)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No MACD data found for ticker '{ticker}'.")
        fig = _predict_price(ticker, period)
        if fig:
            st.pyplot(fig)
        else:
            st.error(f"No prediction data found for ticker '{ticker}'.")

# Dynamic Metrics Dashboard
st.markdown("<div class='section-title'>Quick Metrics</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("💰 Price", price_val, price_delta)
col2.metric("📊 P/E Ratio", pe_val, pe_delta)
col3.metric("🔄 Volume", vol_val, vol_delta)

# --- Metrics Explanation ---
with st.expander("ℹ️ What do these metrics mean?", expanded=False):
    st.markdown("""
    - **Price**: The most recent closing price of the stock.
    - **P/E Ratio**: Price-to-Earnings ratio. A measure of a company's current share price relative to its per-share earnings. Lower can mean undervalued, higher can mean overvalued (but context matters).
    - **Volume**: The number of shares traded during the most recent trading day. High volume can indicate strong interest.
    - **SMA (Simple Moving Average)**: The average closing price over a set period. Used to smooth out price trends.
    - **EMA (Exponential Moving Average)**: Like SMA, but gives more weight to recent prices.
    - **RSI (Relative Strength Index)**: A momentum indicator. Values above 70 may indicate overbought, below 30 oversold.
    - **MACD (Moving Average Convergence Divergence)**: Shows the relationship between two EMAs. Used to spot changes in trend.
    """)

# AI Chat Section
st.markdown("---")
st.markdown("<div class='section-title'>Ask the AI Bot</div>", unsafe_allow_html=True)
user_query = st.text_input("Type your question about a stock:")
if st.button("Ask AI"):
    # Use your agent to process the query
    agent = Agent(
        name="FinanceBot",
        instructions=(
            "You are a financial research analyst. You have tools to: "
            "fetch raw data, compute metrics, visualize price history, "
            "and plot technical indicators."
        ),
        tools=[
            fetch_stock_data,
            compute_metrics,
            plot_price_history,
            plot_sma,
            plot_ema,
            plot_rsi,
            plot_macd,
            predict_price,
        ],
    )
    import asyncio
    try:
        result = asyncio.run(Runner.run(agent, user_query))
        st.write(result.final_output)
    except Exception as e:
        st.error(f"Error: {e}") 