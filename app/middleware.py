from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render


def force_domain(get_response):
    if settings.DEBUG or not settings.FORCE_DOMAIN:
        return get_response

    def middleware(request):
        if request.method != "GET":
            return get_response(request)

        if request.headers.get("host") != settings.FORCE_DOMAIN:
            target = "http{}://{}{}".format(
                request.is_secure() and "s" or "",
                settings.FORCE_DOMAIN,
                request.get_full_path(),
            )
            return HttpResponsePermanentRedirect(target)

        return get_response(request)

    return middleware


def only_staff(get_response):
    if settings.DEBUG or settings.TESTING:
        return get_response

    def middleware(request):
        if request.path.startswith("/admin"):
            return get_response(request)
        elif not request.user.is_staff:
            response = render(request, "only_staff.html", {})
            response.status_code = 403
            return response

        return get_response(request)

    return middleware
