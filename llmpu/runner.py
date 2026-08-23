import inspect, ctypes
from .register import read, write
from .config import config

def _run(c): # share local & global to avoid nonlocal issue
    caller_frame = inspect.currentframe().f_back
    var = caller_frame.f_locals | config["EXEC"]
    exec(read(c) if isinstance(c, int) else c, var)
    caller_frame.f_locals.update({ k: v for k, v in var.items() if k not in config["EXEC"] })
    ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(caller_frame), ctypes.c_int(0))

def run(c): # isolate local variables
    exec(read(c) if isinstance(c, int) else c, config["EXEC"], {})
