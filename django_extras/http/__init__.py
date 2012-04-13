from django.core.serializers import json
from django.utils import simplejson
from django.http import HttpResponse


class HttpResponseUnAuthorised(HttpResponse):
    status_code = 401

class HttpResponseConflict(HttpResponse):
    status_code = 409

class HttpResponseNotImplemented(HttpResponse):
    status_code = 501

class HttpResponseGatewayTimeout(HttpResponse):
    status_code = 504


class FileResponse(HttpResponse):
    """
    Response object that handles files
    """
    def __init__(self, content, content_type, include_last_modified=True):
        if isinstance(content, basestring):
            f = file(content, 'rb')
        else:
            f = content
        super(FileResponse, self).__init__(f, content_type=content_type)

        if include_last_modified:
            modified = os.path.getmtime(f.name)
            self['Last-Modified'] = format_http_date(timeval=modified, localtime=True)


class JsonResponse(HttpResponse):
    """
    Response object that handles JSON encoding and sets the correct content type.
    """
    def __init__(self, data, content_type='application/json', **kwargs):
        super(JsonResponse, self).__init__(
            simplejson.dumps(data, cls=json.DjangoJSONEncoder),
            content_type=content_type, **kwargs)
            
