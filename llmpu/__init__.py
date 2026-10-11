from .config import config
from .register import reg, registers, dump, load, all
from .llm import request
from .srpc import srpc

def stringify(rs=None):
    if rs is None: rs = range(config["V"])
    return "\n\n".join(f'<0x{r:X}>\n{reg[r]}\n</0x{r:X}>' for r in rs)

def cycle():
    return request(stringify())

def serve(port=22222):
    srpc(port=port)
    print(f"SRPC server is listening localhost:{port}. Cautious: it allows arbitrary code execution! Dashboard UI: https://yzITI.github.io/llmpu/")
    srpc["cycle"] = cycle
    srpc["dump"] = dump
    srpc["load"] = load
    srpc["write"] = lambda r, content: reg[r] = content
    srpc["read_all"] = lambda: registers
    srpc["exec"] = lambda c: exec(c, {})
