from .register import read, write
from .config import config

def call(r):
    content = read(r)
    run(content)

def run(code):
    env = { "read": read, "write": write, "call": call }
    exec(code, env, env)
