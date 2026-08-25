import sys
from .register import read, write
from .config import config

# this function is apparently very tricky
# blame Python for making this so difficult

def _run(c): # share locals and inject globals
    cf = lambda: sys._getframe(2) # never assign frame to variables to avoid memory leakage
    statically_known = set(cf().f_code.co_varnames + cf().f_code.co_cellvars + cf().f_code.co_freevars)
    merged = cf().f_locals | cf().f_globals
    exec(read(c) if isinstance(c, int) else c, merged, merged)
    cf().f_locals.update({ k: merged[k] for k in (merged.keys() & statically_known) |
        (merged.keys() - cf().f_globals.keys()) |
        (merged.keys() & cf().f_locals.keys()) })
    cf().f_globals.update({ k: merged[k] for k in merged.keys() - statically_known })
    for k in cf().f_locals.keys() - merged.keys():
        del cf().f_locals[k]
    for k in cf().f_globals.keys() - merged.keys():
        del cf().f_globals[k]

def run(c): # isolate scope
    merged = config["EXEC"] | {}
    exec(read(c) if isinstance(c, int) else c, merged, merged)
