from polypie import polymorphic


RESULT = 'module1'


@polymorphic
def check_clash(a: int):
    return RESULT
