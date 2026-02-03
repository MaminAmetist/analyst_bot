import os
import requests
from dotenv import load_dotenv

load_dotenv()

AI_API_KEY = os.getenv('AI_API_KEY')
HF_TOKEN = os.getenv('HF_TOKEN')
MODEL_NAME = os.getenv('MODEL_NAME')


def get_ai_response(user_message):
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "TelegramBot"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter error {response.status_code}: {response.text}")

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"Unexpected response format: {data}")
