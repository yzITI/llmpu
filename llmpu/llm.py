import json
from .config import config

gemini_client = None
gemini_types = None
openai_client = None
anthropic_client = None

def gemini_request(prompt):
    global gemini_client, gemini_types
    if gemini_client is None:
        from google import genai
        gemini_client = genai.Client(api_key=config["api_key"])
        gemini_types = genai.types
    _config = {
        "thinking_config": gemini_types.ThinkingConfig(thinking_level="high"),
        "response_mime_type": "application/json",
        "response_schema": gemini_types.Schema(
            type=gemini_types.Type.OBJECT,
            required=["instructions"],
            properties={ "instructions": gemini_types.Schema(type=gemini_types.Type.STRING, description="multi-line Python code") }
        ),
        **config.get("llm_config", {})
    }
    res = gemini_client.models.generate_content(model=config["model"], config=_config, contents=prompt)
    r = json.loads(res.text)
    return r["instructions"]

def openai_compatible_request(prompt, base_url=None):
    """Handles OpenAI, Grok, and DeepSeek via the OpenAI SDK."""
    global openai_client
    from openai import OpenAI
    api_key = config.get("api_key")
    client = OpenAI(api_key=api_key, base_url=base_url)
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "python_instructions",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": { "instructions": { "type": "string", "description": "multi-line Python code" } },
                "required": ["instructions"],
                "additionalProperties": False
            }
        }
    }
    extra_args = config.get("llm_config", {}).copy()
    res = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}],
        response_format=response_format,
        **extra_args
    )
    r = json.loads(res.choices[0].message.content)
    return r["instructions"]

def claude_request(prompt):
    global anthropic_client
    if anthropic_client is None:
        import anthropic
        anthropic_client = anthropic.Anthropic(api_key=config["api_key"])
    llm_config = config.get("llm_config", {})
    response = anthropic_client.messages.create(
        model=config["model"],
        max_tokens=llm_config.pop("max_tokens", 64000),
        messages=[{"role": "user", "content": prompt}],
        output_config={ "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": { "instructions": { "type": "string", "description": "multi-line Python code" } },
                "required": ["instructions"],
                "additionalProperties": False
            }
        } },
        **llm_config
    )
    text_content = next(block.text for block in response.content if block.type == "text")
    r = json.loads(text_content)
    return r["instructions"]

def request(prompt):
    model = config["model"].lower()
    if model.startswith("gemini-"):
        return gemini_request(prompt)
    if model.startswith("gpt-") or model.startswith("o1") or model.startswith("o3"):
        return openai_compatible_request(prompt)
    if model.startswith("claude-"):
        return claude_request(prompt)
    if model.startswith("grok-"):
        return openai_compatible_request(prompt, base_url="https://api.x.ai/v1")
    if model.startswith("deepseek-"):
        return openai_compatible_request(prompt, base_url="https://api.deepseek.com")
    raise ValueError(f"Unsupported model: {config['model']}")
