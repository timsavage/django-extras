TIME_MAP = (
    ('w', 604800),
    ('d', 86400),
    ('h', 3600),
    ('m', 60),
    ('s', 1)
)


def describe_seconds(value):
    """
    Convert a seconds value into a human readable (ie week, day, hour) value.
    :param value: integer value of the number of seconds.
    :return: a string with the humanized value.
    """
    value_vector = []
    for unit, factor in iter(TIME_MAP):
        component, value = int(value / factor), value % factor
        if component:
            value_vector.append('%s%s' % (component, unit))
    return ' '.join(value_vector)
