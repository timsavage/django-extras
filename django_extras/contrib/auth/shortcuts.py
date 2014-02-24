# -*- encoding:utf8 -*-
"""
Django Extras: django_extras.contrib.auth.shortcuts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shortcuts for common operations.
"""
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


def get_owned_object_or_40x(klass, owner, include_staff=False,
                            include_superuser=True, *args, **kwargs):
    """
    Returns an object if it can be found (using get_object_or_404).
    If the object is not owned by the supplied owner a 403 will be raised.
    """
    obj = get_object_or_404(klass, *args, **kwargs)
    if obj.is_not_owned_by(owner, include_staff, include_superuser):
        raise PermissionDenied()
    return obj
