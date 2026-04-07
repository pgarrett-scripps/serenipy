"""Shared serialization utilities for converting values to/from string representations."""

from typing import Any, Callable


def serialize_val(val: Any, precision=None) -> str:
    """Convert a value to its string representation for file serialization.

    Args:
        val: The value to serialize. None is serialized as "NA".
        precision: Optional number of decimal places for rounding floats.

    Returns:
        String representation of the value.
    """
    if val is None:
        return "NA"
    if precision is None:
        return str(val)
    return str(round(val, precision))


def deserialize_val(val: str, f: Callable) -> Any:
    """Parse a string value using the provided callable, treating "NA" as None.

    Args:
        val: The string value to deserialize.
        f: A callable to convert the string (e.g., int, float, str).

    Returns:
        The converted value, or None if val is "NA".
    """
    if val == "NA":
        return None
    return f(val)
