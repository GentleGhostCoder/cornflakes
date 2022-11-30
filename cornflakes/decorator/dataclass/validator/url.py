from dataclasses import InitVar, field
from typing import Optional
from urllib.parse import ParseResult, urlparse, urlunparse

from cornflakes.decorator.config.tuple import to_tuple
from cornflakes.decorator.dataclass._dataclass import dataclass as data


@data(
    slots=True,
    frozen=False,
    tuple_factory=lambda self, x: urlunparse(x[:6]),  # unparse to string
    dict_factory=lambda self, x: str(self),  # to string -> tuple -> unparse to string
)
class AnyUrl:
    """Database URL.

    :cvar url: URL to init the whole object (will be overwritten with other args).
    :cvar scheme: The scheme of the url
    :cvar netloc: user / pw / host and port of the url
    :cvar path: path of the url
    :cvar params: url parameters
    :cvar query: url query
    :cvar fragment: url fragment
    :cvar hostname: url hostname (overwrites the netloc)
    :cvar port: url port (overwrites the netloc)
    :cvar username: url username (overwrites the netloc)
    :cvar password: url password (overwrites the netloc)
    """

    url: InitVar[Optional[str]] = None
    scheme: Optional[str] = field(default=None, init=True)
    netloc: Optional[str] = field(default=None, init=True)
    path: Optional[str] = field(default=None, init=True)
    params: Optional[str] = field(default=None, init=True)
    query: Optional[str] = field(default=None, init=True)
    fragment: Optional[str] = field(default=None, init=True)
    hostname: Optional[str] = field(default=None, init=True, repr=False)
    port: Optional[int] = field(default=None, init=True, repr=False)
    username: Optional[str] = field(default=None, init=True, repr=False)
    password: Optional[str] = field(default=None, init=True, repr=False)

    def __init_parsed(self, parsed: ParseResult):
        for slot in getattr(self, "__dataclass_fields__", {}).values():
            if not getattr(self, slot.name, None) and not isinstance(slot.type, InitVar):
                setattr(self, slot.name, getattr(parsed, slot.name, None))

    def __post_init__(self, url: Optional[str] = None) -> None:
        """Post init."""
        if url:
            parsed = urlparse(url)
            self.__init_parsed(parsed)
        else:
            if not self.netloc or self.username or self.password or self.hostname or self.port:
                login = f"{self.username}:{self.password}@" if self.username else ""
                parsed = urlparse(str(self))
                port = f":{self.port or parsed.port}" if self.port or parsed.port else ""
                hostname = self.hostname if self.hostname else parsed.hostname
                self.netloc = f"{login}{hostname}{port}"
            parsed = urlparse(to_tuple(self))
            self.__init_parsed(parsed)

    def __str__(self) -> str:
        """Any url string."""
        return to_tuple(self)
