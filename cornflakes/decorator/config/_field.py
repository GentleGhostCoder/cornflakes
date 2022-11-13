from dataclasses import MISSING, Field
from typing import cast


class ConfigField(Field):
    """Instances of dataclasses Field wrapped for configs."""

    __slots__ = (*getattr(Field, "__slots__", ()), "alias")

    def __init__(self, default, default_factory, init, repr, hash, compare, metadata, kw_only, alias):
        """Init Field method."""
        self.alias = alias
        super().__init__(default, default_factory, init, repr, hash, compare, metadata, kw_only)  # type: ignore

    def __repr__(self):
        """Repr Field method."""
        return f"{Field.__repr__(self)[:-1]}," f"alias={self.alias})"


def config_field(
    *,
    default=MISSING,
    default_factory=MISSING,
    init=True,
    repr=True,
    hash=None,
    compare=True,
    metadata=None,
    kw_only=MISSING,
    alias=None,
):
    """This function is used instead of exposing Field creation directly.

    So that a type checker can be told (via overloads) that this is a function whose type depends on its parameters.
    """
    new_field: Field = ConfigField(
        alias=alias,
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        kw_only=kw_only,
    )
    return cast(Field, new_field)
