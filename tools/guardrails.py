import re
from agents import input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def validate_query(ctx, agent, user_input: str):
    """
    Validates the full natural‑language query string before the agent runs.
    Enforces:
      • Ticker is 1–5 uppercase letters
      • Period (where required) is one of 1mo,3mo,6mo,1y
      • Query matches one of our action patterns exactly
    """
    patterns = [
        r"Get me the latest stock data for [A-Z]{1,5}",
        r"Compute the financial metrics for [A-Z]{1,5}",
        r"Show me a closing price chart for [A-Z]{1,5} over the last (?:1mo|3mo|6mo|1y)",
        r"Plot the SMA\(\d+\) for [A-Z]{1,5} over the last (?:1mo|3mo|6mo|1y)",
        r"Plot the EMA\(\d+\) for [A-Z]{1,5} over the last (?:1mo|3mo|6mo|1y)",
        r"Plot the RSI\(\d+\) for [A-Z]{1,5} over the last (?:1mo|3mo|6mo|1y)",
        r"Plot the MACD\(\d+,\d+\) and signal\(\d+\) for [A-Z]{1,5} over the last (?:1mo|3mo|6mo|1y)",
        r"Get me the latest stock data and financial metrics for [A-Z]{1,5}, and show me a closing price chart and plot SMA\(20\), EMA\(20\), RSI\(14\), MACD\(12,26,9\) over the last (?:1mo|3mo|6mo|1y)",
        r"Predict the closing price for [A-Z]{1,5} for the next (?:1mo|6mo|1y)",
    ]
    for pat in patterns:
        if re.fullmatch(pat, user_input):
            return GuardrailFunctionOutput(output_info=user_input, tripwire_triggered=False)

    # error message
    return GuardrailFunctionOutput(
        output_info=(
            "❗ Invalid command format.\n"
            " • Ticker must be 1–5 uppercase letters (e.g. AAPL).\n"
            " • If you're plotting, period must be one of: 1mo, 3mo, 6mo, 1y.\n"
            " • Examples:\n"
            "     Get me the latest stock data for TSLA\n"
            "     Show me a closing price chart for MSFT over the last 3mo"
        ),
        tripwire_triggered=True
    )
