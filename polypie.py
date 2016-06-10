from inspect import Signature
from typing import get_type_hints
from collections import OrderedDict

from typecheck import typecheck, TypeCheckError


__author__ = 'un.def <un.def@ya.ru>'
__version__ = '0.1.1'


registry = {}


class PolypieException(Exception):

    pass


def _call_func(func_name, args=None, kwargs=None):
    args = args or ()
    kwargs = kwargs or {}
    for sig, func in registry[func_name].items():
        if sig == 'wrapper':
            continue
        try:
            sig.bind(*args, **kwargs)
        except TypeError:
            continue
        try:
            return typecheck(func)(*args, **kwargs)
        except TypeCheckError:
            pass
    raise PolypieException(
        "Matсhing signature for function '{func}' with "
        "args={args} and kwargs={kwargs} not found".format(func=func_name,
                                                           args=args,
                                                           kwargs=kwargs)
    )


def polymorphic(func):
    global registry
    func_name = func.__name__
    sig = Signature.from_callable(func)
    sig = Signature(sig.parameters.values())
    if func_name not in registry:
        def wrapper(*args, **kwargs):
            return _call_func(func_name, args, kwargs)
        registry[func_name] = OrderedDict((
            ('wrapper', wrapper),
            (sig, func),
        ))
        return wrapper
    else:
        if sig in registry[func_name]:
            hints = get_type_hints(func)
            sig_gen = ("{}:{}".format(p, hints[p]) for p in sig.parameters)
            raise PolypieException(
                "Function '{func}' with signature ({sig}) "
                "already exists".format(func=func_name,
                                        sig=", ".join(sig_gen))
            )
        else:
            registry[func_name][sig] = func
            return registry[func_name]['wrapper']
