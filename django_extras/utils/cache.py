# -*- coding:utf8 -*-
__all__ = ('generate_key', 'instance_key')


def _generate_key(instance_or_type, values, postfix=None):
    opts = instance_or_type._meta
    key = 'model:%s.%s[%s]' % (
        opts.app_label, opts.module_name,
        ','.join(['%s=%s' % v for v in values])
    )
    if postfix:
        key += ':' + postfix
    return key


def generate_key(instance_or_type, *args, **kwargs):
    """
    Generate a cache/no-sql key based from a model instance or type.

    Any key/value is used to indicate a field parameter.
    """
    field_names = [f.name for f in instance_or_type._meta.fields]
    field_names.append('pk')
    for field in kwargs.keys():
        if field not in field_names:
            raise AttributeError('Model "%s" has no field "%s".' % (
                instance_or_type._meta.module_name, field))
    return _generate_key(instance_or_type, kwargs.items(), '-'.join(args))


def instance_key(instance, fields=None, postfix=None):
    """
    Generate a cache/no-sql key based from a model instance.

    Fields can be used to generate a key not based on a private key.
    """
    if fields:
        values = [(f, getattr(instance, f)) for f in fields]
    else:
        values = [('pk', instance.pk), ]
    return _generate_key(instance, values, postfix)
