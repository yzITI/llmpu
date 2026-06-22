from .register import read, write
from .config import config

def call(r):
    run(read(r))

def run(code):
    exec(code, config["EXEC"], config["EXEC"])
