class TrendTool:
    name = "analyze_trend"
    description = "Detect bitcoin trend from summary of news articles"

    def __init__(self, llm):
        self.llm = llm

    def run(self, input_data):
        articles = input_data["summary"]

        MAX_LEN = 800

        content = "\n\n".join([
            f"{a.get('title','')}\n{a.get('content','')[:MAX_LEN]}".strip()
            for a in articles
            if a.get("content")
        ])
        
        prompt = f"""
You are a cryptocurrency market analyst.

Task:
Determine the overall Bitcoin market sentiment based on the news below.

Rules:
- Respond with EXACTLY one word: bullish, bearish, or neutral.
- Do NOT include any explanation, punctuation, or extra text.
- Base your decision on overall sentiment, not isolated events.

Definitions:
- bullish → positive outlook, price growth, strong demand, adoption, or optimistic signals
- bearish → negative outlook, price decline, fear, sell pressure, or adverse events
- neutral → mixed signals, unclear direction, or no strong consensus

Instructions:
- Weigh all information collectively.
- Ignore duplicates or minor details.
- If signals conflict, choose the dominant sentiment.

News:
{content}

Answer:
"""
        result = self.llm.generate(prompt)

        return {"trend": result.strip()}