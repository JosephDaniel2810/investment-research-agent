# investment-research-agent

**AI‑Driven Investment Research Bot** built with the OpenAI Agents SDK and Python.

This project implements a command‑line “FinanceBot” that can:

* Fetch the latest stock price data (Open, Close, Volume) for any ticker
* Compute key financial metrics (P/E ratio, EPS, average volume)
* Plot historical price charts and technical indicators (SMA, EMA, RSI, MACD)

---

## 📂 Folder Structure

```
investment-research-agent/
├── main.py                  # Entry point: prompts user, builds and runs the agent
├── agent_config.py          # (Optional) separate module for Agent/Runner setup
├── tools/                   # Custom functions exposed as AI tools
│   ├── fetch_stock_data.py  # @function_tool: download and summarize latest price data
│   ├── compute_metrics.py   # @function_tool: compute P/E, EPS, average volume
│   ├── visualize.py         # @function_tool: plot closing price history
│   └── technical_indicators.py # @function_tool: plot SMA, EMA, RSI, MACD
├── requirements.txt         # Project dependencies
├── .gitignore               # Ignored files (including .env)
├── .env                     # Environment variables (OPENAI_API_KEY)
└── README.md                # This documentation
```

---

## 🚀 Quick Start

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

### 5. Run FinanceBot

```bash
python3 main.py
```

Follow the interactive prompts to:

* **Enter a ticker** (e.g. `AAPL`, `TSLA`)
* **Choose an action**:

  * `data`     → fetch raw price data
  * `metrics`  → compute P/E, EPS, volume
  * `chart`    → plot closing price history
  * `sma`, `ema`, `rsi`, `macd` → plot technical indicators
  * `all`      → run every tool in sequence and display charts together

---

## 🧠 How It Works

1. **Agent & Tools**

   * We use the **OpenAI Agents SDK** to create an `Agent` (FinanceBot) and register each Python function decorated with `@function_tool` as a callable tool.
2. **Natural‑Language Planning**

   * FinanceBot takes your plain English query (constructed in `main.py`) and decides which tool(s) to invoke and in what order.
3. **Tool Execution**

   * Each tool uses `yfinance` to fetch real market data or `matplotlib` to visualize it.
   * Results from multiple tools are aggregated and returned as coherent text and charts.
4. **Interactive CLI**

   * The script prompts the user to choose a ticker and action, then builds a single prompt for the agent.
   * A final `plt.show()` ensures all generated charts stay visible until closed.

---

## 🔧 Adding New Tools

1. Create a new Python file under `tools/`, define a function, and decorate with `@function_tool`.
2. Import and register the tool in `main.py` (and update the prompt logic).
3. The agent will automatically discover and use it based on natural‑language queries.

---

## 📝 License

MIT © 2025
