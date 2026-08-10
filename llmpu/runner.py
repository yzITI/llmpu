import inspect
from .register import read, write
from .config import config

def _run(c):
    exec(read(c) if isinstance(c, int) else c, config["EXEC"], inspect.currentframe().f_back.f_locals)

def run(c): # isolate local variables
    _run(c)
