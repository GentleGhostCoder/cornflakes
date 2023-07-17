from dataclasses import Field
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from inspect import isclass
from ipaddress import IPv4Address, IPv6Address
import json
import pickle
import re
import sqlite3 as sql
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union
from uuid import UUID

from cornflakes.decorator.dataclasses import dataclass_fields
from cornflakes.decorator.datalite.constraints import Unique


def str_to_bool(s: str) -> bool:
    if s.lower() == "true":
        return True
    elif s.lower() == "false":
        return False
    else:
        raise ValueError("String does not represent a boolean value")


def default_formatter(x: Any) -> Any:
    return x


def uuid_formatter(x: UUID) -> bytes:
    return x.bytes


def generator_formatter(_: "Generator") -> None:
    raise ValueError("Generators cannot be serialized to SQLite")


SpecialForm = type(Optional)

type_table: Dict[Union[Optional[type], Any], str] = {
    None: "NULL",
    type(None): "NULL",
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    bytes: "BLOB",
    bool: "INTEGER",
    datetime: "TIMESTAMP",
    date: "DATE",
    time: "TIME",
    Decimal: "NUMERIC",
    # additional types
    tuple: "JSON",
    Tuple: "JSON",
    list: "JSON",
    List: "JSON",
    dict: "JSON",
    Dict: "JSON",
    IPv4Address: "TEXT",
    IPv6Address: "TEXT",
    Enum: "TEXT",
    complex: "TEXT",
    set: "TEXT",
    frozenset: "TEXT",
    bytearray: "BLOB",
    memoryview: "BLOB",
    slice: "TEXT",
    range: "TEXT",
    classmethod: "BLOB",
    Any: "BLOB",
    Type: "TEXT",
    Callable: "BLOB",
    Generator: "TEXT",
    Optional: "BLOB",
    Union: "BLOB",
    UUID: "TEXT",
}

type_table.update(
    {
        Unique[getattr(key, "__args__", type(None))]  # type: ignore
        if isinstance(key, SpecialForm)
        else Unique[key]: f"{value}" + ("" if isinstance(key, SpecialForm) else " NOT NULL UNIQUE")  # type: ignore
        for key, value in type_table.items()
    }
)

validator_table: Dict[str, Union[Callable[[Any], Any], Type]] = {
    "NULL": type(None),
    "INTEGER": int,
    "REAL": float,
    "TEXT": str,
    "BLOB": lambda x: bytes(x) if isinstance(x, (bytes, bytearray)) else x,
    "TIMESTAMP": lambda x: isinstance(x, datetime) and str(x) or "NULL",
    "DATE": lambda x: isinstance(x, date) and str(x) or "NULL",
    "TIME": lambda x: isinstance(x, time) and str(x) or "NULL",
    "NUMERIC": lambda x: Decimal(str(x)),
}

formatter_table: Dict[Union[Type, Any], Any] = {
    int: str,
    float: str,
    Decimal: str,
    str: str,
    bytes: lambda x: re.sub('(^"|"$)', "", json.dumps(str(x)[2:-1])),
    type(None): lambda _: "",
    bool: lambda x: str(int(x)),
    UUID: str,
    # additional formatters
    tuple: lambda x: json.dumps(list(x)),
    Tuple: lambda x: json.dumps(list(x)),
    list: lambda x: json.dumps(x),
    List: lambda x: json.dumps(x),
    dict: lambda x: json.dumps(x),
    Dict: lambda x: json.dumps(x),
    datetime: lambda x: str(x),
    date: lambda x: str(x),
    time: lambda x: str(x),
    IPv4Address: lambda x: re.sub('(^"|"$)', "", json.dumps(str(x))),
    IPv6Address: lambda x: re.sub('(^"|"$)', "", json.dumps(str(x))),
    Enum: lambda x: re.sub('(^"|"$)', "", json.dumps(x.value)),
    complex: lambda x: re.sub('(^"|"$)', "", json.dumps(str(x))),
    set: lambda x: list(x),
    frozenset: lambda x: list(x),
    bytearray: lambda x: '"' + str(bytes(x)).replace("b'", "")[:-1] + '"',
    memoryview: lambda x: '"' + str(bytes(x)).replace("b'", "")[:-1] + '"',
    slice: lambda x: json.dumps(f"{x.start}:{x.stop}:{x.step}"),
    range: lambda x: json.dumps(f"{x.start}:{x.stop}:{x.step}"),
    classmethod: lambda x: str(x),
    Any: lambda x: pickle.dumps(x),
    Type: lambda x: json.dumps(x.__name__),
    Callable: lambda x: pickle.dumps(x),
    Generator: lambda x: list(x),
    Optional: lambda x: pickle.dumps(x),
    Union: lambda x: pickle.dumps(x),
}


def _convert_type(type_hint: Optional[type], type_overload: Optional[Dict[Optional[type], str]] = None) -> str:
    """
    Given a Python type, return the str name of its
    SQLlite equivalent.
    :param type_hint: A Python type, or None.
    :param type_overload: A type table to overload the custom type table.
    :return: The str name of the sql type.
    >>> _convert_type(int)
    'INTEGER'
    """
    if type_overload is None:
        type_overload = type_table
    try:
        actual_type: Any = getattr(type_hint, "__origin__", getattr(type_hint, "type", type_hint))
        if isinstance(actual_type, SpecialForm):
            actual_type = getattr(type_hint, "__args__", type_hint)
        if isclass(actual_type) and issubclass(actual_type, Enum):
            actual_type = Enum
        if isinstance(actual_type, list) or isinstance(actual_type, tuple):
            actual_type = next(item for item in actual_type if not isinstance(item, type(None)))
        return type_overload[actual_type]
    except KeyError:
        raise TypeError("Requested type not in the default or overloaded type table.")


def _validate_sql_type(value, db_type):
    """Validate and format value for insertion into SQLite."""
    if value is None:
        return ""
    return validator_table[db_type](value)


def _convert_sql_format(value: Any) -> Union[str, int]:
    """
    Given a Python value, convert to string representation
    of the equivalent SQL datatype.
    :param value: A value, ie: a literal, a variable etc.
    :return: The string representation of the SQL equivalent.
    >>> _convert_sql_format(1)
    '1'
    >>> _convert_sql_format("John Smith")
    'John Smith'
    """
    try:
        type_hint = type(value)
        actual_type: Any = getattr(type_hint, "__origin__", getattr(type_hint, "type", type_hint))
        if isinstance(actual_type, SpecialForm):
            actual_type = getattr(type_hint, "__args__", type_hint)
        if isclass(actual_type) and issubclass(actual_type, Enum):
            actual_type = Enum
        return formatter_table[actual_type](value)
    except KeyError:
        raise TypeError("Requested type not in the default or overloaded type table.")


def _get_table_cols(cur: sql.Cursor, table_name: str) -> List[str]:
    """
    Get the column data of a table.

    :param cur: Cursor in database.
    :param table_name: Name of the table.
    :return: the information about columns.
    """
    cur.execute(f"PRAGMA table_info({table_name});")
    return [row_info[1] for row_info in cur.fetchall()][1:]


def _get_default(default_object: object, type_overload: Dict[Optional[type], str], db_type: str) -> str:
    """
    Check if the field's default object is filled,
    if filled return the string to be put in the,
    database.
    :param default_object: The default field of the field.
    :param type_overload: Type overload table.
    :return: The string to be put on the table statement,
    empty string if no string is necessary.
    """
    if type(default_object) in type_overload:
        value = _convert_sql_format(_validate_sql_type(default_object, db_type))
        if db_type in ["TEXT", "DATE", "TIMESTAMP", "TIME"]:
            return f" DEFAULT '{value}'"
        return f" DEFAULT {value}"
    return ""


def _create_table(class_: type, cursor: sql.Cursor, type_overload: Optional[Dict[Optional[type], str]] = None) -> None:
    """
    Create the table for a specific dataclass given
    :param class_: A dataclass.
    :param cursor: Current cursor instance.
    :param type_overload: Overload the Python -> SQLDatatype table
    with a custom table, this is that custom table.
    :return: None.
    """
    if not type_overload:
        type_overload = type_table
    fields: List[Field] = [dataclass_fields(class_)[key] for key in dataclass_fields(class_).keys()]
    fields.sort(key=lambda field: field.name)  # Since dictionaries *may* be unsorted.
    sql_fields = ", ".join(
        f"{field.name} {_convert_type(field.type, type_overload)}"
        f"{_get_default(field.default, type_overload, _convert_type(field.type, type_overload))}"
        for field in fields
    )
    sql_fields = "obj_id INTEGER PRIMARY KEY AUTOINCREMENT, " + sql_fields
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {class_.__name__.lower()} ({sql_fields});")
