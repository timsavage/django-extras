import six
try:
    import json
except ImportError:
    from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.db import models
from django_extras import forms


def dumps(value):
    return DjangoJSONEncoder().encode(value)


def loads(txt):
    value = json.loads(txt, encoding=settings.DEFAULT_CHARSET)
    return value


class JsonDict(dict):
    """
    Hack so repr() called by dumpdata will output JSON instead of
    Python formatted data.  This way fixtures will work!
    """
    def __repr__(self):
        return dumps(self)


class JsonList(list):
    """
    As above
    """
    def __repr__(self):
        return dumps(self)


class JsonField(six.with_metaclass(models.SubfieldBase, models.TextField)):
    """Field that serializes/de-serializes a python list/dictionary to the
    database seamlessly."""

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = '{}'
        models.TextField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value is None or value == '':
            return {}
        elif isinstance(value, six.string_types):
            res = loads(value)
            if isinstance(res, dict):
                return JsonDict(**res)
            else:
                return JsonList(res)
        else:
            return value

    def get_db_prep_save(self, value, connection):
        """Convert our JSON object to a string before we save"""
        if not isinstance(value, (list, dict)):
            return super(JsonField, self).get_db_prep_save("", connection=connection)
        else:
            return super(JsonField, self).get_db_prep_save(dumps(value), connection=connection)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.JsonField}
        defaults.update(kwargs)
        return super(JsonField, self).formfield(**defaults)


# Register field with south.
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_extras\.db\.models\.fields\.jsonfield\.JsonField"])
except ImportError:
    pass
