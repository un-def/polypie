from collections import OrderedDict
from functools import update_wrapper
from inspect import signature
from typing import get_type_hints

from typeguard import check_argument_types, _CallMemo


__author__ = 'un.def <un.def@ya.ru>'
__version__ = '0.2.0.dev0'


_registry = {}


class PolypieException(Exception):

    pass


def _call_func(func_key, args=None, kwargs=None):
    args = args or ()
    kwargs = kwargs or {}
    for func in _registry[func_key].values():
        try:
            check_argument_types(_CallMemo(func, args=args, kwargs=kwargs))
        except TypeError:
            continue
        return func(*args, **kwargs)
    raise PolypieException(
        "Matсhing signature for function '{func}' with "
        "args={args} and kwargs={kwargs} not found".format(
            func=func_key, args=args, kwargs=kwargs)
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
    parameters_tuple = tuple(parameters.values())
    if func_key not in _registry:
        def dispatcher(*args, **kwargs):
            return _call_func(func_key, args, kwargs)
        dispatcher = update_dispatcher(dispatcher, func, assign=True)
        signature_mapping = OrderedDict()
        signature_mapping[parameters_tuple] = func
        signature_mapping.dispatcher = dispatcher
        _registry[func_key] = signature_mapping
        return dispatcher
    elif parameters_tuple not in _registry[func_key]:
        _registry[func_key][parameters_tuple] = func
        dispatcher = _registry[func_key].dispatcher
        return update_dispatcher(dispatcher, func, assign=False)
    else:
        hints = get_type_hints(func)
        sig_gen = (
            '{}:{}'.format(p, hints[p]) if p in hints else p
            for p in parameters
        )
        raise PolypieException(
            "Function '{func}' with signature ({sig}) "
            "already exists".format(func=func_key, sig=', '.join(sig_gen))
        )
