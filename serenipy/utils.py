from typing import Callable


def serialize_val(val: any, precision=None):
    if val is None:
        return 'NA'
    if precision is None:
        return str(val)
    return str(round(val, precision))


def deserialize_val(val: str, f: Callable):
    if val == 'NA':
        return None
    return f(val)
