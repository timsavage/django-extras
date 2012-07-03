# -*- encoding:utf8 -*-
from django.contrib.auth.decorators import *
from django.core.exceptions import PermissionDenied


def superuser_required(function=None, login_url=None, raise_exception=False):
    """
    Decorator for views that checks that the user is a superuser, redirecting
    to the log-in page if necessary.
    """
    def check_permission(user):
        if user.is_superuser:
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    actual_decorator = user_passes_test(check_permission, login_url=login_url)
    if function:
        return actual_decorator(function)
    return actual_decorator


def staff_required(function=None, include_superusers=True, login_url=None,
                   raise_exception=False):
    """
    Decorator for views that checks that the user is a staff member,
    redirecting to the log-in page if necessary.
    """
    def check_permission(user):
        if user.is_staff or (include_superusers and user.is_superuser):
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    actual_decorator = user_passes_test(check_permission, login_url=login_url)
    if function:
        return actual_decorator(function)
    return actual_decorator
