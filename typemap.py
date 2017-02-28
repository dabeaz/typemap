# typemap.py
#
# Typemap - The Annotator (TM)
# 
# Author: David Beazley (http://www.dabeaz.com)
# Copyright (C) 2017

import inspect
import sys
from collections import ChainMap

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

class Typemap:
    def __call__(self, *mods):
        if mods:
            typemaps = ChainMap(*(_get_typemaps(mod) for mod in mods))
        else:
            typemaps = None
        module = sys.modules[sys._getframe(1).f_globals['__name__']]
        _apply_typemap(module, module.__name__, typemaps)


# Special codec to allow actual U+2200 and U+2203 characters in typemaps
import codecs

def encode(input, errors='strict'):
    return (input.encode('utf-8', errors), len(input))

def decode(input, errors='strict'):
    return (bytes(input).decode('utf-8', errors).replace('\u2200', 'V\u0335').replace('\u2203', '\u018e'), len(input))

def lookup(name):
    if name == 'typemap':
        return codecs.CodecInfo(
            name='typemap',
            encode=encode,
            decode=decode,
        )
    else:
        return None

codecs.register(lookup)

sys.modules[__name__] = Typemap()

        



