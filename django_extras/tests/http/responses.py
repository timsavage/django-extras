import os.path
import datetime
import json
from django import test
import six
from django_extras.http import FileResponse, JsonResponse


class FileResponseTestCase(test.TestCase):
    def test_with_file_handle(self):
        path = os.path.dirname(__file__)
        f = open(os.path.join(path, 'data/example.txt'))
        target = FileResponse(f, 'test/plain')

        self.assertEqual(target['Content-Type'], 'test/plain')


class JsonResponseTestCase(test.TestCase):
    def assertJSONEqual(self, raw, expected_data, msg=None):
        try:
            data = json.loads(raw)
        except ValueError:
            self.fail("First argument is not valid JSON: %r" % raw)
        if isinstance(expected_data, six.string_types):
            try:
                expected_data = json.loads(expected_data)
            except ValueError:
                self.fail("Second argument is not valid JSON: %r" % expected_data)
        self.assertEqual(data, expected_data, msg=msg)

    def test_simple_dictionary(self):
        target = JsonResponse({
            'foo': 'bar',
            'eek': 123
        })

        if six.PY3:
            actual = target.content.decode('utf8')
        else:
            actual = ''.join(target)
        self.assertJSONEqual(actual, {"foo": "bar", "eek": 123})
        self.assertEqual(target['Content-Type'], 'application/json')

    def test_with_dates(self):
        target = JsonResponse({
            'foo': 'bar',
            'eek': datetime.datetime(2012, 6, 25, 11, 9, 48)
        })

        if six.PY3:
            actual = target.content.decode('utf8')
        else:
            actual = ''.join(target)
        self.assertJSONEqual(actual, {"foo": "bar", "eek": "2012-06-25T11:09:48"})
        self.assertEqual('application/json', target['Content-Type'])
