from importlib import import_module
from inspect import getmembers, ismodule
import logging
import os
from pkgutil import iter_modules

__pached_modules = []


def isclassmethod(method):
    """Check if a classmethod."""
    bound_to = getattr(method, "__self__", None)
    if not isinstance(bound_to, type):
        # must be bound to a class
        return False
    name = method.__name__
    for cls in bound_to.__mro__:
        descriptor = vars(cls).get(name)
        if descriptor is not None:
            return isinstance(descriptor, classmethod)
    return False


def _patch_module(m):
    """Method to overwrite module variables in a generic way.

    1. Overwrite names from submodules declared in __all__ to parent module.
    2. Overwrite doc_string and adds auto summary with objects defined in __all__.
    """
    for obj in [getattr(m, x, None) for x in getattr(m, "__all__", [key for key, _ in getmembers(m)])]:
        if not obj:
            continue
        if ismodule(obj):
            _patch_module(obj)
            for sub_m in iter_modules(getattr(obj, "__path__", [])):
                _patch_module(import_module(f"{obj.__name__}.{sub_m.name}"))
            return
        if not isclassmethod(obj):
            try:
                obj.__module__ = getattr(m, "__name__", "")
            except Exception as e:
                logging.debug(e)

    m.__doc__ = f"""{getattr(m, "__doc__", f"{getattr(m, '__name__', '')} module.")}

.. currentmodule:: {getattr(m, '__name__', '')}

.. autosummary::
   :toctree: _generate

    {'''
    '''.join(getattr(m, "__all__", [key for key, _ in getmembers(m)]))}
"""


def patch_module(module: str):
    """Method to overwrite module with all submodules in a generic way.

    1. Overwrite names from submodules declared in __all__ to parent module.
    2. Overwrite doc_string and adds auto summary with objects defined in __all__.
    """
    if os.environ.get("CORNFLAKES_GENERATING_CONFIG_MODULE", "") == "True" or module in __pached_modules:
        return
    __pached_modules.append(module)
    m = import_module(module)
    for sub_m in iter_modules(getattr(m, "__path__", [])):
        _patch_module(import_module(f"{m.__name__}.{sub_m.name}"))
    _patch_module(m)
