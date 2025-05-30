# investment-research-agent

**AI‑Driven Investment Research Bot** with a Modern, Animated Streamlit UI

This project implements a web-based “FinanceBot” that can:

* Fetch the latest stock price data (Open, Close, Volume) for any ticker
* Compute key financial metrics (P/E ratio, EPS, average volume)
* Plot historical price charts and technical indicators (SMA, EMA, RSI, MACD)
* Predict future prices using machine learning
* Search for stock tickers by company name using OpenAI (AI-powered)
* Enjoy a beautiful, dark-themed, animated dashboard with dynamic metrics and Lottie graphics

---

## 🚀 Features

- **Modern Streamlit UI**: Dark theme, gradient header, colorful section titles, and animated graphics (Lottie + GIFs)
- **AI-Powered Ticker Search**: Enter a company name and get the correct stock ticker using OpenAI GPT
- **Dynamic Metrics**: Price, P/E Ratio, and Volume update live for each stock
- **Animated Visuals**: Lottie animation in the header, GIFs/icons for sections
- **All-in-one Dashboard**: Data, metrics, charts, indicators, and predictions in one place
- **Conversational AI Chatbot**: Ask natural language questions about stocks

---

## 📸 Screenshots

![Modern UI Example](https://user-images.githubusercontent.com/your-screenshot-link.png)

---

## 📂 Folder Structure

```
investment-research-agent/
├── app.py                   # Main Streamlit app (modern UI)
├── agent_config.py          # (Optional) agent/runner setup
├── tools/                   # Custom functions exposed as AI tools
│   ├── fetch_stock_data.py  # Download and summarize latest price data
│   ├── compute_metrics.py   # Compute P/E, EPS, average volume
│   ├── visualize.py         # Plot closing price history
│   └── technical_indicators.py # Plot SMA, EMA, RSI, MACD
├── requirements.txt         # Project dependencies
├── .gitignore               # Ignored files (including .env)
├── .env                     # Environment variables (OPENAI_API_KEY)
└── README.md                # This documentation
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your‑username>/investment-research-agent.git
cd investment-research-agent
```

### 2. Create and activate a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .\.venv\Scripts\activate   # Windows PowerShell
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your OpenAI API key

1. Copy `.env.example` → `.env` (or just create `.env`).
2. Add your key:

   ```dotenv
   OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

### 5. Run the Modern Dashboard

```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. **Modern UI**
   - Dark theme, gradient header, animated Lottie graphics, and colorful section titles
   - GIFs/icons for search, analyze, and results sections
2. **AI Ticker Search**
   - Enter a company name, click the search icon, and get the correct ticker using OpenAI GPT
3. **Dynamic Metrics & Visuals**
   - Price, P/E, and Volume update for each stock
   - All charts and predictions are shown interactively
4. **Conversational AI**
   - Ask the AI bot questions about stocks, metrics, or indicators

---

## 🔧 Adding New Tools

1. Create a new Python file under `tools/`, define a function, and decorate with `@function_tool`.
2. Import and register the tool in `app.py` (and update the UI logic).
3. The agent will automatically discover and use it based on natural‑language queries.

---

## 📝 License

MIT © 2025
