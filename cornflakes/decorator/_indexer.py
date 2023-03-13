from dataclasses import dataclass, field
from typing import Dict, Optional, Type, TypeVar

T = TypeVar("T")


def is_index(obj):
    """Returns True if the given object is an index type."""
    return getattr(getattr(obj, "__class__", {}), "__name__", "")[-6:] == "_Index"


@dataclass
class IndexCounter:
    """Indexer Class."""

    name: str = ""
    start: int = 0
    index: int = field(default=0, init=False)
    type: Optional[Type] = field(default=None, init=False)

    def __post_init__(self):
        """Initialize the dataclass object."""
        self.type = type(f"{self.name}_Index", (int,), {})

        self.start = self.start - 1
        self.index = self.start

        def new(cls, value=None):
            if isinstance(value, int) and self.index == self.start:
                self.start = value - 1
                self.index = self.start
            self.index += 1
            return int.__new__(cls, int(self.index))

        self.type.__new__ = new
        self.type.reset = lambda: self.reset()
        self.is_index = True

    def reset(self):
        """Resets the index."""
        if not self.index == self.start:
            self.index = self.start


class Index(int):
    """Indexer Class."""

    indices: Dict[str, IndexCounter] = {}

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
    def reset(cls):
        """Reset all indices to their initial values."""
        for index in cls.indices.values():
            index.reset()
