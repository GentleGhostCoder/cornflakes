# Mapping
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union
from uuid import UUID


class SQLTypes(Enum):
    """SQL types for SQLite3."""

    null = "NULL"
    integer = "INTEGER"
    real = "REAL"
    text = "TEXT"
    blob = "BLOB"
    timestamp = "TIMESTAMP"
    date = "DATE"
    time = "TIME"
    numeric = "NUMERIC"
    json = "JSON"
    primary_key = "PRIMARY KEY"
    autoincrement = "AUTOINCREMENT"
    foreign_key = "FOREIGN KEY"
    unique_not_null = "NOT NULL UNIQUE"
    unique = "UNIQUE"


SQL_TYPE_MAPPING = [
    {
        None: SQLTypes.null,
        type(None): SQLTypes.null,
        int: SQLTypes.integer,
        float: SQLTypes.real,
        str: SQLTypes.text,
        bytes: SQLTypes.blob,
        bool: SQLTypes.integer,
        datetime: SQLTypes.timestamp,
        date: SQLTypes.date,
        time: SQLTypes.time,
        Decimal: SQLTypes.numeric,
        tuple: SQLTypes.json,
        Tuple: SQLTypes.json,
        list: SQLTypes.json,
        List: SQLTypes.json,
        dict: SQLTypes.json,
        Dict: SQLTypes.json,
        IPv4Address: SQLTypes.text,
        IPv6Address: SQLTypes.text,
        Enum: SQLTypes.text,
        Generator: SQLTypes.blob,
        Any: SQLTypes.blob,
        Type: SQLTypes.text,
        Callable: SQLTypes.blob,
        Optional: SQLTypes.blob,
        Union: SQLTypes.blob,
        UUID: SQLTypes.text,
    }
]
