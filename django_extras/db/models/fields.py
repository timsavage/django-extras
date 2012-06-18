from django.core import exceptions
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extras import forms
from django_extras.core import validators
from django_extras.core.types import Money


_MODULE_NAME = 'django_extras.db.models.fields.'


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

    def south_field_triple(self):
        """
        Support for South
        """
        from south.modelsinspector import introspector
        args, kwargs = introspector(self)
        return _MODULE_NAME + self.__class__.__name__, args, kwargs


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

    def south_field_triple(self):
        """
        Support for South
        """
        from south.modelsinspector import introspector
        args, kwargs = introspector(self)
        return _MODULE_NAME + self.__class__.__name__, args, kwargs


class PercentField(models.FloatField):
    """
    Float field that ensures field value is in the range 0-100.
    """
    default_validators = [
        MinValueValidator(0),
        MaxValueValidator(100),
    ]

    def south_field_triple(self):
        from south.modelsinspector import introspector
        args, kwargs = introspector(self)
        return _MODULE_NAME + self.__class__.__name__, args, kwargs
