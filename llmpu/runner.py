import inspect, ctypes
from .register import read, write
from .config import config

def _run(c): # share locals and inject globals
    cf = lambda: inspect.currentframe().f_back.f_back # never assign frame to variables to avoid memory leakage
    old_locals = set(cf().f_locals.keys())
    exec(read(c) if isinstance(c, int) else c, cf().f_globals, cf().f_locals)
    cf().f_globals.update({ k: v for k, v in cf().f_locals.items() if k not in old_locals })

def run(c): # isolate scope
    exec(read(c) if isinstance(c, int) else c, config["EXEC"], {})
