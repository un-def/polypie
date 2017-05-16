from polypie import polymorphic


RESULT = 'clash1'


@polymorphic
def check_clash(a: int):
    return RESULT
