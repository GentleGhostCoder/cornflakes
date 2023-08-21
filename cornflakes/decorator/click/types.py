from typing import List, Protocol

from click import Option


class GlobalOption(Protocol):
    """GlobalOption Protocol which requires params."""

    params: List[Option]
