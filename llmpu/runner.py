import inspect, ctypes
from .register import read, write
from .config import config

def _run(c):
    cf = inspect.currentframe().f_back
    try:
        old_locals = set(cf.f_locals.keys())
        exec(read(c) if isinstance(c, int) else c, cf.f_globals, cf.f_locals)
        cf.f_globals.update({k: v for k, v in cf.f_locals.items() if k not in old_locals})
    finally:
        del cf

def run(c): # isolate local variables
    exec(read(c) if isinstance(c, int) else c, config["EXEC"], {})
