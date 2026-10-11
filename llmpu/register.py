import json
from .config import config

registers = {} # index -> content

def reg(r, content=None):
    if content is not None:
        if not content: registers.pop(int(r), None)
        else registers[int(r)] = str(content)[:config["L"]]
    return registers.get(int(r), "")

def all():
    return registers

def dump(path="dump.json"):
    json.dump({ "registers": registers }, open(path, "w"))

def load(path="dump.json"):
    global registers
    raw = json.load(open(path, "r"))
    registers = { int(k): v for k, v in raw.get("registers", {}).items() }
