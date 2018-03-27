# sample3.py
# -*- coding: typemap -*-
#
# An example of Typemap - The Annotator (TM).
# This file uses the mathematical quantifier symbols and a special source
# codecs.

import typemap

# Define some typemaps
∀x: int
∀y: int

# Now, define some functions.  You'll see the arguments annotated.
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

# Typemaps can be applied in a class.  In this case, they get
# applied to members of the class.  Classes also see the outer
# typemaps although local redefinitions will override.

class Spam:
    ∀z: int

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
∃f_: float

def mul(f_x, f_y):
    return f_x * f_y

def div(f_x, f_y):
    return f_x / f_y

# Naturally, anything from the typing module will work
from typing import Iterable

∀integers: Iterable[int]

# And typemaps can apply to function names to set return types
∃int_: int

def int_sum(integers):    # (integers: Iterable[int]) -> int
    pass

def int_max(integers):
    pass

def int_min(integers):
    pass

# Apply the typemaps
typemap()

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










