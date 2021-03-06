from unittest import TestCase
from unittest.mock import Mock, patch
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


    def test_can_create_value_from_value(self):
        value = Mock(Value)
        value._value = 10
        value._error = 2
        val = Value(value)
        self.assertEqual(val._value, 10)
        self.assertEqual(val._error, 0)


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



class ValueReprTests(TestCase):

    def test_repr_with_no_error(self):
        val = Value(23)
        self.assertEqual(str(val), '23')


    def test_repr_with_error(self):
        val = Value(23, 0.5)
        self.assertEqual(str(val), '23 ± 0.5')



class ValueAdditionTests(TestCase):

    def test_can_add_values(self):
        val1 = Value(23, 5)
        val2 = Value(19, 1)
        val3 = val1 + val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 42)
        self.assertAlmostEqual(val3._error, 5.1, delta=0.05)


    def test_can_add_value_to_number(self):
        val1 = Value(23, 0.5)
        val2 = 19.0
        val3 = val1 + val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 42)
        self.assertEqual(val3._error, 0.5)


    def test_can_add_number_to_value(self):
        val1 = 23
        val2 = Value(19, 0.4)
        val3 = val1 + val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 42)
        self.assertEqual(val3._error, 0.4)



class ValueSubtractionTests(TestCase):

    def test_can_subtract_values(self):
        val1 = Value(23, 5)
        val2 = Value(19, 1)
        val3 = val1 - val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 4)
        self.assertAlmostEqual(val3._error, 5.1, delta=0.05)


    def test_can_subtract_value_from_number(self):
        val1 = Value(23, 0.5)
        val2 = 19.0
        val3 = val2 - val1
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, -4)
        self.assertEqual(val3._error, 0.5)


    def test_can_subtract_number_from_value(self):
        val1 = 23
        val2 = Value(19, 0.4)
        val3 = val2 - val1
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, -4)
        self.assertEqual(val3._error, 0.4)



class ValueMultiplicationTests(TestCase):

    @patch("fuzz.values.Value.relative_error")
    def test_can_multiply_values(self, mock_err):
        mock_err.side_effect = (0.025, 0.06)
        val1 = Value(2, 0.08)
        val2 = Value(3, 0.05)
        val3 = val1 * val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 6)
        self.assertAlmostEqual(val3._error, 0.39)


    @patch("fuzz.values.Value.relative_error")
    def test_can_multiply_value_with_number(self, mock_err):
        mock_err.return_value = 0.025
        val1 = Value(2, 0.08)
        val2 = 3
        val3 = val1 * val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 6)
        self.assertAlmostEqual(val3._error, 0.15)


    @patch("fuzz.values.Value.relative_error")
    def test_can_multiply_number_with_value(self, mock_err):
        mock_err.return_value = 0.06
        val1 = 2
        val2 = Value(3, 0.05)
        val3 = val1 * val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 6)
        self.assertAlmostEqual(val3._error, 0.36)


    @patch("fuzz.values.Value.relative_error")
    def test_can_multiply_negative_values(self, mock_err):
        mock_err.side_effect = (0.025, 0.06)
        val1 = Value(-2, 0.08)
        val2 = Value(3, 0.05)
        val3 = val1 * val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, -6)
        self.assertAlmostEqual(val3._error, 0.39)



class ValueDivisionTests(TestCase):

    @patch("fuzz.values.Value.relative_error")
    def test_can_divide_values(self, mock_err):
        mock_err.side_effect = (4, 3)
        val1 = Value(12, 48)
        val2 = Value(4, 12)
        val3 = val1 / val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 3)
        self.assertEqual(val3._error, 15)


    @patch("fuzz.values.Value.relative_error")
    def test_can_divide_value_by_number(self, mock_err):
        mock_err.return_value = 0.025
        val1 = Value(12, 48)
        val2 = 4.0
        val3 = val1 / val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 3)
        self.assertAlmostEqual(val3._error, 0.075, delta=0.000005)


    @patch("fuzz.values.Value.relative_error")
    def test_can_divide_number_by_value(self, mock_err):
        mock_err.return_value = 0.06
        val1 = 12
        val2 = Value(4, 12)
        val3 = val1 / val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 3)
        self.assertAlmostEqual(val3._error, 0.18, delta=0.000005)


    @patch("fuzz.values.Value.relative_error")
    def test_can_divide_negative_values(self, mock_err):
        mock_err.side_effect = (4, 3)
        val1 = Value(12, 48)
        val2 = Value(-4, 12)
        val3 = val1 / val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, -3)
        self.assertEqual(val3._error, 15)



class ValuePowerTests(TestCase):

    @patch("fuzz.values.Value.relative_error")
    def test_can_raise_value_to_power(self, mock_err):
        mock_err.return_value = 0.01
        val1 = Value(2, 0.02)
        val2 = 3
        val3 = val1 ** val2
        self.assertIsInstance(val3, Value)
        self.assertEqual(val3._value, 8)
        self.assertEqual(val3._error, 0.24)


    @patch("fuzz.values.Value.relative_error")
    def test_can_raise_negative_value_to_power(self, mock_err):
        mock_err.return_value = 0.01
        val1 = Value(-2, 0.02)
        val = val1 ** 2
        self.assertIsInstance(val, Value)
        self.assertEqual(val._value, 4)
        self.assertEqual(val._error, 0.08)
        val = val1 ** 3
        self.assertIsInstance(val, Value)
        self.assertEqual(val._value, -8)
        self.assertEqual(val._error, 0.24)


    @patch("fuzz.values.Value.relative_error")
    def test_can_raise_value_to_negative_power(self, mock_err):
        mock_err.return_value = 0.01
        val1 = Value(2, 0.02)
        val = val1 ** -2
        self.assertIsInstance(val, Value)
        self.assertEqual(val._value, 0.25)
        self.assertEqual(val._error, 0.005)



class ValueEqualityTests(TestCase):

    def test_values_equal(self):
        val1 = Value(19, 0.4)
        val2 = Value(19, 0.5)
        val3 = Value(23, 0.5)
        self.assertEqual(val1, val2)
        self.assertNotEqual(val1, val3)


    def test_value_number_equality(self):
        val1 = Value(19, 0.4)
        val2 = 19.0
        val3 = 23
        self.assertEqual(val1, val2)
        self.assertNotEqual(val1, val3)


    def test_number_value_equality(self):
        val1 = 19
        val2 = Value(19.0, 0.5)
        val3 = Value(23, 0.5)
        self.assertEqual(val1, val2)
        self.assertNotEqual(val1, val3)



class ValueGreaterTests(TestCase):

    def test_value_greater_than_value(self):
        val1 = Value(19, 0.4)
        val2 = Value(23, 0.5)
        self.assertTrue(val2 > val1)
        self.assertTrue(val1 < val2)


    def test_value_greater_than_number(self):
        val1 = 19
        val2 = Value(23, 0.5)
        self.assertTrue(val2 > val1)
        self.assertTrue(val1 < val2)


    def test_number_greater_than_value(self):
        val1 = Value(19, 0.4)
        val2 = 23
        self.assertTrue(val2 > val1)
        self.assertTrue(val1 < val2)



class ValueGreaterEqualTests(TestCase):

    def test_value_greater_equal_than_value(self):
        val1 = Value(19, 0.4)
        val2 = Value(19, 0.5)
        val3 = Value(17, 0.5)
        self.assertTrue(val2 >= val1)
        self.assertTrue(val1 <= val2)
        self.assertTrue(val2 >= val3)


    def test_value_greater_equal_than_number(self):
        val1 = 19
        val2 = Value(19, 0.5)
        self.assertTrue(val2 >= val1)
        self.assertTrue(val1 <= val2)


    def test_number_greater_equal_than_value(self):
        val1 = Value(19, 0.4)
        val2 = 19
        self.assertTrue(val2 >= val1)
        self.assertTrue(val1 <= val2)


class ValueValueTests(TestCase):

    def test_can_get_value(self):
        val = Value(23, 0.5)
        self.assertIs(val.value(), val._value)



class ValueErrorTests(TestCase):

    def test_can_get_error(self):
        val = Value(23, 0.5)
        self.assertIs(val.error(), val._error)



class ValueRelativeErrorTests(TestCase):

    def test_can_get_relative_error(self):
        val = Value(100, 2)
        self.assertEqual(val.relative_error(), 0.02)


    def test_can_get_relative_error_when_value_is_zero(self):
        val = Value(0, 2)
        self.assertEqual(val.relative_error(), 0)


    def test_can_get_relative_error_when_value_is_negative(self):
        val = Value(-100, 2)
        self.assertEqual(val.relative_error(), 0.02)



class ValueErrorRangeTest(TestCase):

    def test_can_get_error_range(self):
        val = Value(100, 2)
        self.assertEqual(val.error_range(), (98, 102))



class ValueConsistencyTests(TestCase):

    def test_can_get_consistent_results(self):
        val1 = Value(3.3, 0.2)
        val2 = Mock(Value)
        val2.value.return_value = 3.1
        val2.error.return_value = 0.1
        self.assertTrue(val1.consistent_with(val2))


    def test_can_get_inconsistent_results(self):
        val1 = Value(3.30001, 0.2)
        val2 = Mock(Value)
        val2.value.return_value = 3.0
        val2.error.return_value = 0.1
        self.assertFalse(val1.consistent_with(val2))


    def test_can_get_consistency_with_non_value(self):
        val1 = Value(9.87, 0.09)
        val2 = 9.81
        self.assertTrue(val1.consistent_with(val2))
        val2 = 9.78
        self.assertTrue(val1.consistent_with(val2))
        val2 = 9.7799
        self.assertFalse(val1.consistent_with(val2))


    def test_cannot_get_consistency_with_non_number(self):
        val1 = Value(9.87, 0.09)
        with self.assertRaises(TypeError):
            val1.consistent_with("value")
