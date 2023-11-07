import sys
import types

def reload_module(module, verbose=False):
    if isinstance(module, types.ModuleType):
        module=module.__name__
    for mod in list(sys.modules.keys()):
        if module not in mod:
            continue
        mod=sys.modules.pop(mod)
        if mod and verbose:
            print('reload %s'%mod)

if __name__ == "__main__":
    reload_module("orbit")
    from orbit.ui import run_ui
    
    run_ui()