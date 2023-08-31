from typing import List, Protocol, runtime_checkable

from click import Option


@runtime_checkable
class GlobalOption(Protocol):
    """GlobalOption Protocol which requires params."""

    params: List[Option]

    def __call__(self, *args, **kwargs):
        ...
