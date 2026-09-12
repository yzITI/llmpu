from .config import config as _config
from .register import read, read_all, write, dump, load
from .runner import run, _run
from .llm import request
from .srpc import srpc

def config(c):
    _config.update(c)
    return _config

# providing default instruction set
config({ "IS": { "read": read, "write": write, "run": _run } })

def stringify(rs=range(_config["V"])):
    return "\n\n".join(f'<0x{r:X}>\n{read(r)}\n</0x{r:X}>' for r in rs)

def cycle():
    return request(stringify())

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
