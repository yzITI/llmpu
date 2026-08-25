import inspect, ctypes
from .register import read, write
from .config import config

def _run(c): # share locals and inject globals
    cf = lambda: inspect.currentframe().f_back.f_back # never assign frame to variables to avoid memory leakage
    statically_known = set(cf().f_code.co_varnames) | set(cf().f_code.co_cellvars) | set(cf().f_code.co_freevars)
    merged = cf().f_locals | cf().f_globals
    exec(read(c) if isinstance(c, int) else c, merged, merged)
    for k, v in merged.items():
        if k in statically_known: # static local
            cf().f_locals[k] = v
            continue
        if k not in cf().f_globals or k in cf().f_locals: # dynamic
            cf().f_locals[k] = v
        cf().f_globals[k] = v # new
    for k in list(cf().f_locals.keys()):
        if k not in merged:
            del cf().f_locals[k]
    for k in list(cf().f_globals.keys()):
        if k not in merged:
            del cf().f_globals[k]

def run(c): # isolate scope
    merged = config["EXEC"] | {}
    exec(read(c) if isinstance(c, int) else c, merged, merged)
