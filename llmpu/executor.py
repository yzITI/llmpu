from .register import read, write
from .config import config

def call(r, globals=None, locals=None):
    run(read(r), globals, locals)

def run(code, globals=None, locals=None):
    exec(code, globals or config["EXEC"], locals or {})
