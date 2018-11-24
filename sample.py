# sample.py
# -*- coding: utf-8 -*-
#
# An example of Typemap - The Annotator (TM).

# Define some typemaps
ᗄx: int
ᗄy: int

# Now, define some functions.  You'll see the arguments annotated.
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

# Typemaps can be applied in a class.  In this case, they get
# applied to members of the class.  Classes also see the outer
# typemaps although local redefinitions will override.

class Spam:
    ᗄz: int

    def __init__(self, x, y, z):      
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def foo(x, y):
        pass

    @classmethod
    def bar(cls, z):
        pass

# Inheritance propagates any previously defined typemaps
class Child(Spam):

    def yow(self, z):
        pass

# You can write typemaps for a common prefix too
Ǝf_: float

def mul(f_x, f_y):
    return f_x * f_y

def div(f_x, f_y):
    return f_x / f_y

# Naturally, anything from the typing module will work
from typing import Iterable

ᗄintegers: Iterable[int]

# And typemaps can apply to function names to set return types
Ǝint_: int

def int_sum(integers):    # (integers: Iterable[int]) -> int
    pass

def int_max(integers):
    pass

def int_min(integers):
    pass

# Typemaps should work with decorated functions as long as you
# use @wraps
from functools import wraps

def decorate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorate
def mul(x, y):
    return x + y

# Apply the typemaps
import typemap; typemap()

# You're done. A nicely defined Python module with type annotations.
# Enjoy!

# Look at the resulting definitions, see their type annotations
from inspect import signature

print(add, signature(add))
print(sub, signature(sub))
print(Spam.__init__,  signature(Spam))
print(Spam.foo, signature(Spam.foo))
print(Spam.bar, signature(Spam.bar))
print(Child.yow, signature(Child.yow))
print(mul, signature(mul))
print(div, signature(div))
print(int_sum, signature(int_sum))
print(int_max, signature(int_max))
print(int_min, signature(int_min))
print(mul, signature(mul))








