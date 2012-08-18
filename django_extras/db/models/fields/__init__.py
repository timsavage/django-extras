from django.core import exceptions
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extras import forms
from django_extras.core import validators
from django_extras.core.types import Money
from django_extras.db.models.fields.json import JsonField


class ColorField(models.CharField):
    """
    Database field that represents a color value.
    """
    description = _("Color value")

    def __init__(self, verbose_name=None, name=None, allow_alpha=False, **kwargs):
        kwargs.setdefault('max_length', 40)
        super(ColorField, self).__init__(verbose_name, name, **kwargs)

        self.allow_alpha = allow_alpha
        if allow_alpha:
            self.validators.append(validators.validate_alpha_color)
        else:
            self.validators.append(validators.validate_color)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.ColorField}
        defaults.update(kwargs)
        if defaults['form_class'] is forms.ColorField:
            defaults.setdefault('allow_alpha', self.allow_alpha)
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


class LatitudeField(models.FloatField):
    """Latitude field

    Ensures value is in hte range (-90)-90.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [
            validators.MinValueValidator(-90.0),
            validators.MaxValueValidator(90.0),
            ])
        super(LatitudeField, self).__init__(*args, **kwargs)


class LongitudeField(models.FloatField):
    """Longitude field

    Ensures value is in hte range (-180)-180.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [
            validators.MinValueValidator(-180.0),
            validators.MaxValueValidator(180.0),
            ])
        super(LongitudeField, self).__init__(*args, **kwargs)

# Register special admin widgets if admin is in use.
#if 'django.contrib.admin' in settings.INSTALLED_APPS:
#    from django.contrib.admin import options
#    options.FORMFIELD_FOR_DBFIELD_DEFAULTS[ColorField] = { 'widget':  }

# Register fields with south.
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_extras\.db\.models\.fields\.\w+Field"])
except ImportError:
    pass
