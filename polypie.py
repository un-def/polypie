from collections import OrderedDict
from functools import update_wrapper
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

    @classmethod
    def from_parameter(cls, parameter):
        return cls(
            name=parameter.name,
            kind=parameter.kind,
            default=parameter.default,
            annotation=parameter.annotation
        )


def _call_func(func_key, args=None, kwargs=None):
    args = args or ()
    kwargs = kwargs or {}
    for parameters_tuple, func in _registry[func_key].items():
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


def update_dispatcher(dispatcher, func, assign=True):
    assigned = ('__name__', '__qualname__', '__module__') if assign else ()
    dispatcher = update_wrapper(dispatcher, func, assigned)
    del dispatcher.__wrapped__
    return dispatcher


def polymorphic(func):
    global _registry
    func_key = func.__module__ + '.' + func.__qualname__
    parameters = signature(func).parameters
    parameters_tuple = tuple(
        HashableParameter.from_parameter(p) for p in parameters.values())
    if func_key not in _registry:
        def dispatcher(*args, **kwargs):
            return _call_func(func_key, args, kwargs)
        dispatcher = update_dispatcher(dispatcher, func, assign=True)
        signature_mapping = OrderedDict()
        signature_mapping[parameters_tuple] = func
        signature_mapping.dispatcher = dispatcher
        _registry[func_key] = signature_mapping
        return dispatcher
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
            dispatcher = _registry[func_key].dispatcher
            return update_dispatcher(dispatcher, func, assign=False)
