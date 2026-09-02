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
- `run(r)` execute the content in register number `r` as Python code

And their description is not hard coded, but stored in register 0, for example, as a "firmware".

## Get Started

```
pip install llmpu
```

```python
import llmpu

llmpu.init({
  "api_key": "",
  "model": "gemini-flash-latest"
})

# full config with default values:
llmpu.init({
    "api_key": "", # llm api key
    "V": 16, # visible register number
    "L": 16000, # hard character number limit for register
    "model": "gemini-flash-latest", # llm model
    "llm_config": {}, # llm config
    "IS": { # instruction set, can be used by llm
        "read": llmpu.read, "write": llmpu.write, "run": llmpu._run
    }
})
```

Instruction set functions:

```python
# use register 100 as an example
llmpu.write(100, "print('hello')") # truncate if exceed config["L"]
llmpu.read(100) # "print('hello')"
llmpu.run(100) # execute code in register 100
# llmpu.run also supports code string
```

> Note: `llmpu._run` shares the caller's locals and insert new variables to caller's globals, while `llmpu.run` is isolated.

Control functions:

```python
# main cycle: generate instructions
code = llmpu.cycle()
llmpu.run(code) # run the code

# core dump
llmpu.dump("dump.json") # dump registers to a json file
llmpu.load("dump.json") # load registers from a json file
```

Server and UI:

> Network server uses [srpc](https://github.com/yzITI/srpc) protocol. It only allows localhost traffic for security reason. **Exposing the interface allows arbitrary code execution!**

```python
llmpu.serve(port=22222, browser=True)
```
