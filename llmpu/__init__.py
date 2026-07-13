from .config import config
from .register import read, write, dump, load
from .executor import run, call
from .llm import request
from .srpc import srpc

clock = -1

def init(_config={}):
    config.update(_config)

# complete default initialization by providing execution environment
init({ "EXEC": { "read": read, "write": write, "call": call } })

def read_registers(rs=range(config["VR"])):
    res = ""
    for r in rs:
        res += f"--- {r} ---\n\n" + read(r) + "\n\n"
    return res

def log(c):
    if not config["log_path"]:
        return
    with open(config["log_path"], "a") as f:
        f.write(f"--- clock: {clock} ---\n{c}\n")

def cycle(debug=False):
    global clock
    clock += 1
    code = request(read_registers())
    log(code)
    if not debug:
        run(code)
    return code

def serve(port=22222, browser=True):
    srpc(port=port)
    print(f"SRPC server is listening localhost:{port}")
    srpc["read"] = read
    srpc["write"] = write
    srpc["dump"] = dump
    srpc["load"] = load
    srpc["call"] = call
    srpc["run"] = run
    srpc["cycle"] = cycle
    if browser:
        import webbrowser
        webbrowser.open("https://yzITI.github.io/llmpu/")
