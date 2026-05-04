import requests
import logging

logging.basicConfig(level=logging.INFO)

OLLAMA_URL = "http://localhost:11434/api/generate"


class OllamaLLM:
    def __init__(self, model="hhao/qwen2.5-coder-tools:latest"):
        self.model = model

    def generate(self, prompt: str):
        logging.info(f"Calling LLM model: {self.model}")

        try:
            res = requests.post(
                OLLAMA_URL,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
            )

            logging.info(f"LLM status: {res.status_code}")

            res.raise_for_status()

            data = res.json()
            output = data.get("response", "")

            if not output:
                raise Exception("Empty response from LLM")

            return output.strip()

        except Exception as e:
            logging.error(f"LLM call failed: {e}")
            raise