# LLMPU

Large Language Model Processing Unit

<div style="display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; align-items: center;">
  <a style="margin: 0.25rem; display: block;" href="https://pypi.org/project/llmpu/"><img src="https://img.shields.io/pypi/v/llmpu?style=for-the-badge&logo=pypi&logoColor=white"></a>
  <a style="margin: 0.25rem; display: block;" href="https://github.com/yzITI/llmpu"><img src="https://img.shields.io/github/stars/yzITI/llmpu?style=for-the-badge&logo=github"></a>
</div>

Imagine a processing unit powered by LLM and infinite registers. Each register can store a string for prompts or codes. There is no fixed prompt. Instead, the contents of the first several registers are presented to the LLM. By generating code, the processing unit will be able to read and write any register, and directly execute the content of any register as Python code. Then the processing unit can be used as a general intelligent computing engine that potentially can improve itself by rewriting some of its own prompts or codes in registers.

The following instruction set is provided to the processing unit as Python functions:
- `read(r)` returns content in register number `r`
- `write(r, content)` store string `content` in register number `r`
- `call(r)` execute the content in register number `r` as Python code

And their description is not hard coded, but stored in register 0, for example, as a "firmware".

## Get Started

```
pip install llmpu
```

```python
import llmpu
llmpu.init({
    # "VR": 16, # visibile register number
    # "L": 10000, # hard character number limit for register
    # "model": "gemini-3.5-flash", # llm model
    "api_key": "your llm api key", # llm api key
    # "llm_config": {}, # llm config
    # "log_path": "llmpu.log", # log path
})
```

Instruction set functions:

```python
# use register 100 as an example
llmpu.write(100, "print('hello')") # truncate if exceed config["L"]
llmpu.read(100) # "print('hello')"
llmpu.call(100) # execute code in register 100
```

Control functions:

```python
# main clock cycle
# present visible registers to LLM, then execute the generated code.
llmpu.cycle()

# core dump
llmpu.dump("dump.json") # dump state to a json file
llmpu.load("dump.json") # load state from a json file
```

## Minimum Example

```python
# using default config
firmware = """You are a self-improving processing unit with registers: max 5000 chars each, r0-r15 visible, more available but hidden.

API:
- read(r: int) -> str: read register r.
- write(r: int, content: str): write content in r (truncated to 5000 chars).
- call(r: int): Run register r's content as Python code.

common registers:
- r1: current task
"""
llmpu.write(0, firmware)
llmpu.write(1, "load r10001 to r1")
llmpu.write(10000, "do nothing")
llmpu.write(10001, "print hello to the screen, then call r10010")
llmpu.write(10010, "print('hello again')\nwrite(1, read(10000))")

llmpu.cycle() # r10001 will be loaded to r1
llmpu.cycle() # print "hello", then call r10010, which will print "hello again" and write r10000 to r1
llmpu.cycle() # pass
```

