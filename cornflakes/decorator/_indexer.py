from dataclasses import dataclass, field
from typing import Dict, Optional, Type

from cornflakes.types import IndexInstance


@dataclass
class IndexCounter:
    """Indexer Class."""

    name: str = ""
    start: int = 0
    index: int = field(default=0, init=False)
    type: Optional[Type] = field(default=None, init=False)

    def __post_init__(self):
        """Initialize the dataclass object."""
        self.type = type(
            f"{IndexInstance.__name__}.{self.name}_Index",
            (
                IndexInstance,
                int,
            ),
            {},
        )

        self.start = self.start - 1
        self.index = self.start

        def new(cls, value=0, *args, **kwargs):
            if isinstance(value, int) and self.index == self.start:
                self.start = value - 1
                self.index = self.start
            self.index += 1
            return int.__new__(cls, self.index)

        self.type.__new__ = new
        self.type.reset = lambda x=self: self.reset()
        self.is_index = True

    def reset(self):
        """Resets the index."""
        if self.index != self.start:
            self.index = self.start


class Index(int):
    """Indexer Class."""

    indices: Dict[str, IndexCounter] = {}
    is_group_indexing: bool = False

    def __new__(cls, start=None, *args, **kwds):
        """Constructor.

        This only exists to give a better error message in case
        someone tries to subclass a special typing object (not a good idea).
        """
        return super().__new__(cls).get_index("root")(start)

    @classmethod
    def get_index(cls, name: str, start: int = 0):
        """Get an Index instance with the given name."""
        if name not in cls.indices:
            # Create an instance of the new IndexCounter class
            cls.indices[name] = IndexCounter(name=name, start=start)
        return cls.indices[name].type

    def __call__(self, *args, **kwds):
        """Returns type error message."""
        raise TypeError(f"Cannot instantiate {self!r}")

    @classmethod
    def __getitem__(cls, key):
        """Return an Index instance with the given name."""
        return cls.get_index(key)

    @classmethod
    def __class_getitem__(cls, key):
        """Return an Index instance with the given name."""
        return cls.get_index(key)

    @classmethod
    def group_indexing(cls):
        """Set group indexing."""
        Index.reset()
        # print(f"Switch group indexing from {cls.is_group_indexing} to {not cls.is_group_indexing}")
        cls.is_group_indexing = not cls.is_group_indexing
        Index.reset()

    @classmethod
    def reset(cls):
        """Reset all indices to their initial values."""
        if not cls.is_group_indexing:
            for index in cls.indices.values():
                index.reset()
