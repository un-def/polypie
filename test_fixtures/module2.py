from polypie import polymorphic


RESULT = 'module2'


@polymorphic
def check_clash(a: int):
    return RESULT
