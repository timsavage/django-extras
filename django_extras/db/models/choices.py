from collections import OrderedDict
from django.db.models.fields import NOT_PROVIDED
import six


class ChoiceEnum(object):
    """
    Defines a choice set for use with Django Models.

    ChoiceEnum can be used in one of two ways, due to a side effect of how dictionaries are sorted in Python
    (dictionaries and by extension **kwargs are implemented as a hash map) the order is not preserved.

    The nicest way to use ChoiceEnum (without guaranteed ordering):

        MY_CHOICES = ChoiceEnum(
            OPTION_ONE = ('value', 'Verbose value'),
            OPTION_TWO = ('value2', 'Verbose value 2', True),  # Default, the value can be anything ;)
        )

    The less nice way to use ChoiceEnum (with guaranteed ordering):

        MY_CHOICES = ChoiceEnum(
            ('OPTION_ONE', ('value', 'Verbose value')),
            ('OPTION_TWO', ('value2', 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

    They can then be used for field choices:

        foo = models.CharField(max_length=MY_CHOICES.max_length, choices=MY_CHOICES, default=MY_CHOICES.default)

    or with the kwargs helper:

        foo = models.CharField(**MY_CHOICES.kwargs)

    And values referenced using:

        MY_CHOICES.OPTION_ONE

    Display values can be accessed via:

        MY_CHOICES.OPTION_ONE__display

    Convert a value to a display string:

        MY_CHOICES % 'value'

    """
    __slots__ = ('__choices', '__default', '__max_length', '__value_map')

    def __init__(self, *args, **entries):
        if args:
            entries = OrderedDict(args)
        if not entries:
            raise ValueError('No entries have been provided.')

        self.__default = NOT_PROVIDED
        self.__max_length = 0
        self.__value_map = {}
        self.__choices = OrderedDict()

        for entry in entries.items():
            self.__parse_entry(*entry)

    def __parse_entry(self, key, value):
        if not isinstance(value, (tuple, list)):
            raise TypeError('Choice options should be a tuple or list.')
        value_len = len(value)
        if value_len not in (2, 3):
            raise ValueError('Expected choice entry in the form (Value, Verbose Value, [default]).')

        if value_len == 3:
            self.__default = value[0]
        if isinstance(value[0], six.string_types):
            self.__max_length = max(self.__max_length, len(value[0]))

        self.__value_map[value[0]] = value[1]
        self.__choices[key] = value[0], value[1]

    def __iter__(self):
        """
        Return choice list for use in model definition.
        """
        return iter(self.__choices.values())

    def __contains__(self, value):
        """
        Check if a choice value is in this enum.

        @param value Choice value.
        """
        return value in self.__value_map

    def __getattr__(self, item):
        """
        Get the value of an Enum.
        """
        if item.endswith('__display'):
            return self.__choices[item[:-9]][1]
        else:
            return self.__choices[item][0]

    def __mod__(self, other):
        """
        Resolve a value to it's display version.
        """
        return self.__value_map[other]

    @property
    def max_length(self):
        """
        Length of maximum value
        """
        return self.__max_length

    @property
    def default(self):
        """
        The default value.
        """
        return self.__default

    @property
    def kwargs(self):
        """
        Helper to simplify assignment of choices to a model field.
        """
        kwargs = {
            'choices': self,
            'default': self.__default,
        }
        if self.__max_length:
            kwargs['max_length'] = self.__max_length
        return kwargs

    def resolve_value(self, value):
        """
        Resolve a value to it's display version.
        """
        return self.__value_map[value]
