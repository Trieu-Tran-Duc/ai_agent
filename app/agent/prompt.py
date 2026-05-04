def build_prompt(goal, tools, history, input_data):
    tool_desc = "\n".join([
        f"{t.name}: {t.description}" for t in tools
    ])

    return f"""
You are an AI Agent.

Goal: {goal}

Input:
{input_data}

Available tools:
{tool_desc}

Rules:
- Always use tools
- Do not hallucinate
- When done, return:
Action: {{"tool": "finish", "input": {{"summary": "...", "trend": "..."}}}}

Format:
Thought: ...
Action: {{"tool": "...", "input": {{...}}}}

History:
{history}
"""