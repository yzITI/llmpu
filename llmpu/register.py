import json, base64, hashlib
from .config import config

registers = {} # index -> hash
contents = {} # hash -> content

sha256 = lambda s: base64.b64encode(hashlib.sha256(s.encode('utf-8')).digest()).decode('utf-8')

def read(r):
    return contents.get(registers.get(r, ""), "")

def read_all():
    return { r: read(r) for r in registers }

def write(r, content):
    if not content:
        registers.pop(r, None)
        return content
    _content = content[:config["L"]]
    hash = sha256(_content)
    contents[hash] = _content
    registers[r] = hash
    return _content

def clean(): # clean unused contents
    for hash in list(contents.keys()):
        if hash not in registers.values():
            contents.pop(hash, None)

def dump(path="dump.json"):
    clean()
    json.dump({ "registers": registers, "contents": contents }, open(path, "w"))

def load(path="dump.json"):
    global registers, contents
    raw = json.load(open(path, "r"))
    registers = raw.get("registers", {})
    contents = raw.get("contents", {})
