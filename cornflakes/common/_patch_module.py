import inspect


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


def patch_module(m):
    """Method to overwrite module variables in a generic way.

    1. Overwrite names from submodules declared in __all__ to parent module.
    2. Overwrite doc_string and adds auto summary with objects defined in __all__.
    """
    for obj in [m[x] for x in m["__all__"]]:
        if not inspect.ismodule(obj) and not isclassmethod(obj):
            try:
                obj.__module__ = m["__name__"]
            except AttributeError:
                pass

    m[
        "__doc__"
    ] = f"""{m["__doc__"]}
.. currentmodule:: {m["__name__"]}

.. autosummary::
   :toctree: _generate

    {'''
    '''.join(m["__all__"])}
"""
