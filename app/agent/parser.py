import json
import re

def parse_action(text):
    match = re.search(r'Action:\s*(\{.*\})', text, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group(1))
    except:
        return None