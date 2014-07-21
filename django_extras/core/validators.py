# Convenience imports
from django.core.validators import *  # noqa
try:
    import json
except ImportError:
    from django.utils import simplejson as json
import six
from django.utils.translation import ugettext_lazy as _


color_re = re.compile(
    r'(^#[a-f0-9]{3,6}$)'  # Hash style
    r'|(^rgb\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*,\s*){2}((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*)\))'  # rgb style  # noqa
    r'|(^hsl\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{1,2})\s*,\s*(100%|[0-9]{1,2}%)\s*,\s*(100%|[0-9]{1,2}%)\s*\)$)',  # hsl style  # noqa
    re.IGNORECASE
)
validate_color = RegexValidator(color_re, _(six.u('Enter a valid color in CSS format.')), 'invalid')


alpha_color_re = re.compile(
    r'(^#[a-f0-9]{3,6}$)'  # Hash style
    r'|(^rgb\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*,\s*){2}((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*)\))'  # rgb style  # noqa
    r'|(^rgba\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*,\s*){3}(((0?(\.[0-9]+)?)|1)\s*)\)$)'  # rgba style  # noqa
    r'|(^hsl\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{1,2})\s*,\s*(100%|[0-9]{1,2}%)\s*,\s*(100%|[0-9]{1,2}%)\s*\)$)'  # hsl style  # noqa
    r'|(^hsla\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{1,2})\s*,\s*((100%|[0-9]{1,2}%)\s*,\s*){2}(((0?(\.[0-9]+)?)|1)\s*)\)$)',  # hsla style  # noqa
    re.IGNORECASE
)
validate_alpha_color = RegexValidator(alpha_color_re, _(six.u('Enter a valid color in CSS format.')), 'invalid')


class JsonValidator(object):
    message = _(six.u('Enter valid JSON.'))
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
            json.loads(value, **self.load_options)
        except ValueError:
            raise ValidationError(self.message, code=self.code)

validate_json = JsonValidator()
