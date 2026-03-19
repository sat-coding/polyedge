class OpenAIClient:
    async def estimate(self, question: str, yes_price: float) -> dict:
        p = min(0.95, max(0.05, yes_price + 0.03))
        return {"probability": round(p, 4), "confidence": "medium", "reasoning": f"Fallback estimator for: {question[:80]}"}
