![](images/coercion.png)

# coercion
![Python package](https://github.com/kremrik/coercion/workflows/Python%20package/badge.svg)
![coverage](images/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### What is it?
A dead-simple, dictionary-based, schema framework for shaping and _coercing_
arbitrarily complex data

### What is it _not_?
A schema validatator. `coercion` makes every attempt to fill in the blanks and
cast your data to the appropriate types, but employs a "fail fast" approach to
exceptions and does not provide reporting.

### Why coercion?
Two reasons:
1. It's good to have a "gatekeeper" at the bounds of applications where data
may be missing fields, have messed up types, etc
1. `coercion` schemas are just Python - no DSL's, no custom objects, no serde;
if you know how to create a dictionary, you already know everything necessary

### Examples

##### Conform to a schema
```python
from coercion import coerce

# schemas are just dictionaries, with the types specified
# as regular python `type`s:
schema = {"foo": int, "bar": float}
record = {"foo": "1", "baz": "remove-me"}

coerce(schema, record)
{"foo": 1, "bar": None}

# you can alter the default value for missing keys too:
coerce(schema, record, {float: 0.0})
{"foo": 1, "bar": 0.0}
```

##### Operating on lists of dicts
```python
from coercion import coerce

schema = {
    "foo": [
        {"bar": str}
    ]
}
record = {
    "foo": [
        {"bar": 1},
        {"baz": "remove-me"},
        {"bar": "hi"}
    ]
}

coerce(schema, record)
{
    "foo": [
        {"bar": '1'},
        {"bar": None},
        {"bar": "hi"}
    ]
}
```

##### Operating with string representations
```python
from coercion import coerce

schema2 = {"foo": [float]}
record2 = {"foo": "[1, 2, 3]"}  # list is a string
coerce(schema2, record2)
{'foo': [1.0, 2.0, 3.0]}

schema3 = {"foo": {"bar": str}}
record3 = {"foo": '{"bar": 1}'}  # dict is a string
coerce(schema3, record3)
{'foo': {'bar': '1'}}
```

##### Error reporting
Debugging errors while parsing deeply-nested data structures can be a pain.
`coercion` makes this chore easier by providing a simple path on error:
```python
from coercion import coerce

schema = {"foo": {"bar": {"baz": float}}}
record = {"foo": {"bar": {"baz": "hi"}}}

coerce(schema, record)
...
ValueError: foo -> bar -> baz: could not convert string to float: 'hi'
```
