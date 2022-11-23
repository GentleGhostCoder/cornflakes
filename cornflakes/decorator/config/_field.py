from dataclasses import MISSING, Field
from typing import List, Optional, Union


class ConfigField(Field):
    """Instances of dataclasses Field wrapped for configs."""

    __slots__ = (*getattr(Field, "__slots__", ()), "alias", "ignore")

    def __init__(
        self,
        default=MISSING,
        default_factory=MISSING,
        init: Optional[bool] = True,
        repr: Optional[bool] = True,
        hash: Optional[bool] = None,
        compare: Optional[bool] = True,
        metadata: Optional[bool] = None,
        kw_only=MISSING,
        alias: Optional[Union[List[str], str]] = None,
        ignore: Optional[bool] = False,
    ):
        """Init Field method."""
        super().__init__(
            **{
                key: value
                for key, value in (
                    ("default", default),  # type: ignore
                    ("default_factory", default_factory),
                    ("init", init),
                    ("repr", repr),
                    ("hash", hash),
                    ("compare", compare),
                    ("metadata", metadata),
                    ("kw_only", kw_only),
                )
                if key in Field.__init__.__code__.co_varnames
            }
        )
        self.alias = alias
        self.ignore = ignore

    def __repr__(self):
        """Repr Field method."""
        return f"{Field.__repr__(self)[:-1]}," f"alias={self.alias}, ignore={self.ignore})"


# This function is used instead of exposing Field creation directly,
# so that a type checker can be told (via overloads) that this is a
# function whose type depends on its parameters.
def config_field(
    *,
    default=MISSING,
    default_factory=MISSING,
    init: Optional[bool] = True,
    repr: Optional[bool] = True,
    hash: Optional[bool] = None,
    compare: Optional[bool] = True,
    metadata: Optional[bool] = None,
    kw_only=MISSING,
    alias: Optional[Union[List[str], str]] = None,
    ignore: Optional[bool] = False,
):
    """This function is used instead of exposing Field creation directly.

    So that a type checker can be told (via overloads) that this is a function whose type depends on its parameters.
    """
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("cannot specify both default and default_factory")
    new_field = ConfigField(default, default_factory, init, repr, hash, compare, metadata, kw_only, alias, ignore)
    new_field.alias = alias
    return new_field
