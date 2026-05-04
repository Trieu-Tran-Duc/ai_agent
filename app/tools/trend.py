class TrendTool:
    name = "analyze_trend"
    description = "Detect bitcoin trend from articles"

    def __init__(self, llm):
        self.llm = llm

    def run(self, input_data):
        articles = input_data["articles"]

        content = "\n".join([a["content"] for a in articles])

        prompt = f"""
Analyze the trend of bitcoin based on the following news.

Return one word: bullish, bearish, or neutral.

{content}
"""
        result = self.llm.generate(prompt)

        return {"trend": result.strip()}