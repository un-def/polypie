from inspect import Signature, signature, Parameter
from typing import get_type_hints
from collections import OrderedDict

from typecheck import typecheck, TypeCheckError


__author__ = 'un.def <un.def@ya.ru>'
__version__ = '0.1.2'


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


def _call_func(func_name, args=None, kwargs=None):
    args = args or ()
    kwargs = kwargs or {}
    for parameters_tuple, func in _registry[func_name].items():
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
        "args={args} and kwargs={kwargs} not found".format(func=func_name,
                                                           args=args,
                                                           kwargs=kwargs)
    )


def polymorphic(func):
    global _registry
    func_name = func.__name__
    parameters = signature(func).parameters
    parameters_tuple = tuple(
        HashableParameter.from_parameter(p) for p in parameters.values())
    if func_name not in _registry:
        def wrapper(*args, **kwargs):
            return _call_func(func_name, args, kwargs)
        wrapper.__name__ = func_name
        wrapper.__qualname__ = func.__qualname__
        _registry[func_name] = OrderedDict((
            ('wrapper', wrapper),
            (parameters_tuple, func),
        ))
        return wrapper
    else:
        if parameters_tuple in _registry[func_name]:
            hints = get_type_hints(func)
            sig_gen = ('{}:{}'.format(p, hints[p]) if p in hints else p
                       for p in parameters)
            raise PolypieException(
                "Function '{func}' with signature ({sig}) "
                "already exists".format(func=func_name,
                                        sig=', '.join(sig_gen))
            )
        else:
            _registry[func_name][parameters_tuple] = func
            return _registry[func_name]['wrapper']
