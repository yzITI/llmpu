import json
from .config import config

client = None
types = None

def gemini_request(prompt):
    global client, types
    if client is None:
        from google import genai
        client = genai.Client(api_key=config["api_key"])
        types = genai.types
    _config = {
        "thinking_config": types.ThinkingConfig(thinking_level="medium"),
        "response_mime_type": "application/json",
        "response_schema": types.Schema(type=types.Type.OBJECT, required=["instructions"], properties={ "instructions": types.Schema(type=types.Type.STRING, description="Python code") }),
        **config["llm_config"]
    }
    res = client.models.generate_content(model=config["model"], config=_config, contents=prompt)
    r = json.loads(res.text)
    return r["instructions"]

def request(prompt):
    if config["model"].startswith("gemini-"):
        return gemini_request(prompt)
    raise ValueError(f"Unsupported model: {config['model']}")
