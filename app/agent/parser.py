import json
import re
import ast

def parse_action(text):
    match = re.search(r'Action:\s*(\{.*?\})\s*$', text, re.DOTALL)
    if not match:
        return None

    raw = match.group(1)

    try:
        return json.loads(raw)
    except:
        pass

    try:
        fixed = raw.replace("'", '"')
        return json.loads(fixed)
    except:
        pass

    try:
        return ast.literal_eval(raw)
    except:
        pass

    print("❌ PARSE FAILED:\n", raw)
    return None