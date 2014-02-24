from django import test
from django.db.models.fields import NOT_PROVIDED
from django_extras.db.models.choices import ChoiceEnum


class ChoicesTestCase(test.TestCase):
    def test_kwargs(self):
        target = ChoiceEnum(
            OPTION_ONE=('value', 'Verbose value'),
            OPTION_TWO=('value2', 'Verbose value 2', True),  # Default, the value can be anything ;)
        )

        self.assertEqual('value', target.OPTION_ONE)
        self.assertEqual('value2', target.OPTION_TWO)

    def test_args(self):
        target = ChoiceEnum(
            ('OPTION_ONE', ('value', 'Verbose value')),
            ('OPTION_TWO', ('value2', 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

        self.assertEqual('value', target.OPTION_ONE)
        self.assertEqual('value2', target.OPTION_TWO)

    def test_max_length(self):
        target = ChoiceEnum(
            OPTION_ONE=('value', 'Verbose value'),
            OPTION_TWO=('value2', 'Verbose value 2', True),  # Default, the value can be anything ;)
        )

        self.assertEqual(6, target.max_length)

    def test_default_set(self):
        target = ChoiceEnum(
            OPTION_ONE=('value', 'Verbose value'),
            OPTION_TWO=('value2', 'Verbose value 2', True),  # Default, the value can be anything ;)
        )

        self.assertEqual('value2', target.default)

    def test_default_not_set(self):
        target = ChoiceEnum(
            OPTION_ONE=('value', 'Verbose value'),
            OPTION_TWO=('value2', 'Verbose value 2'),
        )

        self.assertEqual(NOT_PROVIDED, target.default)

    def test_kwargs_string_value(self):
        target = ChoiceEnum(
            ('OPTION_ONE', ('value', 'Verbose value')),
            ('OPTION_TWO', ('value2', 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

        self.assertEqual({
            'choices': target,
            'default': 'value2',
            'max_length': 6
        }, target.kwargs)

    def test_kwargs_int_value(self):
        target = ChoiceEnum(
            ('OPTION_ONE', (1, 'Verbose value')),
            ('OPTION_TWO', (2, 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

        self.assertEqual({
            'choices': target,
            'default': 2
        }, target.kwargs)

    def test_resolve_value(self):
        target = ChoiceEnum(
            ('OPTION_ONE', (1, 'Verbose value')),
            ('OPTION_TWO', (2, 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

        self.assertEqual('Verbose value', target.resolve_value(1))

    def test_mod(self):
        target = ChoiceEnum(
            ('OPTION_ONE', (1, 'Verbose value')),
            ('OPTION_TWO', (2, 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

        self.assertEqual('Verbose value 2', target % 2)

    def test_iterator(self):
        target = ChoiceEnum(
            ('OPTION_ONE', (1, 'Verbose value')),
            ('OPTION_TWO', (2, 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

        self.assertEqual([(1, 'Verbose value'), (2, 'Verbose value 2'), ], list(target))

    def test_getattr(self):
        target = ChoiceEnum(
            ('OPTION_ONE', (1, 'Verbose value')),
            ('OPTION_TWO', (2, 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

        self.assertEqual(1, target.OPTION_ONE)

    def test_getattr_display(self):
        target = ChoiceEnum(
            ('OPTION_ONE', (1, 'Verbose value')),
            ('OPTION_TWO', (2, 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

        self.assertEqual('Verbose value 2', target.OPTION_TWO__display)

    def test_contains(self):
        target = ChoiceEnum(
            ('OPTION_ONE', (1, 'Verbose value')),
            ('OPTION_TWO', (2, 'Verbose value 2', True)),  # Default, the value can be anything ;)
        )

        self.assertTrue(1 in target)
        self.assertFalse(3 in target)

    def test_init_no_entries(self):
        self.assertRaises(ValueError, lambda: ChoiceEnum())

    def test_init_invalid_entry(self):
        self.assertRaises(TypeError, lambda: ChoiceEnum(
            OPTION_ONE=('value', 'Verbose value'),
            OPTION_TWO='value2'
        ))

        self.assertRaises(ValueError, lambda: ChoiceEnum(
            OPTION_ONE=('value', 'Verbose value'),
            OPTION_TWO=('value2', 'Verbose value 2', True, 1)
        ))
