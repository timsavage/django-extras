import decimal


NO_CURRENCY_CODE = 'XXX'
NO_CURRENCY_NUMBER = 999

class Currency(object):
    """
    Represents a currency.
    """
    __slots__ = ('code', 'number', 'name', 'symbol', )

    def __init__(self, code, number, name, symbol=''):
        self.code = code
        self.number = number
        self.name = name
        self.symbol = symbol

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
            raise TypeError, 'Can not multiply by a monetary quantity.'
        else:
            return Money(amount = self._amount * decimal_value(other))

    def __div__(self, other):
        if self._can_compare(other):
            raise TypeError, 'Can not divide by a monetary quantity.'
        else:
            return Money(amount = self._amount * decimal_value(other))

    def __rmod__(self, other):
        """
        Re-purposed to calculate a percentage of a monetary quantity.

        >>> 10 % money.Money(500)
        50.0000
        """
        if self._can_compare(other):
            raise TypeError, 'Can not use a monetary quantity as a percentage.'
        else:
            #noinspection PyTypeChecker
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
        if other is None:
            return False
        if isinstance(other, Money):
            return self.currency == other.currency and self._amount == other._amount
        return self._amount == decimal.Decimal(str(other))

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
        digits = map(str, digits)
        build, next = results.append, digits.pop

        # Append trailing negative sign
        if sign:
            build(trailing_negative)

        # Cut off decimal digits
        if places:
            for i in range(places):
                build(next())
            build(decimal_place)

        # Append digits
        if not digits:
            build('0')
        else:
            idx = 0
            while digits:
                build(next())
                idx += 1
                if not idx % 3 and digits:
                    build(str(separator))

        # Append currency symbol and sign before returning result
        build(str(currency_symbol))
        build(str(negative_sign if sign else positive_sign))
        return ''.join(reversed(results))
