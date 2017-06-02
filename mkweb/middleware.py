from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response


def force_domain(get_response):
    if settings.DEBUG or not settings.FORCE_DOMAIN:
        return get_response

    def middleware(request):
        if request.method != 'GET':
            return get_response(request)

        if request.META.get('HTTP_HOST') != settings.FORCE_DOMAIN:
            target = 'http%s://%s%s' % (
                request.is_secure() and 's' or '',
                settings.FORCE_DOMAIN,
                request.get_full_path())
            return HttpResponsePermanentRedirect(target)

        return get_response(request)

    return middleware


def only_staff(get_response):
    if settings.DEBUG or settings.TESTING:
        return get_response

    def middleware(request):
        if request.path.startswith('/admin'):
            return get_response(request)
        elif not request.user.is_staff:
            response = render_to_response('only_staff.html', {})
            response.status_code = 403
            return response

        return get_response(request)

    return middleware
