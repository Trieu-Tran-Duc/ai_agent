class SummarizeTool:
    name = "summarize_articles"
    description = "Summarize a list of bitcoin news articles"

    def __init__(self, llm):
        self.llm = llm

    def run(self, input_data):
        articles = input_data["articles"]

        content = "\n\n".join([
            f"{a['title']}\n{a['content']}"
            for a in articles
        ])

        prompt = f"""
Summarize the following bitcoin news:

{content}

Return summary only.
"""
        return {"summary": self.llm.generate(prompt)}