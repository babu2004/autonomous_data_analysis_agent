import os

from dotenv import load_dotenv
from openai import OpenAI

from .provider import LLMProvider

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("XAI_API_KEY"),
)


class GrokProvider(LLMProvider):
    def __init__(self, model="openai/gpt-oss-20b"):
        self.model = model

    def generate(self, messages, tools=None):
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "max_completion_tokens": 800,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        return client.chat.completions.create(**kwargs)