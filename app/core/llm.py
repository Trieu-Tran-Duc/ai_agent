import requests
import logging

logging.basicConfig(level=logging.INFO)

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(prompt: str, model="hhao/qwen2.5-coder-tools:latest"):
    logging.info(f"Calling LLM model: {model}")

    try:
        res = requests.post(
            OLLAMA_URL, json={"model": model, "prompt": prompt, "stream": False}
        )

        logging.info(f"LLM response status: {res.status_code}")

        res.raise_for_status()

        data = res.json()
        output = data.get("response", "")

        logging.info(f"LLM response length: {len(output)} chars")

        return output

    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return ""
