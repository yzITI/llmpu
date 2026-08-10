from .config import config
from .register import read, read_all, write, dump, load
from .runner import run, _run
from .llm import request
from .srpc import srpc

def init(_config={}):
    config.update(_config)

# complete default initialization by providing execution environment
init({ "EXEC": { "read": read, "write": write, "run": _run } })

def read_registers(rs=range(config["VR"])):
    return "".join(f"--- r{r} ---\n\n{read(r)}\n\n" for r in rs)

def cycle():
    return request(read_registers())

def serve(port=22222, browser=True):
    srpc(port=port)
    print(f"SRPC server is listening localhost:{port}. Dashboard UI: https://yzITI.github.io/llmpu/")
    srpc["read"] = read
    srpc["read_all"] = read_all
    srpc["write"] = write
    srpc["dump"] = dump
    srpc["load"] = load
    srpc["run"] = run
    srpc["cycle"] = cycle
    if browser:
        import webbrowser
        webbrowser.open("https://yzITI.github.io/llmpu/")
