from django.forms.widgets import *  # noqa


class Html5EmailInput(TextInput):
    """
    Widget for HTML5 email input fields.
    """
    input_type = 'email'


class Html5NumberInput(TextInput):
    """
    Widget for HTML5 number input fields.
    """
    input_type = 'number'


class Html5DateInput(DateInput):
    """
    Widget for HTML5 date input fields.
    """
    input_type = 'date'


class Html5DateTimeInput(DateTimeInput):
    """
    Widget for HTML5 datetime input fields.
    """
    input_type = 'datetime'


class Html5TimeInput(TimeInput):
    """
    Widget for HTML5 time input fields.
    """
    input_type = 'time'


class JQueryColorPicker(TextInput):
    """
    Widget for jQuery UI color picker
    """
    class Media:
        css = {
            'all': ('css/jquery/ui.colorPicker.css',)
        }
        js = ('js/jquery.ui-colorPicker.js', 'js/django_extras-widgets.js',)

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'django_extras-colorpicker' + attrs.get('class', '')
        return super(JQueryColorPicker, self).render(name, value, attrs)
