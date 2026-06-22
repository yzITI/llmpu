from .register import read, write
from .config import config

def call(r):
    run(read(r))

def run(code):
    env = { "read": read, "write": write, "call": call }
    exec(code, env, env)
