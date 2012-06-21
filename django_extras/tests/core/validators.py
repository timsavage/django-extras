from django import test
from django_extras.core import validators


class ColorValidatorTestCase(test.TestCase):
    def test_hash(self):
        validators.validate_color('#123')
        validators.validate_color('#abc')
        validators.validate_color('#45d')
        validators.validate_color('#6789ef')
        validators.validate_color('#abcdef')
        validators.validate_color('#0a1b2c')

    def test_rgb(self):
        validators.validate_color('rgb(0,1,2)')
        validators.validate_color('rgb(34,56,78)')
        validators.validate_color('rgb(191,234,156)')
        validators.validate_color('rgb(255,255,255)')

    def test_hsl(self):
        validators.validate_color('hsl(1,2%,3%)')
        validators.validate_color('hsl(23,45%,67%)')
        validators.validate_color('hsl(345,89%,90%)')
        validators.validate_color('hsl(360,100%,100%)')


class AlphaColorValidatorTestCase(test.TestCase):
    def test_hash(self):
        validators.validate_alpha_color('#123')
        validators.validate_alpha_color('#abc')
        validators.validate_alpha_color('#45d')
        validators.validate_alpha_color('#6789ef')
        validators.validate_alpha_color('#abcdef')
        validators.validate_alpha_color('#0a1b2c')

    def test_rgb(self):
        validators.validate_alpha_color('rgb(0,1,2)')
        validators.validate_alpha_color('rgb(34,56,78)')
        validators.validate_alpha_color('rgb(191,234,156)')
        validators.validate_alpha_color('rgb(255,255,255)')

    def test_rgba(self):
        validators.validate_alpha_color('rgba(0, 1, 2, 0)')
        validators.validate_alpha_color('rgba(34, 56, 78, 0.1)')
        validators.validate_alpha_color('rgba(191, 234, 156, .2)')
        validators.validate_alpha_color('rgba(255, 255, 255, 1)')

    def test_hsl(self):
        validators.validate_alpha_color('hsl(1,2%,3%)')
        validators.validate_alpha_color('hsl(23,45%,67%)')
        validators.validate_alpha_color('hsl(345,89%,90%)')
        validators.validate_alpha_color('hsl(360,100%,100%)')

    def test_hsla(self):
        validators.validate_alpha_color('hsla(1,2%,3%,0)')
        validators.validate_alpha_color('hsla(23,45%,67%,0.1)')
        validators.validate_alpha_color('hsla(345,89%,90%,.2)')
        validators.validate_alpha_color('hsla(360,100%,100%,1)')


class JsonValidatorTestCase(test.TestCase):
    def invalid_json(self):
        validators.validate_json('{"foo":"bar", "eek": 123, }')

    def test_valid(self):
        validators.validate_json('{"foo":"bar", "eek": 123}')

    def test_invalid(self):
        self.assertRaises(validators.ValidationError, self.invalid_json)

