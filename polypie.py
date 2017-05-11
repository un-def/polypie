from collections import OrderedDict
from functools import wraps
from inspect import Signature, signature, Parameter
from typing import get_type_hints

from typecheck import typecheck, TypeCheckError


__author__ = 'un.def <un.def@ya.ru>'
__version__ = '0.1.3'


_registry = {}


class PolypieException(Exception):
    pass


class HashableParameter(Parameter):
    def __hash__(self):
        return hash((self.name, self.kind, self.default, self.annotation))

    @staticmethod
    def from_parameter(parameter):
        return HashableParameter(
            name=parameter.name,
            kind=parameter.kind,
            default=parameter.default,
            annotation=parameter.annotation
        )


def _call_func(func_key, args=(), kwargs={}):
    for parameters_tuple, func in _registry[func_key].items():
        if parameters_tuple == 'wrapper':
            continue
        try:
            Signature(parameters_tuple).bind(*args, **kwargs)
        except TypeError:
            continue
        try:
            return typecheck(func)(*args, **kwargs)
        except TypeCheckError:
            pass
    raise PolypieException(
        "Matсhing signature for function '{func}' with "
        "args={args} and kwargs={kwargs} not found".format(func=func_key,
                                                           args=args,
                                                           kwargs=kwargs)
    )


def polymorphic(func):
    func_key = func.__module__ + '.' + func.__qualname__
    parameters = signature(func).parameters
    parameters_tuple = tuple(
        HashableParameter.from_parameter(p) for p in parameters.values())
    if func_key not in _registry:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return _call_func(func_key, args, kwargs)
        _registry[func_key] = OrderedDict((
            ('wrapper', wrapper),
            (parameters_tuple, func),
        ))
        return wrapper
    else:
        if parameters_tuple in _registry[func_key]:
            hints = get_type_hints(func)
            sig_gen = ('{}:{}'.format(p, hints[p]) if p in hints else p
                       for p in parameters)
            raise PolypieException(
                "Function '{func}' with signature ({sig}) "
                "already exists".format(func=func_key,
                                        sig=', '.join(sig_gen))
            )
        else:
            _registry[func_key][parameters_tuple] = func
            return _registry[func_key]['wrapper']


__all__ = [PolypieException.__name__, polymorphic.__name__]
