import json
from openai import AsyncOpenAI
from app.config import settings

SYSTEM_PROMPT = """You are a calibrated prediction market analyst.
Return strict JSON with keys:
probability (0..1), confidence (high|medium|low), reasoning (short), key_factors (array), risks_to_estimate (array)
"""


class OpenAIClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def estimate(self, question: str, yes_price: float) -> dict:
        if not self.client:
            p = min(0.95, max(0.05, yes_price + 0.02))
            return {
                "probability": round(p, 4),
                "confidence": "medium",
                "reasoning": f"No OPENAI_API_KEY; fallback estimate around market anchor for: {question[:80]}",
                "key_factors": ["market_anchor"],
                "risks_to_estimate": ["model_key_missing"],
            }

        user_prompt = f"Question: {question}\nCurrent YES price: {yes_price}\nEstimate real probability with calibration."
        try:
            resp = await self.client.chat.completions.create(
                model=settings.openai_model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=500,
            )
            data = json.loads(resp.choices[0].message.content)
            p = float(data.get("probability", yes_price))
            return {
                "probability": max(0.01, min(0.99, p)),
                "confidence": data.get("confidence", "medium"),
                "reasoning": data.get("reasoning", "model response"),
                "key_factors": data.get("key_factors", []),
                "risks_to_estimate": data.get("risks_to_estimate", []),
            }
        except Exception as e:
            p = min(0.95, max(0.05, yes_price + 0.015))
            return {
                "probability": round(p, 4),
                "confidence": "low",
                "reasoning": f"OpenAI call failed, fallback used: {str(e)[:120]}",
                "key_factors": ["fallback"],
                "risks_to_estimate": ["api_error"],
            }
