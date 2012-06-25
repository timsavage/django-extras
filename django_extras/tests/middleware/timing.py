from django import test
from django.http import HttpRequest, HttpResponse
from django_extras.middleware.timing import TimingMiddleware


class TimingMiddlewareTestCase(test.TestCase):
    def test_full_lifecycle(self):
        request = HttpRequest()
        response = HttpResponse()
        target = TimingMiddleware()

        target.process_request(request)
        assert(hasattr(request, TimingMiddleware.REQUEST_ATTR))

        target.process_response(request, response)
        self.assertIsNotNone(response[TimingMiddleware.RESPONSE_HEADER])

    def test_process_response_only(self):
        request = HttpRequest()
        response = HttpResponse()
        target = TimingMiddleware()

        target.process_response(request, response)
        self.assertRaises(KeyError, lambda: response[TimingMiddleware.RESPONSE_HEADER])
