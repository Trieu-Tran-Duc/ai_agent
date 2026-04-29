def summary_prompt(text: str):
    return f"""
You are a professional news summarizer.

Summarize this text:

{text}

Return:
- Summary (3 sentences)
- Sentiment (positive|neutral|negative)
"""