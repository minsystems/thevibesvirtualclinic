from functools import wraps

from django.http import Http404, HttpResponseBadRequest


def ajax_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        return function(request, *args, **kwargs)

    return wrap