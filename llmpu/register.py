import json
from collections import UserDict
from .config import config

registers = {} # index -> content

class RegisterDict(UserDict):
    def __init__(self, bind={}):
        super().__init__()
        self.data = bind
    def __setitem__(self, key, value):
        str_val = str(value)[:config["L"]]
        if not str_val: self.data.pop(int(key), None)
        else: self.data[int(key)] = str_val
    def __getitem__(self, key):
        return self.data.get(int(key), "")

reg = RegisterDict(registers)

def dump(path="dump.json"):
    json.dump({ "registers": registers }, open(path, "w"))

def load(path="dump.json"):
    global registers
    raw = json.load(open(path, "r"))
    registers = { int(k): v for k, v in raw.get("registers", {}).items() }
