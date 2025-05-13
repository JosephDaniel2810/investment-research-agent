# tools/guardrails.py

import re
from agents import input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def validate_ticker(ctx, agent, ticker: str):
    """
    Ensures the ticker is 1–5 uppercase letters.
    """
    if not re.fullmatch(r"[A-Z]{1,5}", ticker.strip()):
        return GuardrailFunctionOutput(
            output_info=f"❗ Invalid ticker '{ticker}'. Must be 1–5 uppercase letters.",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(
        output_info=ticker.strip().upper(),
        tripwire_triggered=False
    )

@input_guardrail
async def validate_period(ctx, agent, period: str):
    """
    Ensures the period is one of 1mo, 3mo, 6mo, or 1y.
    """
    allowed = {"1mo", "3mo", "6mo", "1y"}
    p = period.strip()
    if p not in allowed:
        return GuardrailFunctionOutput(
            output_info=f"❗ Invalid period '{period}'. Choose from {', '.join(allowed)}.",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(output_info=p, tripwire_triggered=False)
