from polypie import polymorphic


class Wrapper:

    ATTR1 = 'attr1'
    ATTR2 = 'attr2'

    def check_special_attrs(a: int):
        return True

    check_special_attrs.attr1 = ATTR1

    NAME = check_special_attrs.__name__
    QUALNAME = check_special_attrs.__qualname__
    MODULE = check_special_attrs.__module__

    check_special_attrs = polymorphic(check_special_attrs)

    def check_special_attrs(a: str):
        return False

    check_special_attrs.attr2 = ATTR2

    check_special_attrs = polymorphic(check_special_attrs)
