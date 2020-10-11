from map_ops.core import cut_, diff_, put_
from copy import deepcopy
from functools import partial, reduce
from typing import Any, List, Optional


DEFAULTS = {
    int: None,
    float: None,
    str: None,
    bytes: None,
    None: None,
}


def coerce(schema: dict, record: dict) -> dict:
    """
    Examples:
        .. highlight:: python
        .. code-block:: python

            from coercion import coerce

            schema = {"foo": float, "bar": str}
            record = {"foo": 1, "bar": 3.14}

            coerce(schema, record)
            {'foo': 1.0, 'bar': '3.14'}

    Args:
        schema: A Python dict defining a schema
        record: A Python dict to coerce

    Returns:
        A Python dict in the shape of `schema`
    """
    extras = deep_diff(record, schema)
    trimmed = deep_cut(extras, record)
    return deep_put(schema, trimmed)


# ---------------------------------------------------------
def deep_diff(d1: dict, d2: dict) -> dict:
    return diff_(
        d1=d1, d2=d2, list_strategy=_diff_list_strategy
    )


def _diff_list_strategy(
    record_val: List[Any], schema_val: List[Any]
) -> Optional[List[Any]]:
    if isinstance(schema_val, set):
        schema_val = deepcopy(schema_val)
        inner = schema_val.pop()
    else:
        inner = schema_val[0]

    if not isinstance(inner, dict):
        return None

    superset = reduce(lambda x, y: put_(x, y), record_val)

    diff = type(schema_val)([diff_(superset, inner)])
    return diff


# ---------------------------------------------------------
def deep_cut(d1: dict, d2: dict) -> dict:
    return cut_(
        d1=d1, d2=d2, list_strategy=_cut_list_strategy
    )


def _cut_list_strategy(
    record_val: List[Any], schema_val: List[Any]
) -> List[Any]:
    if isinstance(schema_val, set):
        schema_val = deepcopy(schema_val)
        inner = schema_val.pop()
    else:
        inner = schema_val[0]

    if not isinstance(inner, dict):
        return record_val

    fnc = partial(cut_, inner)
    cut = type(schema_val)(map(fnc, record_val))
    return cut


# ---------------------------------------------------------
def deep_put(d1: dict, d2: dict) -> dict:
    return put_(
        d1=d1,
        d2=d2,
        on_missing=_put_on_missing,
        on_match=_put_on_match,
        list_strategy=_put_list_strategy,
    )


def _put_on_missing(schema_val: type) -> Any:
    return DEFAULTS.get(schema_val)


def _put_on_match(
    schema_val: type, record_val: Any
) -> Any:
    return schema_val(record_val)


def _put_list_strategy(
    schema_val: List[Any], record_val: List[Any]
) -> List[Any]:
    if isinstance(schema_val, set):
        schema_val = deepcopy(schema_val)
        inner = schema_val.pop()
    else:
        inner = schema_val[0]

    if not isinstance(inner, dict):
        fnc = lambda x: inner(x)
    else:
        _put = partial(deep_put, inner)
        fnc = lambda x: _put(x)

    return type(schema_val)(map(fnc, record_val))
