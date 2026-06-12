import json
from .config import config

client = None

def gemini_request(prompt):
    global client
    if client is None:
        from google import genai
        client = genai.Client(api_key=config["api_key"])
    res = client.models.generate_content(
        model=config["model"],
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="high"),
            response_mime_type="application/json",
            response_schema=types.Schema(type=types.Type.OBJECT, required=["code"], properties={ "code": types.Schema(type=types.Type.STRING) }),
            **config["llm_config"]
        ),
        contents=prompt
    )
    r = json.loads(res.text)
    return r["code"]

def request(prompt):
    return gemini_request(prompt)
