import unittest

from serenipy.utils import deserialize_val, serialize_val


class TestUtils(unittest.TestCase):
    def test_serialize_val_none(self):
        self.assertEqual(serialize_val(None), "NA")

    def test_serialize_val_string(self):
        self.assertEqual(serialize_val("hello"), "hello")

    def test_serialize_val_int(self):
        self.assertEqual(serialize_val(42), "42")

    def test_serialize_val_float(self):
        self.assertEqual(serialize_val(3.14159), "3.14159")

    def test_serialize_val_float_precision(self):
        self.assertEqual(serialize_val(3.14159, 2), "3.14")
        self.assertEqual(serialize_val(3.14159, 4), "3.1416")
        self.assertEqual(serialize_val(1.0, 0), "1.0")

    def test_serialize_val_none_with_precision(self):
        self.assertEqual(serialize_val(None, 2), "NA")

    def test_deserialize_val_na(self):
        self.assertIsNone(deserialize_val("NA", int))
        self.assertIsNone(deserialize_val("NA", float))
        self.assertIsNone(deserialize_val("NA", str))

    def test_deserialize_val_int(self):
        self.assertEqual(deserialize_val("42", int), 42)
        self.assertEqual(deserialize_val("-5", int), -5)

    def test_deserialize_val_float(self):
        self.assertAlmostEqual(deserialize_val("3.14", float), 3.14)
        self.assertAlmostEqual(deserialize_val("-0.5", float), -0.5)

    def test_deserialize_val_str(self):
        self.assertEqual(deserialize_val("hello", str), "hello")

    def test_deserialize_val_custom_callable(self):
        result = deserialize_val("[1]", lambda x: int(x.strip("[").strip("]")))
        self.assertEqual(result, 1)
