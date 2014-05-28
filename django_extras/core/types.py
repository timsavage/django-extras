# -*- coding: UTF-8 -*-
import decimal
import math


NO_CURRENCY_CODE = 'XXX'
NO_CURRENCY_NUMBER = 999


class Currency(object):
    """
    Definition of a currency.

    This object uses values from the ISO_4217 list of currency names, codes.
    See http://en.wikipedia.org/wiki/ISO_4217
    """
    __slots__ = ('code', 'number', 'name', 'symbol', 'decimal_digits')

    def __init__(self, code, number, name, symbol='', decimal_digits=2):
        self.code = code
        self.number = number
        self.name = name
        self.symbol = symbol
        self.decimal_digits = decimal_digits

    # Comparison operators
    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Currency):
            return self.code == other.code
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def is_no_currency(self):
        return self.code == NO_CURRENCY_CODE

NoCurrency = Currency(NO_CURRENCY_CODE, NO_CURRENCY_NUMBER, 'No Currency')


def decimal_value(value):
    """
    Convert a value into a decimal and handle any conversion required.

    @raises ValueError if trying to convert a value that does not translate to decimal.
    """
    if value is None:
        raise ValueError('None is not a valid money value.')
    if not isinstance(value, decimal.Decimal):
        try:
            return decimal.Decimal(str(value))
        except decimal.InvalidOperation:
            raise ValueError('Value could not be converted into a decimal.')
    return value


class Money(object):
    """
    Represents a monetary quantity.
    """
    __slots__ = ('_amount', 'currency', )

    def __init__(self, amount=decimal.Decimal('0.0'), currency=NoCurrency):
        self._amount = decimal_value(amount)
        self.currency = currency

    def __repr__(self):
        return '%5.4f' % self._amount

    def __unicode__(self):
        return self.format()

    def __hash__(self):
        return self.__repr__()

    # Math operators
    def __pos__(self):
        return Money(amount=self._amount)

    def __neg__(self):
        return Money(amount=-self._amount)

    def __add__(self, other):
        if self._can_compare(other):
            return Money(amount=self._amount + other._amount)
        else:
            return Money(amount=self._amount + decimal_value(other))

    def __sub__(self, other):
        if self._can_compare(other):
            return Money(amount=self._amount - other._amount)
        else:
            return Money(amount=self._amount - decimal_value(other))

    def __mul__(self, other):
        if self._can_compare(other):
            raise TypeError('Can not multiply by a monetary quantity.')
        else:
            return Money(amount=self._amount * decimal_value(other))

    def __div__(self, other):
        if self._can_compare(other):
            raise TypeError('Can not divide by a monetary quantity.')
        else:
            return Money(amount=self._amount * decimal_value(other))

    def __rmod__(self, other):
        """
        Re-purposed to calculate a percentage of a monetary quantity.

        >>> 10 % Money(500)
        50.0000
        """
        if isinstance(other, Money):
            raise TypeError('Can not use a monetary quantity as a percentage.')
        else:
            # noinspection PyTypeChecker
            percentage = decimal_value(other) * self._amount / 100
            return Money(amount=percentage)

    def __abs__(self):
        return Money(abs(self._amount))

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rdiv__ = __div__

    # Comparison operators
    def __eq__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                return False
            return self._amount == other._amount
        # For non Money types assume the that the amount is being compared.
        try:
            return self._amount == decimal_value(other)
        except ValueError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self._can_compare(other):
            return self._amount < other._amount
        else:
            return self._amount < decimal.Decimal(str(other))

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        if self._can_compare(other):
            return self._amount > other._amount
        else:
            return self._amount > decimal.Decimal(str(other))

    def __ge__(self, other):
        return self > other or self == other

    # Type conversion
    def __int__(self):
        return self._amount.__int__()

    def __float__(self):
        return self._amount.__float__()

    # Pickle support
    def __getstate__(self):
        return {
            'amount': self._amount,
            'currency': self.currency.code,
        }

    def __setstate__(self, state):
        self._amount = decimal_value(state.get('amount', '0.0'))

    def _can_compare(self, right):
        """
        Check if we are able to compare right value.

        @raises Value Error if currencies do not match.
        """
        if isinstance(right, Money):
            if self.currency == right.currency:
                return True
            else:
                raise ValueError('Currencies do not match')
        else:
            return False

    def format(self, places=2, currency_symbol='', separator=',', decimal_place='.', positive_sign='',
               negative_sign='-', trailing_negative=''):
        """
        Format money value to a string
        """
        # Round and split number
        q = decimal.Decimal(10) ** -places
        sign, digits, exp = self._amount.quantize(q).as_tuple()

        # Convert digits to string
        results = []
        digits = [str(d) for d in digits]
        build, next_ = results.append, digits.pop

        # Append trailing negative sign
        if sign:
            build(trailing_negative)

        # Cut off decimal digits
        if places:
            for i in range(places):
                build(next_())
            build(decimal_place)

        # Append digits
        if not digits:
            build('0')
        else:
            idx = 0
            while digits:
                build(next_())
                idx += 1
                if not idx % 3 and digits:
                    build(str(separator))

        # Append currency symbol and sign before returning result
        build(str(currency_symbol))
        build(str(negative_sign if sign else positive_sign))
        return ''.join(reversed(results))


def to_dms(value, absolute=False):
    """
    Split a float value into DMS (degree, minute, second) parts

    :param value - Float value to split
    :param absolute - Obtain the absolute value
    :return tuple containing DMS values
    """
    invert = not absolute and value < 0
    value = abs(value)
    degree = int(math.floor(value))
    value = (value - degree) * 60
    minute = int(math.floor(value))
    second = (value - minute) * 60
    return (
        degree * -1 if invert else degree,
        minute,
        second
    )


def to_dm(value, absolute=False):
    """
    Split a float value into DM (degree, minute) parts

    :param value - Float value to split
    :param absolute - Obtain the absolute value
    :return tuple containing DM values
    """
    invert = not absolute and value < 0
    value = abs(value)
    degree = int(math.floor(value))
    minute = (value - degree) * 60
    return (
        degree * -1 if invert else degree,
        minute
    )


class latitude(float):
    """ Latitude value """
    def __new__(cls, value=None):
        if value is None:
            return float.__new__(cls, 0.0)
        if isinstance(value, float):
            if 90.0 >= value >= -90.0:
                return float.__new__(cls, value)
            raise ValueError("Value %d out of range(-90.0, 90.0)" % value)
        raise ValueError("Expected type float or latitude")

    def __repr__(self):
        return "%02.3f" % self

    def __str__(self):
        result = "%02i°%02i'%02f\"" % to_dms(self, True)
        if self < 0:
            return result + 'S'
        else:
            return result + 'N'


class longitude(float):
    """Longitude value"""
    def __new__(cls, value=None):
        if value is None:
            return float.__new__(cls, 0.0)
        if isinstance(value, float):
            if 180.0 >= value >= -180.0:
                return float.__new__(cls, value)
            raise ValueError("Value %d out of range(-180.0, 180.0)" % value)
        raise ValueError("Expected type float or longitude")

    def __repr__(self):
        return "%03.3f" % self

    def __str__(self):
        result = "%03i°%02i\'%02f\"" % to_dms(self, True)
        if self < 0:
            return result + 'W'
        else:
            return result + 'E'


class latlng(object):
    """Latitude/Longitude pair"""

    __slots__ = ['lat', 'lng']  # Define available parameters

    def __init__(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            (lat, lng) = value
            self.lat = latitude(lat)
            self.lng = longitude(lng)
        elif isinstance(value, latlng):
            self.lat = latitude(value.lat)
            self.lng = longitude(value.lng)
        else:
            raise ValueError

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return self.lat == other.lat and self.lng == other.lng

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Latitude %s; Longitude %s" % (str(self.lat), str(self.lng))

    def get_value(self):
        """ Returns tuple lat/lng pair """
        return self.lat, self.lng
