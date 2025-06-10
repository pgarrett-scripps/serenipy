from typing import Callable, Any


def serialize_val(val: Any, precision=None) -> str:
    if val is None:
        return "NA"
    if precision is None:
        return str(val)
    return str(round(val, precision))


def deserialize_val(val: str, f: Callable) -> Any:
    if val == "NA":
        return None
    return f(val)
