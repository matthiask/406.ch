from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response


class ForceDomainMiddleware(object):
    def __init__(self):
        if settings.DEBUG or not settings.FORCE_DOMAIN:
            raise MiddlewareNotUsed

    def process_request(self, request):
        if request.method != 'GET':
            return

        if request.META.get('HTTP_HOST') != settings.FORCE_DOMAIN:
            target = 'http%s://%s%s' % (
                request.is_secure() and 's' or '',
                settings.FORCE_DOMAIN,
                request.get_full_path())
            return HttpResponsePermanentRedirect(target)


class OnlyStaffMiddleware(object):
    def __init__(self):
        if settings.DEBUG or settings.TESTING:
            raise MiddlewareNotUsed

    def process_request(self, request):
        if request.path.startswith('/admin'):
            pass
        elif not request.user.is_staff:
            response = render_to_response('only_staff.html', {})
            response.status_code = 403
            return response
