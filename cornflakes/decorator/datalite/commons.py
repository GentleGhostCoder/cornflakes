from dataclasses import Field
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
import json
import pickle
import sqlite3 as sql
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union
from uuid import UUID

from cornflakes.decorator.dataclass.helper import dataclass_fields
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


def generator_formatter(x: "Generator") -> None:
    raise ValueError("Generators cannot be serialized to SQLite")


SpecialForm = type(Optional)


type_table: Dict[Optional[type], str] = {
    None: "NULL",
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
    List: "TEXT",
    Dict: "TEXT",
    Tuple: "TEXT",
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
    UUID: "BLOB",
}

type_table.update(
    {
        Unique[key]
        if not isinstance(key, SpecialForm)
        else Unique[getattr(key, "__args__", type(None))]: f"{value}"
        + (" NOT NULL UNIQUE" if not isinstance(key, SpecialForm) else "")
        for key, value in type_table.items()
    }
)

validator_table: Dict[str, Optional[type]] = {
    "NULL": type(None),
    "INTEGER": int,
    "REAL": float,
    "TEXT": str,
    "BLOB": lambda x: bytes(x) if isinstance(x, (bytes, bytearray)) else x,
    "TIMESTAMP": lambda x: isinstance(x, datetime) and str(x) or "NULL",
    "DATE": lambda x: isinstance(x, date) and str(x) or "NULL",
    "TIME": lambda x: isinstance(x, time) and str(x) or "NULL",
    "NUMERIC": Decimal,
}
# additional validators
validator_table.update(
    {
        "IPv4Address": IPv4Address,
        "IPv6Address": IPv6Address,
        "Enum": Enum,
        "slice": slice,
        "UUID": UUID,
    }
)

formatter_table: Dict[type, Callable[[...], Any]] = {
    int: int,
    float: float,
    str: str,
    bytes: bytes,
    type(None): lambda x: None,
    bool: lambda x: int(x),
    UUID: lambda x: x.bytes,
    # additional formatters
    List: lambda x: json.dumps(x),
    Dict: lambda x: json.dumps(x),
    Tuple: lambda x: json.dumps(x),
    IPv4Address: str,
    IPv6Address: str,
    Enum: lambda x: x.value,
    complex: lambda x: str(x),
    set: lambda x: json.dumps(list(x)),
    frozenset: lambda x: json.dumps(list(x)),
    bytearray: bytes,
    memoryview: bytes,
    slice: lambda x: f"{x.start}:{x.stop}:{x.step}",
    range: lambda x: f"{x.start}:{x.stop}:{x.step}",
    classmethod: lambda x: str(x),
    Any: lambda x: pickle.dumps(x),
    Type: lambda x: x.__name__,
    Callable: lambda x: pickle.dumps(x),
    Generator: lambda x: json.dumps(list(x)),
    Optional: lambda x: pickle.dumps(x),
    Union: lambda x: pickle.dumps(x),
}


def _convert_type(type_: Optional[type], type_overload: Dict[Optional[type], str]) -> str:
    """
    Given a Python type, return the str name of its
    SQLlite equivalent.
    :param type_: A Python type, or None.
    :param type_overload: A type table to overload the custom type table.
    :return: The str name of the sql type.
    >>> _convert_type(int)
    "INTEGER"
    """
    try:
        return type_overload[type_]
    except KeyError:
        raise TypeError("Requested type not in the default or overloaded type table.")


def _convert_sql_format(value: Any, db_type: str = None) -> str:
    """
    Given a Python value, convert to string representation
    of the equivalent SQL datatype.
    :param value: A value, ie: a literal, a variable etc.
    :return: The string representation of the SQL equivalent.
    >>> _convert_sql_format(1)
    "1"
    >>> _convert_sql_format("John Smith")
    '"John Smith"'
    """
    if type(value) in formatter_table:
        value = formatter_table[type(value)](value)
    if db_type and db_type in validator_table:
        value = validator_table[db_type](value)
    if value is None:
        return "NULL"
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bytes):
        return '"' + str(value).replace("b'", "")[:-1] + '"'
    else:
        return str(value)


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
        return f" DEFAULT {_convert_sql_format(default_object, db_type)}"
    return ""


def _create_table(class_: type, cursor: sql.Cursor, type_overload: Dict[Optional[type], str] = None) -> None:
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
