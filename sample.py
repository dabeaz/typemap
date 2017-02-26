# sample.py
#
# An example of Typemap - The Annotator (TM).

# Define some typemaps
V̵x: int
V̵y: int

# Now, define some functions.  You'll see the arguments annotated.
def add(x, y):       # (x: int, y: int)
    return x + y

def sub(x, y):       # (x: int, y: int)
    return x - y

# Typemaps can be applied in a class.  In this case, they get
# applied to members of the class.  Classes also see the outer
# typemaps although local redefinitions will override.

class Spam:
    V̵z: int

    # Annotated as: (x:int, y:int, z:int)
    def __init__(self, x, y, z):      
        self.x = x
        self.y = y
        self.z = z

    # static and class methods work
    @staticmethod
    def foo(x, y):        # (x:int, y:int)
        pass

    @classmethod
    def bar(cls, z):       # (cls, z:int)
        pass

# Inheritance propagates any previously defined typemaps
class Child(Spam):

    def yow(self, z):     # (self, z: int)
        pass

# You can write typemaps for a common prefix too
Ǝf_: float

def mul(f_x, f_y):         # (f_x: float, f_y: float)
    return f_x * f_y

def div(f_x, f_y):         # (f_x: float, f_y: float)
    return f_x / f_y

# Naturally, anything from the typing module will work
from typing import Iterable

V̵integers: Iterable[int]

# And typemaps can apply to function names to set return types
Ǝint_: int

def int_sum(integers):    # (integers: Iterable[int]) -> int
    pass

def int_max(integers):    # (integers: Iterable[int]) -> int
    pass

def int_min(integers):    # (integers: Iterable[int]) -> int
    pass

# Don't forget this part.  It has to go at the end.
from typemap import *

# You're done. A nicely defined Python module with type annotations.
# Enjoy!








