from .config import config
from .register import read, read_all, write, dump, load
from .runner import run, _run
from .llm import request
from .srpc import srpc

def init(_config={}):
    config.update(_config)

# complete default initialization by providing execution environment
init({ "IS": { "read": read, "write": write, "run": _run } })

def stringify(rs=range(config["V"])):
    return "\n\n".join(f'<r{r}>\n{read(r)}\n</r{r}>' for r in rs)

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
