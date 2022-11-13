from dataclasses import MISSING, Field


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
    """Return an object to identify dataclass fields.

    default is the default value of the field.  default_factory is a
    0-argument function called to initialize a field's value.  If init
    is true, the field will be a parameter to the class's __init__()
    function.  If repr is true, the field will be included in the
    object's repr().  If hash is true, the field will be included in the
    object's hash().  If compare is true, the field will be used in
    comparison functions.  metadata, if specified, must be a mapping
    which is stored but not otherwise examined by dataclass.  If kw_only
    is true, the field will become a keyword-only parameter to
    __init__().

    It is an error to specify both default and default_factory.
    """
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("cannot specify both default and default_factory")
    field = Field(default, default_factory, init, repr, hash, compare, metadata, kw_only)
    field.__slots__ = (*getattr(field, "__slots__", ()), "alias")
    field.alias = alias
    field.__repr__ = lambda _: f"{Field.__repr__(field)[:-1]}," f"alias={field.alias})"
