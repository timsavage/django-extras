from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extras.core import validators
from django_extras.types import Money
from django_extras import forms


class ColorField(models.CharField):
    """
    Database field that represents a color value.
    """
    default_error_messages = {
        'invalid': _(u'This value must be a CSS color value.'),
    }
    description = _("Color value")

    def __init__(self, verbose_name=None, name=None, max_length=30, **kwargs):
        kwargs.setdefault('verbose_name', verbose_name)
        kwargs.setdefault('name', name)
        kwargs.setdefault('max_length', max_length)
        super(ColorField, self).__init__(**kwargs)
        self.validators.append(validators.validate_color)

    def formfield(self, **kwargs):
        defaults = {
            'widget': forms.ColorPickerWidget
        }
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

    def __init__(self, verbose_name=None, name=None, max_digits=20, decimal_places=4, **kwargs):
        super(MoneyField, self).__init__(verbose_name, name, max_digits, decimal_places, **kwargs)

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

    def formfield(self, **kwargs):
        defaults = {
#            'form_class': forms.DecimalField,
        }
        defaults.update(kwargs)
        return super(MoneyField, self).formfield(**defaults)
