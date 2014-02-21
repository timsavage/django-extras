import six
import os.path
from django.http import *  # noqa
from email.utils import formatdate as format_http_date


class HttpResponseCreated(HttpResponse):
    status_code = 201


class HttpResponseAccepted(HttpResponse):
    status_code = 202


class HttpResponseNonAuthoritative(HttpResponse):
    status_code = 203


class HttpResponseNoContent(HttpResponse):
    status_code = 204


class HttpResponseResetContent(HttpResponse):
    status_code = 205


class HttpResponsePartialContent(HttpResponse):
    status_code = 206


# 301/302 Defined by Django


class HttpResponseSeeOther(HttpResponseRedirect):
    status_code = 303


# 304 Defined by Django


# 400 Defined by Django


class HttpResponseUnAuthorised(HttpResponse):
    status_code = 401


class HttpResponsePaymentRequired(HttpResponse):
    status_code = 402


# 403/404/405 Defined by Django


class HttpResponseNotAcceptable(HttpResponse):
    status_code = 406


class HttpResponseRequestTimeout(HttpResponse):
    status_code = 408


class HttpResponseConflict(HttpResponse):
    status_code = 409


# 410 Defined by Django


class HttpResponseLengthRequired(HttpResponse):
    status_code = 411


class HttpResponsePreconditionFailed(HttpResponse):
    status_code = 412


class HttpResponseRequestEntityTooLarge(HttpResponse):
    status_code = 413


class HttpResponseUnsupportedMediaType(HttpResponse):
    status_code = 415


class HttpResponseExpectationFailed(HttpResponse):
    status_code = 417


class HttpResponseUnprocessableEntity(HttpResponse):
    status_code = 422


class HttpResponseLocked(HttpResponse):
    status_code = 423


class HttpResponseFailedDependency(HttpResponse):
    status_code = 424


class HttpResponseUpgradeRequired(HttpResponse):
    status_code = 426


class HttpResponseNotImplemented(HttpResponse):
    status_code = 501


class HttpResponseBadGateway(HttpResponse):
    status_code = 502


class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503


class HttpResponseGatewayTimeout(HttpResponse):
    status_code = 504


class HttpResponseInsufficientStorage(HttpResponse):
    status_code = 507


class FileResponse(HttpResponse):
    """
    Response object that handles files
    """
    def __init__(self, content, content_type, include_last_modified=True):
        if isinstance(content, six.string_types):
            f = open(content, 'rb')
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
        try:
            import json
        except ImportError:
            from django.utils import simplejson as json
        from django.core.serializers.json import DjangoJSONEncoder

        super(JsonResponse, self).__init__(json.dumps(data, cls=DjangoJSONEncoder),
                                           content_type=content_type, **kwargs)
