from unittest import TestCase
from fuzz.values import Value

class ValueCreationTests(TestCase):

    def test_can_create_simple_value(self):
        val = Value(10)
        self.assertEqual(val._value, 10)
        self.assertEqual(val._error, 0)


    def test_can_create_value_with_uncertainty(self):
        val = Value(10, 1.5)
        self.assertEqual(val._value, 10)
        self.assertEqual(val._error, 1.5)


    def test_value_requires_numbers(self):
        Value(23)
        Value(23.5)
        with self.assertRaises(TypeError):
            Value("100")
        with self.assertRaises(TypeError):
            Value(True)


    def test_error_requires_numbers(self):
        Value(23, 1)
        Value(23, 0.5)
        with self.assertRaises(TypeError):
            Value(23, "100")
        with self.assertRaises(TypeError):
            Value(23, True)


    def test_error_must_be_positive(self):
        with self.assertRaises(ValueError):
            Value(23, -0.01)



class ValueSafeCreateTests(TestCase):

    def test_can_get_simple_value_safely(self):
        val = Value.create(10)
        self.assertIsInstance(val, Value)
        self.assertEqual(val._value, 10)
        self.assertEqual(val._error, 0)


    def test_can_get_error_value_safely(self):
        val = Value.create(10.5, 0.2)
        self.assertIsInstance(val, Value)
        self.assertEqual(val._value, 10.5)
        self.assertEqual(val._error, 0.2)


    def test_can_ignore_non_numbers(self):
        s = "value"
        val = Value.create(s, 0.2)
        self.assertIs(val, s)
