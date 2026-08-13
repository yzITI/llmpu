import inspect
from .register import read, write
from .config import config

def _run(_c):
    _var = inspect.currentframe().f_back.f_locals | config["EXEC"]
    exec(read(_c) if isinstance(_c, int) else _c, _var, _var) # share local & global to avoid nonlocal issue

def run(c): # isolate local variables
    _run(c)
