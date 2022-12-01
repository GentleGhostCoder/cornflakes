def patch_module(m):
    """Method to overwrite module variables in a generic way.

    1. Overwrite names from submodules declared in __all__ to parent module.
    2. Overwrite doc_string and adds auto summary with objects defined in __all__.
    """
    for obj in [m[x] for x in m["__all__"]]:
        obj.__module__ = m["__name__"]

    m[
        "__doc__"
    ] = f"""{m["__doc__"]}
.. currentmodule:: {m["__name__"]}

.. autosummary::
   :toctree: _generate

    {'''
    '''.join(m["__all__"])}
"""
