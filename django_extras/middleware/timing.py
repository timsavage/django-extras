import datetime


class TimingMiddleware(object):
    """
    Appends the X-PROCESSING_TIME_MS header to all responses.

    This value is the total time spent processing a user request in microseconds.
    """
    REQUEST_ATTR = '_timing_start'
    RESPONSE_HEADER = 'X-PROCESSING_TIME_MS'

    def process_request(self, request):
        setattr(request, self.REQUEST_ATTR, datetime.datetime.now())

    def process_response(self, request, response):
        start = getattr(request, self.REQUEST_ATTR, None)
        if start:
            end = datetime.datetime.now()
            length = end - start
            response[self.RESPONSE_HEADER] = str(length.microseconds)
        return response
