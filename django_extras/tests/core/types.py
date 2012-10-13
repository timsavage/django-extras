#coding=UTF-8
from django import test
from django_extras.core.types import Money, latitude, longitude


#TODO: Add more tests to get complete coverage
class MoneyTestCase(test.TestCase):

    LARGE = Money('200000000.0000')
    SMALL = Money('100.000')
    NEGATIVE = Money('-200000.0000')

    FORMAT_POSITIVE = Money('123456.789')
    FORMAT_NEGATIVE = Money('-12345.6789')

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


class LatitudeTestCase(test.TestCase):
    def testEmpty(self):
        self.failUnlessEqual(latitude(), 0.0)

    def testOutOfRange(self):
        self.failUnlessRaises(ValueError, latitude, 91.0)
        self.failUnlessRaises(ValueError, latitude, -91.0)

    def testInvalidType(self):
        self.failUnlessRaises(ValueError, latitude, 91)
        self.failUnlessRaises(ValueError, latitude, "91")

    def testStrPositive(self):
        l = latitude(27 + 27.9487 / 60)
        self.failUnlessEqual(str(l), "27°27'56.922000\"N")

    def testStrNegative(self):
        l = latitude(-(27 + 27.9487 / 60))
        self.failUnlessEqual(str(l), "27°27'56.922000\"S")


class LongitudeTestCase(test.TestCase):
    def testEmpty(self):
        self.failUnlessEqual(longitude(), 0.0)

    def testOutOfRange(self):
        self.failUnlessRaises(ValueError, longitude, 191.0)
        self.failUnlessRaises(ValueError, longitude, -191.0)

    def testInvalidType(self):
        self.failUnlessRaises(ValueError, longitude, 91)
        self.failUnlessRaises(ValueError, longitude, "91")

    def testStrPositive(self):
        l = longitude(153 + 05.3408 / 60)
        self.failUnlessEqual(str(l), "153°05'20.448000\"E")

    def testStrNegative(self):
        l = longitude(-(153 + 05.3408 / 60))
        self.failUnlessEqual(str(l), "153°05'20.448000\"W")
