import inspect
from .register import read, write
from .config import config

def _run(_c): # share local & global to avoid nonlocal issue
    exec(read(_c) if isinstance(_c, int) else _c, inspect.currentframe().f_back.f_locals | config["EXEC"])

def run(c): # isolate local variables
    _run(c)
