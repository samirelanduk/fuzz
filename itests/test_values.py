from unittest import TestCase
from fuzz.values import Value

class ValueTest(TestCase):

    def test_can_combine_values(self):
        # Values can be added
        value1 = Value(4, 5)
        value2 = Value(9.2, 1)
        sum_ = value1 + value2
        self.assertEqual(sum_.value(), 13.2)
        self.assertAlmostEqual(sum_.error(), 5.1, delta=0.05)

        # Values can be subtracted
        value1 = Value(2, 0.03)
        value2 = Value(0.88, 0.04)
        difference = value1 - value2
        self.assertEqual(difference.value(), 1.12)
        self.assertAlmostEqual(difference.error(), 0.05, delta=0.05)

        # Values can be multiplied
        value1 = Value(49.52, 0.08)
        value2 = Value(189.53, 0.05)
        product = value1 * value2
        self.assertEqual(product.value(), 9385.5256)
        self.assertAlmostEqual(product.error(), 15.36, delta=0.005)

        # Values can be divided
        value1 = Value(120, 3)
        value2 = Value(20, 1.2)
        quotient = value1 / value2
        self.assertEqual(quotient.value(), 6)
        self.assertAlmostEqual(quotient.error(), 0.39, delta=0.005)

        # Values can be raised to a power
        value1 = Value(5.75, 0.08)
        power = value1 ** 3
        self.assertEqual(power.value(), 190.1)
        self.assertAlmostEqual(power.error(), 7.93, delta=0.005)

        # Values can be combined with constants
        value1 = Value(3.8, 0.3)
        quotient = value1 / 9.81
        self.assertEqual(quotient.value(), 0.387)
        self.assertAlmostEqual(quotient.error(), 0.0306, delta=0.0005)
        sum_ = value1 + 100
        self.assertEqual(sum_.value(), 103.8)
        self.assertEqual(sum_.error(), 0.3)


    def test_can_compare_values(self):
        # Equality
        self.assertEqual(Value(2, 1), Value(2, 0.1))
        self.assertNotEqual(Value(1, 0.4), Value(2, 0.4))

        # Greater
        self.assertGreater(Value(4, 3), Value(3.5, 2))
        self.assertGreaterEqual(Value(4, 3), Value(4, 2))

        # Less
        self.assertLess(Value(3.5, 3), Value(4, 2))
        self.assertLessEqual(Value(4, 3), Value(4, 2))

        # Consistency
        self.assertTrue(Value(3, 0.4).consistent_with(Value(3.4, 0.01)))
        self.assertTrue(Value(3, 0.4).consistent_with(3.4))
        self.assertFalse(Value(3, 0.39).consistent_with(Value(3.4, 0.01)))
        self.assertFalse(Value(3, 0.39).consistent_with(3.4))
