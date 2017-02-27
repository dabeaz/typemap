Typemap - The Annotator (TM)
============================

Typemap is a module that allows you to apply Python type annotations
by name, using simple "type quantifier" operators.  Here's a simple
example::

    # sample1.py
    import typemap

    V̵x: int
    V̵y: int

    def add(x, y):
        return x + y

    def sub(x, y):
        return x - y 

    typemap()

In this case, the "for all" type quantifier attaches the given type
annotation to all occurrences of a given name.  You can see this
if you import your module and look at the annotations::

    >>> import sample1
    >>> sample1.add.__annotations__
    {'x': <class 'int'>, 'y': <class 'int'>}
    >>> sample1.sub.__annotations__
    {'x': <class 'int'>, 'y': <class 'int'>}
    >>> 

Sweet!  You can also apply typemaps to name prefixes using
the "there exists" type quantifier.  If there exists a
given prefix, then it gets a type annotation.  For example::

    # sample2.py
    import typemap

    Ǝi: int

    def add(ix, iy):
        return ix + iy

    def sub(ix, iy):
        return ix - iy

    typemap()

It's one less line of typing (sic) and it still works::

    >>> import sample2
    >>> sample2.add.__annotations__
    {'ix': <class 'int'>, 'iy': <class 'int'>}
    >>>

Naturally, you can also use typemaps in class definitions::

    # sample3.py
    import typemap

    class Spam:
        V̵x: int
        V̵y: int
        def __init__(self, x,  y):
            self.x = x
            self.y = y

        def yow(self, x):
            pass

    typemap()

Typemaps are inherited.  Thus, this class gets the same typemaps as
the parent class::

    class Child(Spam):
        def bar(self, x, y):
            pass

    typemap()

Look at some of the annotations::

    >>> import sample3
    >>> sample3.Spam.__init__.__annotations__
    {'x': <class 'int'>, 'y': <class 'int'>}
    >>> sample3.Child.bar.__annotations__
    {'x': <class 'int'>, 'y': <class 'int'>}
    >>>

See the file ``sample.py`` for more examples.

FAQ
---

*How do you type V̵ and Ǝ?*

The V̵ character is the sequence ``'V\u0335'``. The Ǝ character is ``'\u018e'``.
The easiest way to get these is probably to cut and paste them out
of a document that shows them displayed correctly.   If you absolutely must, you
can use ``all_`` and ``prefix_`` as substitutes.  However, keep in mind that
good type annotations should be hard to type. 

*Why do you have to call typemap() at the bottom?*

Reasons.  Think of it as a kind of module decorator. 

*Are there any unit tests?*

No, not tests, types.

*Is there any more documentation?*

No, not documentation, types.

*WHY?*

Is it not obvious?

*Who?*

Typemap - The Annotator (TM) is the brainchild of David Beazley (@dabeaz) 
who disavows all knowledge of it and who should probably be working on
his book instead.
