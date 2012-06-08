from django.forms.widgets import *
from django.conf import settings


class ColorPickerWidget(TextInput):
    """
    Color picker widget.
    """
    class Media:
        js = (settings.STATIC_URL + 'js/jquery.colorpicker.js', )

    def __init__(self, attrs={}):
        attrs.set_default('class', 'vColorField')
        super(ColorPickerWidget, self).__init__(attrs=attrs)
