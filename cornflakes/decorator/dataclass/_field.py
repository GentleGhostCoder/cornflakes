from dataclasses import Field as DataclassField
from dataclasses import MISSING
from typing import Any, Callable, List, Optional, Union

from cornflakes.decorator._types import WITHOUT_DEFAULT, _WithoutDefault

_MISSING_TYPE = type(MISSING)


class Field(DataclassField):
    """Instances of dataclasses Field wrapped for configs.

    Info:
       currently only supported arguments are:
       `default, default_factory, init, repr, hash, compare, metadata, kw_only, validator, alias, ignore`
       other arguments will be ignored when initialise dataclass.
    """

    __slots__ = (
        *getattr(
            DataclassField,
            "__slots__",
            (),
        ),
        "validator",
        "ignore",
        "alias",
        "title",
        "description",
        "exclude",
        "include",
        "const",
        "gt",
        "ge",
        "lt",
        "le",
        "multiple_of",
        "allow_inf_nan",
        "max_digits",
        "decimal_places",
        "min_items",
        "max_items",
        "unique_items",
        "min_length",
        "max_length",
        "allow_mutation",
        "regex",
        "discriminator",
        "extra",
    )

    def __init__(
        self,
        default: Union[_MISSING_TYPE, Any] = MISSING,
        default_factory: Union[_MISSING_TYPE, _WithoutDefault, Callable[..., Any]] = MISSING,
        init: Optional[bool] = True,
        repr: Optional[bool] = True,
        hash: Optional[Union[bool, _MISSING_TYPE]] = None,
        compare: Optional[bool] = True,
        metadata: Optional[bool] = None,
        kw_only: Union[_MISSING_TYPE, bool] = MISSING,
        validator: Optional[Union[Callable[[str], Any], _MISSING_TYPE]] = MISSING,
        alias: Optional[Union[List[str], str]] = None,
        ignore: Optional[bool] = False,
        title: Optional[str] = None,
        description: Optional[str] = None,
        exclude: Optional[Union[str, List[str]]] = None,
        include: Optional[Union[str, List[str]]] = None,
        const: Optional[bool] = None,
        gt: Optional[Union[int, float]] = None,
        ge: Optional[Union[int, float]] = None,
        lt: Optional[Union[int, float]] = None,
        le: Optional[Union[int, float]] = None,
        multiple_of: Optional[Union[int, float]] = None,
        allow_inf_nan: Optional[bool] = True,
        max_digits: Optional[int] = None,
        decimal_places: Optional[int] = None,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        unique_items: Optional[bool] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        allow_mutation: Optional[bool] = True,
        regex: Optional[str] = None,
        discriminator: Optional[str] = None,
        **extra: Any,
    ):
        """Init Field method.

        :param default: Default value for field.
        :param default_factory: Default factory for field.
        :param init: Field will be included in __init__ method.
        :param repr: Field will be included in __repr__ method.
        :param hash: Field will be included in __hash__ method.
        :param compare: Field will be included in __eq__ method.
        :param metadata: Field will be included in metadata.
        :param kw_only: Field will be included in __init__ method as keyword only.
        :param validator: Validator for field.
        :param alias: Aliases for config data (will be used to read from config files).
        :param ignore: Field will be ignored when writing to_ini etc.
        :param title: Can be any string, used in the schema.
        :param description: can be any string, used in the schema.
        :param exclude: exclude this field while dumping. Takes same values as
                the ``include`` and ``exclude`` arguments on the ``.dict`` method.
        :param include: include this field while dumping. Takes same values as the
                ``include`` and ``exclude`` arguments on the ``.dict`` method.
        :param const: this field is required and *must* take it's default value
        :param gt: only applies to numbers, requires the field to be "greater than".
                The schema will have an ``exclusiveMinimum`` validation keyword
        :param ge: only applies to numbers, requires the field to be "greater than or equal to".
                The schema will have a ``minimum`` validation keyword
        :param lt: only applies to numbers, requires the field to be "less than".
                The schema will have an ``exclusiveMaximum`` validation keyword
        :param le: only applies to numbers, requires the field to be "less than or equal to".
                The schema will have a ``maximum`` validation keyword
        :param multiple_of: only applies to numbers, requires the field to be "a multiple of".
                The schema will have a ``multipleOf`` validation keyword
        :param allow_inf_nan: only applies to numbers, allows the field to be NaN or infinity (+inf or -inf),
                which is a valid Python float. Default True, set to False for compatibility with JSON.
        :param max_digits: only applies to Decimals, requires the field to have a maximum number of digits
                within the decimal. It does not include a zero before the decimal point or trailing decimal zeroes.
        :param decimal_places: only applies to Decimals, requires the field to have at most a number of
                decimal places allowed. It does not include trailing decimal zeroes.
        :param min_items: only applies to lists, requires the field to have a minimum number of elements.
                The schema will have a ``minItems`` validation keyword
        :param max_items: only applies to lists, requires the field to have a maximum number of elements.
                The schema will have a ``maxItems`` validation keyword
        :param unique_items: only applies to lists, requires the field not to have duplicated elements.
                The schema will have a ``uniqueItems`` validation keyword
        :param min_length: only applies to strings, requires the field to have a minimum length.
                The schema will have a ``minLength`` validation keyword
        :param max_length: only applies to strings, requires the field to have a maximum length.
                The schema will have a ``maxLength`` validation keyword
        :param allow_mutation: a boolean which defaults to True. When False, the field raises a TypeError if
                the field is assigned on an instance.  The BaseModel Config must set validate_assignment to True
        :param regex: only applies to strings, requires the field match against a regular expression pattern string.
                The schema will have a ``pattern`` validation keyword
        :param discriminator: only useful with a (discriminated a.k.a. tagged) `Union` of sub models with a common field.
                The `discriminator` is the name of this common field to shorten validation and improve generated schema
        :param repr: show this field in the representation
        :param extra: any additional keyword arguments will be added as is to the schema

        Returns: None
        """
        self.validator = validator
        self.ignore = ignore
        self.alias = alias
        self.title = title
        self.description = description
        self.exclude = exclude
        self.include = include
        self.const = const
        self.gt = gt
        self.ge = ge
        self.lt = lt
        self.le = le
        self.multiple_of = multiple_of
        self.allow_inf_nan = allow_inf_nan
        self.max_digits = max_digits
        self.decimal_places = decimal_places
        self.min_items = min_items
        self.max_items = max_items
        self.unique_items = unique_items
        self.min_length = min_length
        self.max_length = max_length
        self.allow_mutation = allow_mutation
        self.regex = regex
        self.discriminator = discriminator
        self.extra = extra

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
                if key in DataclassField.__init__.__code__.co_varnames
            }
        )

        for k, v in extra.items():
            setattr(self, k, v)

    def __repr__(self):
        """Repr Field method.

        :return: Field repr
        """
        return (
            f"{DataclassField.__repr__(self)[:-1]}, "
            f"validator={self.validator!r}, "
            f"ignore={self.ignore!r}, "
            f"alias={self.alias!r}, "
            f"title={self.title!r}, "
            f"description={self.description!r}, "
            f"exclude={self.exclude!r}, "
            f"include={self.include!r}, "
            f"const={self.const!r}, "
            f"gt={self.gt!r}, "
            f"ge={self.ge!r}, "
            f"lt={self.lt!r}, "
            f"le={self.le!r}, "
            f"multiple_of={self.multiple_of!r}, "
            f"allow_inf_nan={self.allow_inf_nan!r}, "
            f"max_digits={self.max_digits!r}, "
            f"decimal_places={self.decimal_places!r}, "
            f"min_items={self.min_items!r}, "
            f"max_items={self.max_items!r}, "
            f"unique_items={self.unique_items!r}, "
            f"min_length={self.min_length!r}, "
            f"max_length={self.max_length!r}, "
            f"allow_mutation={self.allow_mutation!r}, "
            f"regex={self.regex!r}, "
            f"discriminator={self.discriminator!r})"
        )


def field(
    *,
    default: Union[_MISSING_TYPE, Any] = MISSING,
    default_factory: Union[_MISSING_TYPE, _WithoutDefault, Callable[..., Any]] = MISSING,
    init: Optional[bool] = True,
    repr: Optional[bool] = True,
    hash: Optional[Union[bool, _MISSING_TYPE]] = None,
    compare: Optional[bool] = True,
    metadata: Optional[bool] = None,
    kw_only: Union[_MISSING_TYPE, bool] = MISSING,
    validator: Optional[Union[Callable[[str], Any], _MISSING_TYPE]] = MISSING,
    alias: Optional[Union[List[str], str]] = None,
    ignore: Optional[bool] = False,
    title: Optional[str] = None,
    description: Optional[str] = None,
    exclude: Optional[Union[str, List[str]]] = None,
    include: Optional[Union[str, List[str]]] = None,
    const: Optional[bool] = None,
    gt: Optional[Union[int, float]] = None,
    ge: Optional[Union[int, float]] = None,
    lt: Optional[Union[int, float]] = None,
    le: Optional[Union[int, float]] = None,
    multiple_of: Optional[Union[int, float]] = None,
    allow_inf_nan: Optional[bool] = True,
    max_digits: Optional[int] = None,
    decimal_places: Optional[int] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: Optional[bool] = True,
    regex: Optional[str] = None,
    discriminator: Optional[str] = None,
    no_default: bool = False,
    **extra: Any,
) -> Union[DataclassField, Any]:
    """This function is used instead of exposing Field creation directly.

    So that a type checker can be told (via overloads) that this is a function whose type depends on its parameters.
    This function is used instead of exposing Field creation directly,
    so that a type checker can be told (via overloads) that this is a
    function whose type depends on its parameters.

    :param default: Default value for field.
    :param default_factory: Default factory for field.
    :param init: Field will be included in __init__ method.
    :param repr: Field will be included in __repr__ method.
    :param hash: Field will be included in __hash__ method.
    :param compare: Field will be included in __eq__ method.
    :param metadata: Field will be included in metadata.
    :param kw_only: Field will be included in __init__ method as keyword only.
    :param validator: Validator for field.
    :param alias: Aliases for config data (will be used to read from config files).
    :param ignore: Field will be ignored when writing to_ini etc.
    :param title: Can be any string, used in the schema.
    :param description: can be any string, used in the schema.
    :param exclude: exclude this field while dumping. Takes same values as
            the ``include`` and ``exclude`` arguments on the ``.dict`` method.
    :param include: include this field while dumping. Takes same values as the
            ``include`` and ``exclude`` arguments on the ``.dict`` method.
    :param const: this field is required and *must* take it's default value
    :param gt: only applies to numbers, requires the field to be "greater than".
            The schema will have an ``exclusiveMinimum`` validation keyword
    :param ge: only applies to numbers, requires the field to be "greater than or equal to".
            The schema will have a ``minimum`` validation keyword
    :param lt: only applies to numbers, requires the field to be "less than".
            The schema will have an ``exclusiveMaximum`` validation keyword
    :param le: only applies to numbers, requires the field to be "less than or equal to".
            The schema will have a ``maximum`` validation keyword
    :param multiple_of: only applies to numbers, requires the field to be "a multiple of".
            The schema will have a ``multipleOf`` validation keyword
    :param allow_inf_nan: only applies to numbers, allows the field to be NaN or infinity (+inf or -inf),
            which is a valid Python float. Default True, set to False for compatibility with JSON.
    :param max_digits: only applies to Decimals, requires the field to have a maximum number of digits
            within the decimal. It does not include a zero before the decimal point or trailing decimal zeroes.
    :param decimal_places: only applies to Decimals, requires the field to have at most a number of
            decimal places allowed. It does not include trailing decimal zeroes.
    :param min_items: only applies to lists, requires the field to have a minimum number of elements.
            The schema will have a ``minItems`` validation keyword
    :param max_items: only applies to lists, requires the field to have a maximum number of elements.
            The schema will have a ``maxItems`` validation keyword
    :param unique_items: only applies to lists, requires the field not to have duplicated elements.
            The schema will have a ``uniqueItems`` validation keyword
    :param min_length: only applies to strings, requires the field to have a minimum length.
            The schema will have a ``minLength`` validation keyword
    :param max_length: only applies to strings, requires the field to have a maximum length.
            The schema will have a ``maxLength`` validation keyword
    :param allow_mutation: a boolean which defaults to True. When False, the field raises a TypeError if
            the field is assigned on an instance.  The BaseModel Config must set validate_assignment to True
    :param regex: only applies to strings, requires the field match against a regular expression pattern string.
            The schema will have a ``pattern`` validation keyword
    :param discriminator: only useful with a (discriminated a.k.a. tagged) `Union` of sub models with a common field.
            The `discriminator` is the name of this common field to shorten validation and improve generated schema
    :param repr: show this field in the representation
    :param no_default: if True, the field will not have a default value, even if a default value is specified
    :param extra: any additional keyword arguments will be added as is to the schema

    :return: A dataclass field.
    :raises ValueError: if both default and default_factory are specified.
    """
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("cannot specify both default and default_factory")

    if default is MISSING and default_factory is MISSING and no_default:
        default_factory = WITHOUT_DEFAULT
    new_field = Field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        kw_only=kw_only,
        validator=validator,
        alias=alias,
        ignore=ignore,
        title=title,
        description=description,
        exclude=exclude,
        include=include,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_items=min_items,
        max_items=max_items,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        discriminator=discriminator,
        **extra,
    )
    return new_field
