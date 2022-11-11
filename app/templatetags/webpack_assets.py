from functools import cache

from django import template
from django.conf import settings
from django.utils.html import mark_safe


register = template.Library()


def webpack_assets(entry):
    debug = "debug." if settings.DEBUG else ""
    with open(settings.WEBPACK_ASSETS / f"{debug}{entry}.html") as f:
        html = f.read()
    return mark_safe(html.strip().removeprefix("<head>").removesuffix("</head>"))


if not settings.DEBUG:
    webpack_assets = cache(webpack_assets)
register.simple_tag(webpack_assets)
