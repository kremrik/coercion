# coercion
![](images/coercion.png)

### Why coercion?
Two reasons:
1. It's good to have a "gatekeeper" at the bounds of applications where data
may be missing fields, have messed up types, etc
1. `coercion` is pure Python - no DSL's, no custom objects, no serialization;
if you know how to create a dictionary, you already know how to use it

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
`coercion` is NOT a schema validator, and as such does not support any form of
violation/exception reporting. This means that in the event of an error, you
will see the first exception that `coerce` throws, but no more. There is
possible functionality in the works to facilitate this, but it's currently not
within the scope of the project.
