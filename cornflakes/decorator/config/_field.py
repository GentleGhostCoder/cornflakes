from dataclasses import MISSING, Field, field
import logging


class ConfigField(Field):
    """Instances of dataclasses Field wrapped for configs."""

    __slots__ = (*getattr(Field, "__slots__", ()), "alias")

    def __init__(
        self, default, default_factory, init: bool, repr: bool, hash: bool, compare: bool, metadata, kw_only, alias
    ):
        """Init Field method."""
        super().__init__(default, default_factory, init, repr, hash, compare, metadata, kw_only)
        self.alias = alias

    def __repr__(self):
        """Repr Field method."""
        return f"{Field.__repr__(self)[:-1]}," f"alias={self.alias})"


# This function is used instead of exposing Field creation directly,
# so that a type checker can be told (via overloads) that this is a
# function whose type depends on its parameters.
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
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("cannot specify both default and default_factory")
    try:
        new_field = ConfigField(default, default_factory, init, repr, hash, compare, metadata, kw_only, alias)
        new_field.alias = alias
        return new_field
    except TypeError as e:
        logging.error(e)
        return field(
            default=default,
            default_factory=default_factory,
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=metadata,
        )
