from .config import config
from .register import read, write
from .executor import run
from .llm import request

def init(_config={}):
    config.update(_config)

def read_registers(rs=range(config["VR"])):
    res = ""
    for r in rs:
        res += f"--- {r} ---\n\n"
        res += read(r) + "\n\n"
    return res

def cycle():
    code = request(read_registers())
    run(code)

