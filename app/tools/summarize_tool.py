class SummarizeTool:
    name = "summarize_articles"
    description = "Summarize a list of bitcoin news articles"

    def __init__(self, llm):
        self.llm = llm

    def run(self, input_data):
        articles = input_data["articles"]
        content = "\n\n".join([f"- {title}" for title in articles])

        prompt = f"""
You are a financial news analyst specializing in cryptocurrency.

Task:
Summarize the key insights from the following Bitcoin-related news articles.

Instructions:
- Focus on the most important facts, trends, and market implications.
- Remove redundancy and ignore minor details.
- Maintain factual accuracy and neutrality.
- If multiple articles overlap, consolidate the information.
- Highlight any significant market impact, regulatory changes, or technological developments.

Output format:
- A concise paragraph (5–8 sentences).
- Clear, coherent, and professional tone.
- No bullet points, no extra commentary, no repetition.

Articles:
{content}

Return summary only.
"""
        return {"summary": self.llm.generate(prompt)}