import sys
from .register import read

# this function is apparently very tricky
# blame Python for making this so difficult
# you might notice this is the only function that I would bother to write comments for each line. It's because I am wasting multiple hours on this little function.

def run(c): # share locals and inject globals
    cf = lambda: sys._getframe(2) # avoid assigning to variables to avoid circular reference and memory leakage
    # thanks to Python's FAST_LOCALS, we need to analyze which variables are already existing
    statically_known = set(cf().f_code.co_varnames + cf().f_code.co_cellvars + cf().f_code.co_freevars)
    scope = dict(cf().f_locals) # exec only accepts dict for globals
    # globals and locals must refer to the same object, because the "globals" inside exec is actually updated to the locals object, thanks to the trash module mechanism.
    exec(read(c) if isinstance(c, int) else c, scope, scope)
    scope.pop("__builtins__", None) # Python somehow shits in your object
    cf().f_locals.update({k: scope[k] for k in scope.keys() & statically_known}) # those present get updated
    cf().f_globals.update({k: scope[k] for k in scope.keys() - statically_known}) # those absent get ... WTF ... injected to globals?
    # Can you believe that, even with C APIs, you cannot add a local variable to a frame
    for k in set(cf().f_locals.keys()) - set(scope.keys()): # sync deletion
        del cf().f_locals[k]

# If you don't get the annoyance, let me remind you that in JavaScript such a mess can be implemented directly as `eval(code)`
