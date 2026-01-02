import requests

class LLMAdapter:
    def __init__(self, model="mistral"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    def chat(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        response = requests.post(self.url, json=payload)
        response.raise_for_status()

        return response.json()["message"]["content"]