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
        gold = {"foo": 1}
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


if __name__ == "__main__":
    unittest.main()