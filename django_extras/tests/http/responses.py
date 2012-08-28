import os.path
import datetime
from django import test
from django_extras.http import FileResponse, JsonResponse


class FileResponseTestCase(test.TestCase):
    def test_with_file_handle(self):
        path = os.path.dirname(__file__)
        f = file(os.path.join(path, 'data/example.txt'))
        target = FileResponse(f, 'test/plain')

        self.assertEqual(target['Content-Type'], 'test/plain')


class JsonResponseTestCase(test.TestCase):
    def test_simple_dictionary(self):
        target = JsonResponse({
            'foo': 'bar',
            'eek': 123
        })

        actual = ''.join(target)
        self.assertEqual(actual, '{"foo": "bar", "eek": 123}')
        self.assertEqual(target['Content-Type'], 'application/json')

    def test_with_dates(self):
        target = JsonResponse({
            'foo': 'bar',
            'eek': datetime.datetime(2012, 6, 25, 11, 9, 48)
        })

        actual = ''.join(target)
        self.assertEqual('{"foo": "bar", "eek": "2012-06-25 11:09:48"}', actual)
        self.assertEqual('application/json', target['Content-Type'])
