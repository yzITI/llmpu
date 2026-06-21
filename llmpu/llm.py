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
        "response_schema": types.Schema(type=types.Type.OBJECT, required=["python_code"], properties={ "python_code": types.Schema(type=types.Type.STRING) }),
        **config["llm_config"]
    }
    res = client.models.generate_content(model=config["model"], config=_config, contents=prompt)
    r = json.loads(res.text)
    return r["python_code"]

def request(prompt):
    return gemini_request(prompt)
