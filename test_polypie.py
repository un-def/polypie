import unittest
from imp import reload
from typing import Any, Sequence, Tuple, Union

import polypie


class PolypieTestCase(unittest.TestCase):

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
        from test_fixtures import clash1, clash2
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
        self.assertEqual(clash1.check_clash(1), clash1.RESULT)
        self.assertEqual(clash2.check_clash(1), clash2.RESULT)

    def test_methods(self):
        class TestClass:

            value = 'cls'

            def __init__(self):
                self.value = None

            def getter(self):
                return self.value

            @polypie.polymorphic
            def setter(self, value: str):
                self.value = value

            @polypie.polymorphic
            def setter(self, value: int):
                self.value = str(value)

            @classmethod
            def cls_getter(cls):
                return cls.value

            @classmethod
            @polypie.polymorphic
            def cls_setter(cls, value: str):
                cls.value = value

            @classmethod
            @polypie.polymorphic
            def cls_setter(cls, value: int):
                cls.value = str(value)

            @staticmethod
            def static_getter(obj):
                return obj.value

            @staticmethod
            @polypie.polymorphic
            def static_setter(obj, value: str):
                obj.value = value

            @staticmethod
            @polypie.polymorphic
            def static_setter(obj, value: int):
                obj.value = str(value)

        instance = TestClass()
        # instance methods
        instance.setter('foo')
        self.assertEqual(instance.getter(), 'foo')
        instance.setter(1)
        self.assertEqual(instance.getter(), '1')
        # cls methods
        self.assertEqual(instance.cls_getter(), 'cls')
        instance.cls_setter('bar')
        self.assertEqual(instance.cls_getter(), 'bar')
        instance.cls_setter(2)
        self.assertEqual(instance.cls_getter(), '2')
        self.assertEqual(instance.getter(), '1')
        # static methods
        instance.static_setter(instance, 'baz')
        instance.static_setter(TestClass, 'xyzzy')
        self.assertEqual(instance.static_getter(instance), 'baz')
        self.assertEqual(instance.static_getter(TestClass), 'xyzzy')
        instance.static_setter(instance, 100)
        instance.static_setter(TestClass, 200)
        self.assertEqual(instance.static_getter(instance), '100')
        self.assertEqual(instance.static_getter(TestClass), '200')

    def test_exception_due_to_existent_signature(self):
        @polypie.polymorphic
        def f(a):
            pass

        @polypie.polymorphic
        def f(a, b):
            pass

        @polypie.polymorphic
        def f(a, b: str):
            pass

        @polypie.polymorphic
        def f(a, b: int):
            pass

        with self.assertRaisesRegex(
                polypie.PolypieException, "already exists"):
            @polypie.polymorphic
            def f(a, b: str):
                pass

    def test_function_special_attrs(self):
        from test_fixtures.specialattrs import Wrapper

        self.assertEqual(Wrapper.check_special_attrs.__name__,
                         Wrapper.NAME)
        self.assertEqual(Wrapper.check_special_attrs.__qualname__,
                         Wrapper.QUALNAME)
        self.assertEqual(Wrapper.check_special_attrs.__module__,
                         Wrapper.MODULE)
        self.assertEqual(Wrapper.check_special_attrs.attr1, Wrapper.ATTR1)
        self.assertEqual(Wrapper.check_special_attrs.attr2, Wrapper.ATTR2)
        self.assertFalse(Wrapper.check_special_attrs.__annotations__)
        self.assertFalse(hasattr(Wrapper.check_special_attrs, '__wrapped__'))


if __name__ == '__main__':
    unittest.main()
