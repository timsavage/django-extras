from django import template
from django_extras.utils import humanize


register = template.Library()


@register.filter(is_safe=True)
def describe_seconds(value):
    """
    Convert a seconds value into a human readable (ie week, day, hour) value.
    :param value: integer value of the number of seconds.
    :return: a string with the humanized value.
    """
    return humanize.describe_seconds(value)
