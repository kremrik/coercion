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


def coerce(
    schema: dict,
    record: dict,
    defaults: Optional[dict] = None,
) -> dict:
    """
    Examples:
        .. highlight:: python
        .. code-block:: python

            >>> from coercion import coerce

            >>> schema = {"foo": float, "bar": str}
            >>> record = {"foo": 1, "baz": 3.14}

            >>> coerce(schema, record)
            {'foo': 1.0, 'bar': None}

            # you can change the default type like:
            >>> coerce(schema, record, {str: ""})
            {'foo': 1.0, 'bar': ''}

    Args:
        schema: A Python dict defining a schema
        record: A Python dict to coerce
        defaults: An optional dict mapping primitive types
            to their preferred default values

    Returns:
        A Python dict in the shape of `schema`
    """
    if defaults is None:
        defaults = {}

    try:
        extras = deep_diff(record, schema)
        trimmed = deep_cut(extras, record)
        return deep_put(defaults, schema, trimmed)
    except Exception as e:
        msg = _unwind_exception(e.args)
        raise type(e)(msg)


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
def deep_put(defaults: dict, d1: dict, d2: dict) -> dict:
    return put_(
        d1=d1,
        d2=d2,
        on_missing=partial(_put_on_missing, defaults),
        on_match=_put_on_match,
        list_strategy=partial(
            _put_list_strategy, defaults
        ),
    )


def _put_on_missing(
    defaults: dict, schema_val: type
) -> Any:
    _defaults = {**DEFAULTS, **defaults}
    return _schema_to_defaults(_defaults, schema_val)


def _put_on_match(
    schema_val: type, record_val: Any
) -> Any:
    return schema_val(record_val)


def _put_list_strategy(
    defaults: dict,
    schema_val: List[Any],
    record_val: List[Any],
) -> List[Any]:
    if isinstance(schema_val, set):
        schema_val = deepcopy(schema_val)
        inner = schema_val.pop()
    else:
        inner = schema_val[0]

    if not isinstance(inner, dict):
        fnc = lambda x: inner(x)
    else:
        _put = partial(deep_put, defaults, inner)
        fnc = lambda x: _put(x)

    return type(schema_val)(map(fnc, record_val))


# ---------------------------------------------------------
def _unwind_exception(e_args: tuple) -> str:
    if len(e_args) == 1:
        return str(e_args[0])
    if not isinstance(e_args[1], tuple):
        return f"{e_args[0]}: {e_args[1]}"
    if len(e_args[1]) <= 1:
        return f"{e_args[0]}: {e_args[1][0]}"
    return (
        e_args[0] + " -> " + _unwind_exception(e_args[1])
    )


def _schema_to_defaults(defaults: dict, obj: Any) -> Any:
    if obj in list(defaults.keys()):
        return defaults.get(obj)

    fnc = partial(_schema_to_defaults, defaults)

    if type(obj) in (set, list, tuple):
        return (
            type(obj)(map(lambda x: fnc(x), obj))
            if isinstance(obj, dict)
            else []
        )

    return dict(
        zip(
            obj.keys(), map(lambda x: fnc(x), obj.values())
        )
    )
