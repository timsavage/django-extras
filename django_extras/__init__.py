"""
Django Extras
~~~~~~~~~~~~~

Extensions for Django to solve common development situations not (or not yet)
covered by the core Django framework.

"""

VERSION = (0, 2, 8)


def get_version():
    return '.'.join(str(a) for a in VERSION)
