import unittest
from imp import reload
from typing import Any, Sequence, Tuple, Union

import polypie


class PolymorphicFunctionsTestCase(unittest.TestCase):

    def setUp(self):
        reload(polypie)

    def test_without_annotations(self):
        @polypie.polymorphic
        def f():
            return 0

        @polypie.polymorphic
        def f(a):
            return 1

        @polypie.polymorphic
        def f(a, b):
            return 2

        self.assertEqual(f(), 0)
        self.assertEqual(f(120), 1)
        self.assertEqual(f(120, 'foo'), 2)
        with self.assertRaisesRegex(polypie.PolypieException, 'not found'):
            f(120, 240, 'foo')

    def test_same_types_annotations(self):
        @polypie.polymorphic
        def f(a: int, b: int):
            return 'int, int first'

        @polypie.polymorphic
        def f(x: int, y: int):
            return 'int, int second'

        @polypie.polymorphic
        def f(a: int, b: str):
            return 'int, str'

        self.assertEqual(f(120, 240), 'int, int first')
        self.assertEqual(f(a=120, b=240), 'int, int first')
        self.assertEqual(f(x=120, y=240), 'int, int second')
        self.assertEqual(f(120, 'foo'), 'int, str')
        self.assertEqual(f(a=120, b='foo'), 'int, str')

    def test_builtin_types_annotations(self):
        @polypie.polymorphic
        def f(a: int, b: int):
            return 'int, int'

        @polypie.polymorphic
        def f(a: int, b: str):
            return 'int, str'

        @polypie.polymorphic
        def f(a, b: dict):
            return 'any, dict'

        self.assertEqual(f(120, 240), 'int, int')
        self.assertEqual(f(120, 'foo'), 'int, str')
        self.assertEqual(f(120, {}), 'any, dict')
        self.assertEqual(f('foo', {}), 'any, dict')

    def test_own_types_annotations(self):
        class Foo():
            pass

        class Bar():
            pass

        @polypie.polymorphic
        def f(a: Foo, b: Bar):
            return 'Foo, Bar'

        @polypie.polymorphic
        def f(a: Bar, b: Foo):
            return 'Bar, Foo'

        foo = Foo()
        bar = Bar()

        self.assertEqual(f(foo, bar), 'Foo, Bar')
        self.assertEqual(f(bar, foo), 'Bar, Foo')
        with self.assertRaisesRegex(polypie.PolypieException, 'not found'):
            f(foo, foo)

    def test_typing_annotations(self):
        @polypie.polymorphic
        def f(a: Any, b: Sequence):
            return 'Any, Sequence'

        @polypie.polymorphic
        def f(a: Tuple[int, str], b: Union[int, bool]):
            return 'Tuple, Union'

        self.assertEqual(f(120, [1, 2, 3]), 'Any, Sequence')
        self.assertEqual(f((120, 'foo'), 120), 'Tuple, Union')
        self.assertEqual(f((120, 'foo'), True), 'Tuple, Union')
        with self.assertRaisesRegex(polypie.PolypieException, 'not found'):
            f(('foo', 120), 100)
        with self.assertRaisesRegex(polypie.PolypieException, 'not found'):
            f((120, 'foo'), None)

    def test_name_clashing(self):
        from test_fixtures import module1, module2
        TOP = 'top'
        WRAPPED = 'wrapped'

        @polypie.polymorphic
        def check_clash(a: int):
            return TOP

        class Wrapper:
            @polypie.polymorphic
            def check_clash(a: int):
                return WRAPPED

        self.assertEqual(check_clash(1), TOP)
        self.assertEqual(Wrapper.check_clash(1), WRAPPED)
        self.assertEqual(module1.check_clash(1), module1.RESULT)
        self.assertEqual(module2.check_clash(1), module2.RESULT)


if __name__ == '__main__':
    unittest.main()
