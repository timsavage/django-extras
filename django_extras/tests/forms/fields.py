from django import test
from django_extras.forms import fields
from django_extras.core import validators

class ColorFieldTestCase(test.TestCase):
    def test_check_validator_no_alpha(self):
        target = fields.ColorField()
        self.assertIn(validators.validate_color, target.validators)

    def test_check_validator_with_alpha(self):
        target = fields.ColorField(allow_alpha=True)
        self.assertIn(validators.validate_alpha_color, target.validators)