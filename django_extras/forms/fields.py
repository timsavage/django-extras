from django.utils import simplejson
from django.forms.fields import *
from django.forms.widgets import Textarea
from django_extras.core import validators


class JsonField(Field):
    """
    Form field that validates that valid JSON is supplied.
    """
    widget = Textarea
    default_validators = [ validators.validate_json ]
