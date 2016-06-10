polypie
=======

Python polymorphic function declaration with obvious syntax. Just use
the same function name and mark each function definition with
``@polymorphic`` decorator.

Installation
~~~~~~~~~~~~

``pip install polypie``

Requirements
~~~~~~~~~~~~

-  Python 3.3+
-  `typecheck-decorator <https://github.com/prechelt/typecheck-decorator>`__

Example
~~~~~~~

.. code:: python

    from typing import Any, Sequence

    from polypie import polymorphic, PolypieException


    @polymorphic
    def example(a: int, b):
        print('(1)')


    @polymorphic
    def example(a: str, b: Any):
        print('(2)')


    @polymorphic
    def example(a: Sequence[str]):
        print('(3)')


    example(100, 200)   # (1)
    example('foo', 200)   # (2)
    example(['foo'])   # (3)
    example(('bar', 'baz'))   # (3)
    try:
        example(['foo', 100])
    except PolypieException as exc:
        print(exc)   # Matching signature <...> not found


    class Example:

        def __init__(self):
            self.values = {}

        @polymorphic
        def value(self, name):
            return self.values[name]

        @polymorphic
        def value(self, name, value):
            self.values[name] = value


    instance = Example()
    instance.value('foo', 100)
    instance.value('bar', 'baz')
    print(instance.value('foo'))   # 100
    print(instance.value('bar'))   # baz
