from django.core import exceptions
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django_extras import forms
from django_extras.core import validators
from django_extras.core.types import Money


class ColorField(models.CharField):
    """
    Database field that represents a color value.
    """
    default_validators = [validators.validate_color]
    description = _("Color value")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 40)
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # As with CharField, this will cause color validation to be performed
        # twice.
        defaults = {'widget': forms.ColorPickerWidget}
        defaults.update(kwargs)
        return super(ColorField, self).formfield(**defaults)


class MoneyField(models.DecimalField):
    """
    Database field that represents a Money amount.
    """
    default_error_messages = {
        'invalid': _(u'This value must be a monetary amount.'),
    }
    description = _("Monetary amount")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 20)
        kwargs.setdefault('decimal_places', 4)
        super(MoneyField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value
        try:
            return Money(value)
        except ValueError:
            raise exceptions.ValidationError(self.error_messages['invalid'])

    def get_db_prep_save(self, value, connection):
        value = self.to_python(value)
        if value is not None:
            value = value._amount
        super(MoneyField, self).get_db_prep_save(value, connection)


class PercentField(models.FloatField):
    """
    Float field that ensures field value is in the range 0-100.
    """
    default_validators = [
        MinValueValidator(0),
        MaxValueValidator(100),
    ]


class JsonField(models.TextField):
    """
    Field that stores a dictionary in the database as JSON.
    """
    description = _("JSON dictionary")

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.dump_options = { 'cls': DjangoJSONEncoder, }
        self.load_options = {}
        self.dump_options.update(kwargs.pop('dump_options', {}))
        self.load_options.update(kwargs.pop('load_options', {}))
        super(JsonField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, basestring):
            try:
                return simplejson.loads(value, **self.load_options)
            except ValueError:
                pass
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, basestring):
            return value
        return simplejson.dumps(value, **self.dump_options)

    def value_to_string(self, obj):
        return super(JsonField, self).value_to_string(obj)

    def value_from_object(self, obj):
        return simplejson.dumps(super(JsonField, self).value_from_object(obj))

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.JsonField}
        defaults.update(kwargs)
        return super(JsonField, self).formfield(**defaults)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_extras\.db\.models\.fields\.ColorField"])
    add_introspection_rules([], ["^django_extras\.db\.models\.fields\.MoneyField"])
    add_introspection_rules([], ["^django_extras\.db\.models\.fields\.PercentField"])
    add_introspection_rules([], ["^django_extras\.db\.models\.fields\.JsonField"])
except ImportError:
    pass
