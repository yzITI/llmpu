from .register import read, write
from .config import config

def call(r):
    content = read(r)
    run(content)

def run(code):
    env = { "READ": read, "WRITE": write, "CALL": call }
    exec(code, env, env)
