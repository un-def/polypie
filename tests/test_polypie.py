from imp import reload
from typing import Any, Sequence, Tuple, Union

import pytest

import polypie


@pytest.fixture(autouse=True)
def reload_polypie():
    reload(polypie)


def test_without_annotations():

    @polypie.polymorphic
    def f():
        return 0

    @polypie.polymorphic
    def f(a):
        return 1

    @polypie.polymorphic
    def f(a, b):
        return 2

    assert f() == 0
    assert f(120) == 1
    assert f(120, 'foo') == 2
    with pytest.raises(polypie.PolypieException, match='not found'):
        f(120, 240, 'foo')


def test_same_types_annotations():

    @polypie.polymorphic
    def f(a: int, b: int):
        return 'int, int first'

    @polypie.polymorphic
    def f(x: int, y: int):
        return 'int, int second'

    @polypie.polymorphic
    def f(a: int, b: str):
        return 'int, str'

    assert f(120, 240) == 'int, int first'
    assert f(a=120, b=240) == 'int, int first'
    assert f(x=120, y=240) == 'int, int second'
    assert f(120, 'foo') == 'int, str'
    assert f(a=120, b='foo') == 'int, str'


def test_builtin_types_annotations():

    @polypie.polymorphic
    def f(a: int, b: int):
        return 'int, int'

    @polypie.polymorphic
    def f(a: int, b: str):
        return 'int, str'

    @polypie.polymorphic
    def f(a, b: dict):
        return 'any, dict'

    assert f(120, 240) == 'int, int'
    assert f(120, 'foo') == 'int, str'
    assert f(120, {}) == 'any, dict'
    assert f('foo', {}) == 'any, dict'


def test_own_types_annotations():

    class Foo:
        pass

    class Bar:
        pass

    @polypie.polymorphic
    def f(a: Foo, b: Bar):
        return 'Foo, Bar'

    @polypie.polymorphic
    def f(a: Bar, b: Foo):
        return 'Bar, Foo'

    foo = Foo()
    bar = Bar()
    assert f(foo, bar) == 'Foo, Bar'
    assert f(bar, foo) == 'Bar, Foo'
    with pytest.raises(polypie.PolypieException, match='not found'):
        f(foo, foo)


def test_typing_annotations():

    @polypie.polymorphic
    def f(a: Any, b: Sequence):
        return 'Any, Sequence'

    @polypie.polymorphic
    def f(a: Tuple[int, str], b: Union[int, bool]):
        return 'Tuple, Union'

    assert f(120, [1, 2, 3]) == 'Any, Sequence'
    assert f((120, 'foo'), 120) == 'Tuple, Union'
    assert f((120, 'foo'), True) == 'Tuple, Union'
    with pytest.raises(polypie.PolypieException, match='not found'):
        f(('foo', 120), 100)
    with pytest.raises(polypie.PolypieException, match='not found'):
        f((120, 'foo'), None)


def test_name_clashing():

    @polypie.polymorphic
    def check_clash(a: int):
        return 'top'

    class Wrapper:
        @polypie.polymorphic
        def check_clash(a: int):
            return 'wrapped'

    from samples import clash1, clash2
    assert check_clash(1) == 'top'
    assert Wrapper.check_clash(1), 'wrapped'
    assert clash1.check_clash(1) == clash1.RESULT
    assert clash2.check_clash(1) == clash2.RESULT


def test_methods():

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
    assert instance.getter() == 'foo'
    instance.setter(1)
    assert instance.getter() == '1'
    # cls methods
    assert instance.cls_getter() == 'cls'
    instance.cls_setter('bar')
    assert instance.cls_getter() == 'bar'
    instance.cls_setter(2)
    assert instance.cls_getter() == '2'
    assert instance.getter() == '1'
    # static methods
    instance.static_setter(instance, 'baz')
    instance.static_setter(TestClass, 'xyzzy')
    assert instance.static_getter(instance) == 'baz'
    assert instance.static_getter(TestClass) == 'xyzzy'
    instance.static_setter(instance, 100)
    instance.static_setter(TestClass, 200)
    assert instance.static_getter(instance) == '100'
    assert instance.static_getter(TestClass) == '200'


def test_exception_due_to_existent_signature():

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

    with pytest.raises(polypie.PolypieException, match='already exists'):
        @polypie.polymorphic
        def f(a, b: str):
            pass


def test_function_special_attrs():
    from samples.specialattrs import Wrapper
    assert Wrapper.check_special_attrs.__name__ == Wrapper.NAME
    assert Wrapper.check_special_attrs.__qualname__ == Wrapper.QUALNAME
    assert Wrapper.check_special_attrs.__module__ == Wrapper.MODULE
    assert Wrapper.check_special_attrs.attr1 == Wrapper.ATTR1
    assert Wrapper.check_special_attrs.attr2 == Wrapper.ATTR2
    assert not Wrapper.check_special_attrs.__annotations__
    assert not hasattr(Wrapper.check_special_attrs, '__wrapped__')
