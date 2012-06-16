import datetime


class TimingMiddleware(object):
    """
    Appends the X-PROCESSING_TIME_MS header to all responses.

    This value is the total time spent processing a user request in microseconds.
    """

    def process_request(self, request):
        setattr(request, 'start', datetime.datetime.now())

    def process_response(self, request, response):
        start = getattr(request, 'start')
        if start:
            end = datetime.datetime.now()
            length = end - start
            response['X-PROCESSING_TIME_MS'] = str(length.microseconds)
