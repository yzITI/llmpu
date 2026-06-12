from .config import config

data = {}

def read(r):
    return data.get(r, "")

def write(r, content):
    _content = content[:config["L"]]
    data[r] = _content
    return _content
