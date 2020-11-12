from coercion.infer_schema import infer_schema
import unittest


class test_infer_schema(unittest.TestCase):
    def test_null(self):
        inpt = {}
        gold = {}
        output = infer_schema(inpt)
        self.assertEqual(gold, output)

    def test_simple(self):
        inpt = {"foo": 1}
        gold = {"foo": int}
        output = infer_schema(inpt)
        self.assertEqual(gold, output)

    def test_nested(self):
        inpt = {"foo": {"bar": 3.14}}
        gold = {"foo": {"bar": float}}
        output = infer_schema(inpt)
        self.assertEqual(gold, output)

    def test_primitive_list(self):
        inpt = {"foo": [1, 2, 3]}
        gold = {"foo": [int]}
        output = infer_schema(inpt)
        self.assertEqual(gold, output)

    def test_dict_list(self):
        inpt = {"foo": [{"foo": 1}, {"bar": 3.14}]}
        gold = {"foo": [{"foo": int, "bar": float}]}
        output = infer_schema(inpt)
        self.assertEqual(gold, output)

    def test_list_list(self):
        inpt = {"foo": [[1, 2], [3, 4]]}
        gold = {"foo": [[int]]}
        output = infer_schema(inpt)
        self.assertEqual(gold, output)

    def test_set(self):
        inpt = {"foo": {1, 2, 3}}
        gold = {"foo": {int}}
        output = infer_schema(inpt)
        self.assertEqual(gold, output)

    def test_set_list(self):
        inpt = {"foo": [{1, 2, 3}]}
        gold = {"foo": [{int}]}
        output = infer_schema(inpt)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
