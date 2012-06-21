import re
from django.core.validators import *
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson


color_re = re.compile(
    r'(^#[a-f0-9]{3,6}$)' # Hash style
    r'|(^rgb\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*,\s*){2}((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*)\))' # rgb style
    r'|(^hsl\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{1,2})\s*,\s*(100%|[0-9]{1,2}%)\s*,\s*(100%|[0-9]{1,2}%)\s*\)$)', re.IGNORECASE) # hsl style
validate_color = RegexValidator(color_re, _(u'Enter a valid color in CSS format.'), 'invalid')


alpha_color_re = re.compile(
    r'(^#[a-f0-9]{3,6}$)' # Hash style
    r'|(^rgb\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*,\s*){2}((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*)\))' # rgb style
    r'|(^rgba\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*,\s*){3}(((0?(\.[0-9]+)?)|1)\s*)\)$)' # rgba style
    r'|(^hsl\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{1,2})\s*,\s*(100%|[0-9]{1,2}%)\s*,\s*(100%|[0-9]{1,2}%)\s*\)$)' # hsl style
    r'|(^hsla\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{1,2})\s*,\s*((100%|[0-9]{1,2}%)\s*,\s*){2}(((0?(\.[0-9]+)?)|1)\s*)\)$)', re.IGNORECASE) # hsla style
validate_alpha_color = RegexValidator(alpha_color_re, _(u'Enter a valid color in CSS format.'), 'invalid')


class JsonValidator(object):
    message = _(u'Enter valid JSON.')
    code = 'invalid'

    def __init__(self, message=None, code=None, load_options=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.load_options = load_options if load_options else {}

    def __call__(self, value):
        """
        Validates that the input is valid JSON.
        """
        try:
            simplejson.loads(value, **self.load_options)
        except ValueError:
            raise ValidationError(self.message, code=self.code)

validate_json = JsonValidator()
