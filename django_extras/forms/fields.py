from django.forms.fields import *  # noqa
from django_extras.forms import widgets
from django_extras.core import validators


class ColorField(CharField):
    """
    Form field that provides input for color picker
    """
    widget = widgets.JQueryColorPicker

    def __init__(self, allow_alpha=False, *args, **kwargs):
        super(ColorField, self).__init__(*args, **kwargs)
        self.allow_alpha = allow_alpha
        if allow_alpha:
            self.validators.append(validators.validate_alpha_color)
        else:
            self.validators.append(validators.validate_color)


class JsonField(CharField):
    """
    Form field that validates that valid JSON is supplied.
    """
    widget = widgets.Textarea
    default_validators = [validators.validate_json]
