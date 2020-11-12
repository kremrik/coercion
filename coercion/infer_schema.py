from collections.abc import Iterable
from functools import reduce
from typing import Any


__all__ = ["infer_schema"]


def infer_schema(obj: Any) -> Any:
    # TODO: should have optional param for handling None

    if isinstance(obj, dict):
        return dict(
            zip(
                obj.keys(),
                map(
                    lambda x: infer_schema(x),
                    obj.values(),
                ),
            )
        )

    is_iter = isinstance(obj, Iterable)
    is_str = isinstance(obj, str)

    if is_iter and not is_str:
        inner = reduce(
            lambda x, y: _inner_type(x, y),
            map(lambda x: infer_schema(x), obj),
        )
        return type(obj)((inner,))

    return type(obj)


def _inner_type(obj1: Any, obj2: Any) -> Any:
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        return {**obj1, **obj2}

    if obj1 == obj2:
        return obj1
    else:
        msg = "List types '{}' and '{}' differ".format(
            obj1, obj2
        )
        raise TypeError(msg)
