def summary_prompt(text: str):
    return f"""
You are a crypto analyst.

Given multiple Bitcoin news articles:

1. Identify main topics
2. Detect overall trend
3. Summarize key insights

Return:

- Summary
- Key topics
- Trend (bullish / bearish / neutral)
"""
