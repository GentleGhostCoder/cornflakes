from dataclasses import dataclass as new_dataclass

from cornflakes.decorator.config._field import Field


def dataclass(cls, *args, **kwargs):
    """Returns the same class as was passed in, with dunder methods added based on the fields defined in the class.

    Examines PEP 526 __annotations__ to determine fields.

    If init is true, an __init__() method is added to the class. If
    repr is true, a __repr__() method is added. If order is true, rich
    comparison dunder methods are added. If unsafe_hash is true, a
    __hash__() method function is added. If frozen is true, fields may
    not be assigned to after instance creation. If match_args is true,
    the __match_args__ tuple is added. If kw_only is true, then by
    default all fields are keyword-only. If slots is true, an
    __slots__ attribute is added.

    Extra: wrapped for configs with updated fields.
    """

    def wrap(cls):
        dataclass_fields = {
            obj_name: getattr(cls, obj_name)
            for obj_name in dir(cls)
            if isinstance(getattr(cls, obj_name), Field) and hasattr(getattr(cls, obj_name), "alias")
        }
        new_cls = new_dataclass(cls, *args, **kwargs)
        new_cls.__dataclass_fields__.update(dataclass_fields)
        return new_cls

    # See if we're being called as @dataclass or @dataclass().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @dataclass without parens.
    return wrap(cls)
