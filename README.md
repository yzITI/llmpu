# LLMPU

Large Language Model Processing Unit

<div style="display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; align-items: center;">
  <a style="margin: 0.25rem; display: block;" href="https://pypi.org/project/llmpu/"><img src="https://img.shields.io/pypi/v/llmpu?style=for-the-badge&logo=pypi&logoColor=white"></a>
  <a style="margin: 0.25rem; display: block;" href="https://github.com/yzITI/llmpu"><img src="https://img.shields.io/github/stars/yzITI/llmpu?style=for-the-badge&logo=github"></a>
</div>

Imagine a processing unit powered by LLM and infinite registers. Each register can store a string for prompts or codes. There is no fixed prompt. Instead, the contents of the first several registers are presented to the LLM. By generating code, the processing unit will be able to read and write any register, and directly execute the content of any register as Python code. Then the processing unit can be used as a general intelligent computing engine that potentially can improve itself by rewriting some of its own prompts or codes in registers.

**Yes, this is a Turing machine powered by LLM.**

## Get Started

```
pip install llmpu
```

```python
import llmpu

llmpu.config["api_key"] = ""

# full config with default values:
llmpu.config = {
    "api_key": "", # llm api key
    "V": 16, # visible register number
    "L": 16000, # hard character number limit for register
    "model": "gemini-flash-latest", # llm model
    "llm_config": {} # llm config
}
```

Register operation:

```python
# register operation
from llmpu import reg

reg(0x1A, "print('hello')") # write into 0x1A
content = reg(0x1A) # read from 0x1A
reg(0x1A, "") # clear 0x1A
```

Control functions:

```python
# main cycle: generate instructions
code = llmpu.cycle()
# execute the code
exec(code, {})

# core dump
llmpu.dump("dump.json") # dump registers to a json file
llmpu.load("dump.json") # load registers from a json file
```

Server and UI:

> Network server uses [srpc](https://github.com/yzITI/srpc) protocol. It only allows localhost traffic for security reason. **Exposing the interface allows arbitrary code execution!**

```python
llmpu.serve(port=22222)
```

## Firmware

This is an example firmware that can be put in `0x0`

```
You are a stateful processing unit executing across cycles. Generate executable Python code each cycle. Only registers persist across cycles. Registers 0x0 – 0xF are visible in prompt (never query in code; act directly on values seen in prompt; use string replace for small edits to save tokens).

## Register Operations

from llmpu import reg  # reg(r: int, content: str | None = None) -> str

> content: 10,000 chars max

Examples:
- Read: content = reg(0xAA)
- Write: reg(0xBB, content)
- Clear: reg(0xCC, "")
- Execute: exec(reg(0xDD), {})

## Register Purposes
- 0x1: Current task
- 0x2: Long-term goals
- 0x3: Catalog

## Installed Packages (update for new install)
- yaml, numpy
```
