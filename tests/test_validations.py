from nasa import validations
from datetime import date
import random
import time
import unittest

class TestValidations(unittest.TestCase):
    def test_optional_validators(self):
        self.assertIsNone(validations.optional_date(None))
        self.assertIsNone(validations.optional_int(None))
        self.assertIsNone(validations.optional_float(None))
        # test the optional decorator
        thrower = lambda x: (_ for _ in ()).throw(Exception('In the validator!'))
        wrapped = validations.optional(thrower)
        self.assertIsNone(wrapped(None))
        self.assertRaises(Exception, lambda: wrapped(2))

    def test_nasa_date(self):
        sec_in_year = 60 * 60 * 24 * 365
        now = time.time()
        for i in range(100):
            offset = random.randint(15 * sec_in_year * -1, 10 * sec_in_year)
            test_date = date.fromtimestamp(now + offset)
            formatted = test_date.strftime('%Y-%m-%d')
            self.assertEqual(validations.nasa_date(formatted), formatted)
        self.assertRaises(ValueError, lambda: validations.nasa_date('tomorrow'))
        self.assertRaises(ValueError, lambda: validations.nasa_date('2015'))
        self.assertRaises(ValueError, lambda: validations.nasa_date('2015-01'))
        self.assertRaises(ValueError, lambda: validations.nasa_date('2015/01/04'))

    def test_nasa_int(self):
        for i in range(100):
            value = random.randint(-100000, 100000)
            self.assertEqual(validations.nasa_int(value), value)
        self.assertRaises(ValueError, lambda: validations.nasa_int(0.1))
        self.assertRaises(ValueError, lambda: validations.nasa_int('string'))
        self.assertRaises(ValueError, lambda: validations.nasa_int('10'))

    def test_nasa_float(self):
        for i in range(100):
            value = random.random()
            self.assertEqual(validations.nasa_float(value), value)
        self.assertRaises(ValueError, lambda: validations.nasa_float(12))
        self.assertRaises(ValueError, lambda: validations.nasa_float('1.5'))
