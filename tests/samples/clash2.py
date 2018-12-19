from polypie import polymorphic


RESULT = 'clash2'


@polymorphic
def check_clash(a: int):
    return RESULT
