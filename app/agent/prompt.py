def build_prompt(goal, tools, history, input_data):
    tool_desc = "\n".join([
        f"{t.name}: {t.description}" for t in tools
    ])

    return f"""
You are an AI Agent.

Goal:
{goal}

Input articles:
{format_articles(input_data["articles"])}

Available tools:
{tool_desc}

Rules:
- You MUST use tools
- You MUST NOT generate final answer directly
- You MUST follow the format EXACTLY
- Output ONLY valid JSON after 'Action:'
- "input" MUST be a JSON object (dictionary)
- NEVER return a list as input, if tool requires list, wrap it in a dict, e.g. {{"articles": [...]}}

When finished, return:
Action: {{"tool": "finish", "input": {{"summary": "...", "trend": "bullish|bearish|neutral"}}}}

Format:
Thought: <your reasoning>
Action: {{"tool": "<tool_name>", "input": {{...}}}}

History:
{history}
"""

def format_articles(articles):
    return "\n\n".join([
        f"- {a['title']}: {a['content'][:200]}"
        for a in articles
    ])