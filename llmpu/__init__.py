from .config import config
from .register import read, write
from .executor import run
from .llm import request

clock = 0

def init(_config={}):
    config.update(_config)

def read_registers(rs=range(config["VR"])):
    res = ""
    for r in rs:
        res += f"--- {r} ---\n\n"
        res += read(r) + "\n\n"
    return res

def log(c):
    if not config["log_path"]:
        return
    with open(config["log_path"], "a") as f:
        f.write(f"--- clock: {clock} ---\n")
        f.write(c + "\n")

def cycle():
    code = request(read_registers())
    log(code)
    run(code)
    global clock
    clock += 1

