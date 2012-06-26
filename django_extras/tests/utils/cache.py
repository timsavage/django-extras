from django import test
from django.db import models
from django_extras.utils.cache import generate_key, instance_key


class TestModel(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        app_label = 'test'


class GenerateKeyTestCase(test.TestCase):
    def __init__(self, *args, **kwargs):
        super(GenerateKeyTestCase, self).__init__(*args, **kwargs)
        self.m = TestModel(id=1, name='eek')

    def test_type_using_pk(self):
        actual = generate_key(TestModel, pk=1)
        self.assertEqual(actual, 'model:test.testmodel[pk=1]')

    def test_type_using_knowen_field(self):
        actual = generate_key(TestModel, id=2)
        self.assertEqual(actual, 'model:test.testmodel[id=2]')

    def test_type_using_unknown_field(self):
        self.assertRaises(AttributeError, lambda : generate_key(TestModel, eek=2))

    def test_type_using_single_postfix(self):
        actual = generate_key(TestModel, 'cover', pk=1)
        self.assertEqual(actual, 'model:test.testmodel[pk=1]:cover')

    def test_type_using_multiple_postfix(self):
        actual = generate_key(TestModel, 'foo', 'bar', pk=1)
        self.assertEqual(actual, 'model:test.testmodel[pk=1]:foo-bar')

    def test_instance_using_pk(self):
        actual = generate_key(self.m, pk=1)
        self.assertEqual(actual, 'model:test.testmodel[pk=1]')

    def test_instance_using_known_field(self):
        actual = generate_key(self.m, id=2)
        self.assertEqual(actual, 'model:test.testmodel[id=2]')

    def test_instance_using_unknown_field(self):
        self.assertRaises(AttributeError, lambda : generate_key(self.m, eek=2))

    def test_instance_using_single_postfix(self):
        actual = generate_key(self.m, 'cover', pk=1)
        self.assertEqual(actual, 'model:test.testmodel[pk=1]:cover')

    def test_instance_using_multiple_postfix(self):
        actual = generate_key(self.m, 'foo', 'bar', pk=1)
        self.assertEqual(actual, 'model:test.testmodel[pk=1]:foo-bar')


class InstanceKeyTestCase(test.TestCase):
    def __init__(self, *args, **kwargs):
        super(InstanceKeyTestCase, self).__init__(*args, **kwargs)
        self.m = TestModel(id=1, name='eek')

    def test_just_instance(self):
        actual = instance_key(self.m)
        self.assertEqual(actual, 'model:test.testmodel[pk=1]')

    def test_specific_fields(self):
        actual = instance_key(self.m, ('name', ))
        self.assertEqual(actual, 'model:test.testmodel[name=eek]')

    def test_unknown_field(self):
        self.assertRaises(AttributeError, lambda : instance_key(self.m, ('eek', )))

    def test_postfix(self):
        actual = instance_key(self.m, ('name', ), 'cover')
        self.assertEqual(actual, 'model:test.testmodel[name=eek]:cover')
