import re
from django.core.validators import *
from django.utils.translation import ugettext_lazy as _


color_re = re.compile(
    r'(^#[a-f0-9]{3,6}$)' # Hash style
    r'|(^rgb\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{2}|100%|[0-9]{1,2}%)\s*,\s*){2}((2[0-4][0-9]|25[0-5]|1?[0-9]{2}|100%|[0-9]{1,2}%)\s*)\))' # rgb style
    r'|(^rgba\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{2}|100%|[0-9]{1,2}%)\s*,\s*){3}(((0(\.[0-9]+)?)|1)\s*)\)$)' # rgba style
    r'|(^hsl\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{2})\s*,\s*(100%|[0-9]{1,2}%)\s*,\s*(100%|[0-9]{1,2}%)\s*\)$)' # hsl style
    r'|(^hsla\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{2})\s*,\s*((100%|[0-9]{1,2}%)\s*,\s*){2}(((0(\.[0-9]+)?)|1)\s*)\)$)', re.IGNORECASE) # hsla style
validate_color = RegexValidator(color_re, _(u'Enter a valid color in CSS format.'), 'invalid')
