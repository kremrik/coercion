from map_ops.core import put_
from functools import partial
from typing import Any, List


DEFAULTS = {
    int: None,
    float: None,
    str: None,
    bytes: None,
    None: None,
}


def coerce(schema: dict, record: dict) -> dict:
    return deep_put(schema, record)


def deep_put(d1: dict, d2: dict) -> dict:
    return put_(
        d1=d1,
        d2=d2,
        on_missing=_on_missing,
        on_match=_on_match,
        list_strategy=_list_strategy,
    )


def _on_missing(schema_val: type) -> Any:
    return DEFAULTS.get(schema_val)


def _on_match(schema_val: type, record_val: Any) -> Any:
    return schema_val(record_val)


def _list_strategy(
    schema_val: List[Any], record_val: List[Any]
) -> List[Any]:
    if isinstance(schema_val, set):
        inner = schema_val.pop()
    else:
        inner = schema_val[0]

    if not isinstance(inner, dict):
        fnc = lambda x: inner(x)
    else:
        _put = partial(deep_put, inner)
        fnc = lambda x: _put(x)

    return type(schema_val)(map(fnc, record_val))
