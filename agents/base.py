"""
Base utilities for GHOSTDEVS agents (Ollama version)
"""

from langchain_ollama import ChatOllama
from config.settings import settings


def get_llm(role: str = "worker"):
    """
    Return the appropriate LLM based on agent role.
    Using Ollama (local & free).
    """

    # You can change the model name here
    model_name = "qwen2.5-coder:7b"

    return ChatOllama(
        model=model_name,
        temperature=0.1,
        num_predict=4096,      # max tokens
    )