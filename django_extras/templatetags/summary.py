from django import template

register = template.Library()


@register.filter
def humanize_bytes(value, precision=1):
    """
    Generate a humanized version of a file size.
    :param value:
    :param precision:
    :return:
    """
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if value == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if value >= factor:
            break
    return '%.*f %s' % (precision, value / factor, suffix)
