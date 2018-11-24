# sample2.py
#
# An example of importing typemaps from a different module.
# tmaps.py contains the typemaps. Use typemap(tmaps) to incorporate
# them into the current file.

import tmaps

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def read_data(filename):
    pass

def maxvalue(data):
    pass

import typemap; typemap(tmaps)

# Look at the applied typemaps
from inspect import signature
print(add, signature(add))
print(sub, signature(sub))
print(read_data, signature(read_data))
print(maxvalue, signature(maxvalue))

