# typemap.py
#
# Typemap - The Annotator (TM)
# 
# Author: David Beazley (http://www.dabeaz.com)
# Copyright (C) 2017

import inspect
import sys
import importlib
from collections import ChainMap

_typemap = True
__all__ = [ '_typemap' ]

def _get_typemaps(module):
    if not hasattr(module, '__annotations__'):
        return { }
    typemaps = { }
    for key, val in module.__annotations__.items():
        if key[:2] == 'V\u0335':
            typemaps[key[2:]] = val
        elif key[:4] == 'all_':
            typemaps[key[4:]] = val
        elif key[:1] == '\u018e':
            typemaps[key[1:]+'*'] = val
        elif key[:7] == 'prefix_':
            typemaps[key[7:]+'*'] = val
    return typemaps

def _annotate(func, typemaps, prefixes):
    signature = inspect.signature(func)
    parms = list(signature.parameters)
    for name in parms:
        if name not in func.__annotations__:
            if name in typemaps:
                func.__annotations__[name] = typemaps[name]
            else:
                for key, value in prefixes:
                    if name.startswith(key):
                        func.__annotations__[name] = value

    if 'return' not in func.__annotations__:
        if func.__name__ in typemaps:
            func.__annotations__['return'] = typemaps[func.__name__]
        else:
            for key, value in prefixes:
                if func.__name__.startswith(key):
                    func.__annotations__['return'] = value

def _apply_typemap(module, modulename=None, typemaps=None):
    typemaps = ChainMap() if typemaps is None else typemaps.new_child()
    modulename = module.__module__ if modulename is None else modulename
    if not hasattr(module, '__annotations__'):
        module.__annotations__ = { }
        
    if hasattr(module, '__mro__'):
        for cls in reversed(module.__mro__):
            typemaps.update(_get_typemaps(cls))
        
    typemaps.update(_get_typemaps(module))

    prefixes = [ (key[:-1], val) for key, val in typemaps.items() if key[-1:] == '*' ]

    for key, val in vars(module).items():
        if callable(val):
            if getattr(val, '__module__', None) != modulename:
                continue
            if isinstance(val, type):
                _apply_typemap(val, modulename, typemaps)
            else:
                _annotate(val, typemaps, prefixes)
        elif isinstance(val, (staticmethod, classmethod)):
            _annotate(val.__func__, typemaps, prefixes)

class TypemapFinder:
    def __init__(self):
        self._skip = set()

    def find_module(self, fullname, path=None):
        if fullname in self._skip:
            return None
        self._skip.add(fullname)
        return TypemapLoader(self)

class TypemapLoader:
    def __init__(self, finder):
        self._finder = finder

    def load_module(self, fullname):
        try:
            importlib.import_module(fullname)
            module = sys.modules[fullname]
            if getattr(module, '_typemap', False):
                _apply_typemap(module, module.__name__)
            return module            
        finally:
            self._finder._skip.discard(fullname)

def _patch_importer():
    n = 2
    try:
        while True:
            f = sys._getframe(n)
            if f.f_globals.get('__annotations__'):
                module = sys.modules[f.f_globals['__name__']]
                typemaps = _get_typemaps(module)
                if typemaps:
                    _apply_typemap(module, module.__name__)
                    return
            n += 1
    except ValueError:
        pass

sys.meta_path.insert(0, TypemapFinder())
_patch_importer()

        



