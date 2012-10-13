from django import template

register = template.Library()


@register.filter
def humanize_bytes(bytes, precision=1):
    """
    Generate a humanized version of a file size.
    :param bytes:
    :param precision:
    :return:
    """
    abbrevs = (
        (1<<50L, 'PB'),
        (1<<40L, 'TB'),
        (1<<30L, 'GB'),
        (1<<20L, 'MB'),
        (1<<10L, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)
