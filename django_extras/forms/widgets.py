# Convenience import
from django.forms.widgets import *


class Html5EmailInput(TextInput):
    input_type = 'email'


class Html5NumberInput(TextInput):
    input_type = 'number'


class Html5DateInput(DateInput):
    input_type = 'date'


class Html5DateTimeInput(DateTimeInput):
    input_type = 'datetime'


class Html5TimeInput(TimeInput):
    input_type = 'time'


class JQueryColorPicker(TextInput):
    class Media:
        css = {
            'all': ('css/jquery/ui.colorPicker.css',)
        }
        js = ('js/jquery.ui.colorPicker.min.js', 'js/django_extras-widgets.js',)

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'django_extras-colorpicker' + attrs.get('class', '')
        return super(JQueryColorPicker, self).render(name, value, attrs)
