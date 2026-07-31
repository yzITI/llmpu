import inspect
from .register import read, write
from .config import config

def run(c):
    exec(read(c) if isinstance(c, int) else c, config["EXEC"], inspect.currentframe().f_back.f_locals)
