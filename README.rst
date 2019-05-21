polypie
=======

|Build Status| |Coverage Status| |PyPI version| |PyPI license|

Python polymorphic function declaration with obvious syntax. Just use
the same function name and mark each function definition with
``@polymorphic`` decorator.

Installation
~~~~~~~~~~~~

``pip install polypie``

Requirements
~~~~~~~~~~~~

-  Python 3.5+
-  `typeguard <https://github.com/agronholm/typeguard>`__ (will be installed automatically)

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
        example({'foo': 'bar'})
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

Tests
~~~~~

``tox [-e ENV] [-- --cov]``

.. |Build Status| image:: https://travis-ci.org/un-def/polypie.svg?branch=master
   :target: https://travis-ci.org/un-def/polypie
.. |Coverage Status| image:: https://coveralls.io/repos/github/un-def/polypie/badge.svg?branch=master
   :target: https://coveralls.io/github/un-def/polypie?branch=master
.. |PyPI version| image:: https://badge.fury.io/py/polypie.svg
   :target: https://pypi.python.org/pypi/polypie/
.. |PyPI license| image:: https://img.shields.io/pypi/l/polypie.svg?maxAge=3600
   :target: https://raw.githubusercontent.com/un-def/polypie/master/LICENSE
