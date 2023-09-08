from importlib import import_module
from inspect import getmembers, ismodule
import logging
import os
from pkgutil import iter_modules

logger = logging.getLogger(__name__)

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


patch_modules: list = []


def _patch_module(m: str, main_module: str):
    """Method to overwrite module variables in a generic way.

    1. Overwrite names from submodules declared in __all__ to parent module.
    2. Overwrite doc_string and adds auto summary with objects defined in __all__.
    """
    if main_module not in m:
        # skip
        return
    module = import_module(m)
    for obj in [getattr(module, x, None) for x in getattr(module, "__all__", [key for key, _ in getmembers(module)])]:
        if not obj:
            continue
        if ismodule(obj):
            _patch_module(obj.__name__, main_module)
            for sub_m in iter_modules(getattr(obj, "__path__", [])):
                if f"{obj.__name__}.{sub_m.name}" in patch_modules:
                    continue
                patch_modules.append(f"{obj.__name__}.{sub_m.name}")
                _patch_module(f"{obj.__name__}.{sub_m.name}", main_module)
            return
        if not isclassmethod(obj):
            try:
                obj.__module__ = getattr(module, "__name__", "")
            except Exception as e:
                logger.debug(e)

    module.__doc__ = f"""{getattr(module, "__doc__", f"{getattr(module, '__name__', '')} module.")}

.. currentmodule:: {getattr(module, '__name__', '')}

.. autosummary::
   :toctree: _generate

    {'''
    '''.join(getattr(module, "__all__", [key for key, _ in getmembers(module) if not key.startswith("_")]))}
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
    main_module = m.__name__
    for sub_m in iter_modules(getattr(m, "__path__", [])):
        if f"{m.__name__}.{sub_m.name}" in patch_modules:
            continue
        patch_modules.append(f"{m.__name__}.{sub_m.name}")
        _patch_module(f"{m.__name__}.{sub_m.name}", main_module)
    _patch_module(module, main_module)
