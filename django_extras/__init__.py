VERSION = (0, 1, 2, 'beta')

def get_version(*args, **kwargs):
    # Don't litter django_extras/__init__.py with all the get_version stuff.
    # Only import if it's actually called.
    from django.utils.version import get_version
    return get_version(*args, **kwargs)
