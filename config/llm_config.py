# config/llm_config.py

llm_config = {
    "temperature": 0.3,
    "seed": 42,
    "config_list": [
        {
            "model": "mistral",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
        }
    ],
}
