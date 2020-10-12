from coercion.coercion import coerce
import unittest


class test_coerce(unittest.TestCase):
    def test_falsy_both(self):
        schema = {}
        record = {}
        gold = {}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_falsy_schema(self):
        schema = {}
        record = {"foo": 1}
        gold = {}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_falsy_record(self):
        schema = {"foo": int}
        record = {}
        gold = {"foo": None}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_no_change(self):
        schema = {"foo": str}
        record = {"foo": "hi"}
        gold = {"foo": "hi"}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_numeric_type_conflict(self):
        schema = {"foo": float}
        record = {"foo": 1}
        gold = {"foo": 1.0}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_nested(self):
        schema = {"foo": {"bar": str}}
        record = {"foo": {"bar": 1}}
        gold = {"foo": {"bar": "1"}}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_list_of_primitive(self):
        schema = {"foo": [float]}
        record = {"foo": [1, 2, 3]}
        gold = {"foo": [1.0, 2.0, 3.0]}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_set_of_primitive(self):
        schema = {"foo": {float}}
        record = {"foo": {1, 2, 3}}
        gold = {"foo": {1.0, 2.0, 3.0}}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_tuple_of_primitive(self):
        schema = {"foo": (float,)}
        record = {"foo": (1, 2, 3)}
        gold = {"foo": (1.0, 2.0, 3.0)}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_list_of_dicts(self):
        schema = {"foo": [{"bar": str}]}
        record = {"foo": [{"bar": 1.0}, {"bar": 2.0}]}
        gold = {"foo": [{"bar": "1.0"}, {"bar": "2.0"}]}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_removes_extra_key(self):
        schema = {"foo": int}
        record = {"foo": 1, "bar": 2}
        gold = {"foo": 1}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_removes_extra_nested_key(self):
        schema = {"foo": {"bar": int}}
        record = {"foo": {"bar": 1, "baz": 2}}
        gold = {"foo": {"bar": 1}}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_removes_extra_key_in_list(self):
        schema = {"foo": [{"bar": int}]}
        record = {"foo": [{"bar": 1, "baz": 2}]}
        gold = {"foo": [{"bar": 1}]}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_adds_missing_key(self):
        schema = {"foo": int, "bar": int}
        record = {"foo": 1}
        gold = {"foo": 1, "bar": None}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_adds_missing_nested_key(self):
        schema = {"foo": {"bar": int, "baz": int}}
        record = {"foo": {"bar": 1}}
        gold = {"foo": {"bar": 1, "baz": None}}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_adds_handles_single_extra_nested_key(self):
        schema = {"foo": {"bar": int}}
        record = {"foo": {"baz": 1}}
        gold = {"foo": {"bar": None}}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_adds_missing_key_in_list(self):
        schema = {"foo": [{"bar": int, "baz": int}]}
        record = {"foo": [{"bar": 1}]}
        gold = {"foo": [{"bar": 1, "baz": None}]}
        output = coerce(schema, record)
        self.assertEqual(gold, output)

    def test_specify_default_type(self):
        schema = {"foo": int}
        record = {}
        gold = {"foo": 0}
        output = coerce(schema, record, {int: 0})
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
