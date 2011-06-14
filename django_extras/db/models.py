

class ChoiceEnum(object):
    """
    Defines a choice set for use with Django Models.

    Items are defined with:

        MY_CHOICES = ChoiceEnum(
            OPTION_ONE = ('value', 'Verbose value'),
            OPTION_TWO = ('value2', 'Verbose value 2'),
        )

    They can then be used for choices with:

        MY_CHOICES.get_choices()

    And values referenced using:

        MY_CHOICES.OPTION_ONE

    Display values can be accessed via:

        MY_CHOICES.OPTION_ONE__display

    """
    def __init__(self, **entries):
        self._value_map = dict([(key, value) for (key, value) in entries.values()])
        self._choices = entries

    def get_choices(self):
        """
        Return choice list for use in model definition.
        """
        return self._choices.values()

    def resolve_display(self, value):
        """
        Resolve a value to it's display version.
        """
        return self._value_map[value]

    def __contains__(self, value):
        """
        Check if a choice value is in this enum.

        @param value Choice value.
        """
        return value in self._value_map.keys()

    def __getattr__(self, item):
        """
        Get the value of an Enum.

        Append __display to get display version of the item.
        """
        if item.endswith('__display'):
            return self._choices[item[:-9]][1]
        else:
            return self._choices[item][0]
