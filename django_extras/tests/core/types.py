#coding=UTF-8
from decimal import Decimal
from django import test
from django_extras.core.types import Currency, Money, latitude, longitude, decimal_value


class ToDecimalTestCase(test.TestCase):
    def test_value_values(self):
        self.assertEqual(decimal_value(12), Decimal('12'))
        self.assertEqual(decimal_value(12.3), Decimal('12.3'))
        self.assertEqual(decimal_value('12'), Decimal('12'))

    def test_value_is_none(self):
        with self.assertRaises(ValueError):
            decimal_value(None)

    def test_empty_value(self):
        with self.assertRaises(ValueError):
            decimal_value('')

        with self.assertRaises(ValueError):
            decimal_value([])

        with self.assertRaises(ValueError):
            decimal_value(())

        with self.assertRaises(ValueError):
            decimal_value({})

    def test_decimal_value(self):
        in_value = Decimal('12')
        out_value = decimal_value(in_value)

        self.assertEqual(in_value, out_value)
        self.assertIs(in_value, out_value)


#TODO: Add more tests to get complete coverage
class MoneyTestCase(test.TestCase):

    LARGE = Money('200000000.0000')
    SMALL = Money('100.000')
    NEGATIVE = Money('-200000.0000')

    FORMAT_POSITIVE = Money('123456.789')
    FORMAT_NEGATIVE = Money('-12345.6789')

    AUD = Currency('AUD', 36, "Australian Dollar", '$')
    NZD = Currency('NZD', 554, "New Zealand Dollar", '$')

    def test_format_default(self):
        self.assertEqual('123,456.79', self.FORMAT_POSITIVE.format())
        self.assertEqual('-12,345.68', self.FORMAT_NEGATIVE.format())

    def test_format_places(self):
        self.assertEqual('123,456.7890', self.FORMAT_POSITIVE.format(places=4))
        self.assertEqual('-12,345.678900', self.FORMAT_NEGATIVE.format(places=6))

    def test_format_currency_symbol(self):
        self.assertEqual('$123,456.79', self.FORMAT_POSITIVE.format(currency_symbol='$'))
        self.assertEqual('-£12,345.68', self.FORMAT_NEGATIVE.format(currency_symbol='£'))

    def test_format_europe(self):
        self.assertEqual('123.456,79', self.FORMAT_POSITIVE.format(separator='.', decimal_place=','))
        self.assertEqual('-12.345,68', self.FORMAT_NEGATIVE.format(separator='.', decimal_place=','))

    def test_format_signs(self):
        self.assertEqual('p123,456.79', self.FORMAT_POSITIVE.format(positive_sign="p"))
        self.assertEqual('n12,345.68', self.FORMAT_NEGATIVE.format(negative_sign="n"))

    def test_format_trailing_negative(self):
        self.assertEqual('123,456.79', self.FORMAT_POSITIVE.format(trailing_negative=" neg"))
        self.assertEqual('-12,345.68 neg', self.FORMAT_NEGATIVE.format(trailing_negative=" neg"))

    # Tests from issue #1
    def test_equal_equal_values(self):
        self.assertTrue(self.SMALL == '100.0')
        self.assertTrue(self.SMALL == '100')
        self.assertTrue(self.SMALL == 100.0)
        self.assertTrue(Money('123.4567') == Money('123.4567'))
        self.assertTrue(Money('123.4567', self.AUD) == Money('123.4567', self.AUD))

    def test_equal_not_equal_values(self):
        self.assertFalse(self.SMALL == 99)
        self.assertFalse(self.SMALL == '99.9')
        self.assertFalse(self.SMALL == None)
        self.assertFalse(self.SMALL == '')
        self.assertFalse(self.SMALL == [])
        self.assertFalse(Money('123.4567') == Money('765.4321'))
        self.assertFalse(Money('123.4567', self.AUD) == Money('123.4567', self.NZD))


class LatitudeTestCase(test.TestCase):
    def testEmpty(self):
        self.assertEqual(0.0, latitude())

    def testOutOfRange(self):
        with self.assertRaises(ValueError):
            latitude(91.0)
        with self.assertRaises(ValueError):
            latitude(-91.0)

    def testInvalidType(self):
        with self.assertRaises(ValueError):
            latitude(91)
        with self.assertRaises(ValueError):
            latitude("91")

    def testStrPositive(self):
        l = latitude(27 + 27.9487 / 60)
        self.assertEqual("27°27'56.922000\"N", str(l))

    def testStrNegative(self):
        l = latitude(-(27 + 27.9487 / 60))
        self.assertEqual("27°27'56.922000\"S", str(l))


class LongitudeTestCase(test.TestCase):
    def testEmpty(self):
        self.assertEqual(0.0, longitude())

    def testOutOfRange(self):
        with self.assertRaises(ValueError):
            longitude(191.0)
        with self.assertRaises(ValueError):
            longitude(-191.0)

    def testInvalidType(self):
        with self.assertRaises(ValueError):
            longitude(91)
        with self.assertRaises(ValueError):
            longitude("91")

    def testStrPositive(self):
        l = longitude(153 + 05.3408 / 60)
        self.assertEqual("153°05'20.448000\"E", str(l))

    def testStrNegative(self):
        l = longitude(-(153 + 05.3408 / 60))
        self.assertEqual("153°05'20.448000\"W", str(l))
