"""cornflakes common module.
__________________________________

.. currentmodule:: cornflakes.common

.. autosummary::
   :toctree: _generate

    add_slots
    default_ca_path
    import_component
"""  # noqa: RST303 D205
from cornflakes.common._import_component import import_component
from cornflakes.common._default_ca_path import default_ca_path

__all__ = ["import_component", "default_ca_path"]
