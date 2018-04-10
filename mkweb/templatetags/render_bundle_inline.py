import io
import os

from django import template
from django.conf import settings
from django.utils.html import mark_safe

from webpack_loader import utils


register = template.Library()


JS_INLINE = '<script type="text/javascript">{chunk}</script>'
CSS_INLINE = '<style type="text/css">{chunk}</style>'
JS_EXTERNAL = '<script type="text/javascript" src="{url}" {attrs}></script>'
CSS_EXTERNAL = '<link type="text/css" rel="stylesheet" href="{url}" {attrs} />'

BUNDLE_PATH = os.path.join(settings.BASE_DIR, 'static', 'app')


@register.simple_tag
def render_bundle_inline(
        bundle_name, extension=None, config='DEFAULT', attrs=''):
    tags = []
    for chunk in utils.get_files(
            bundle_name, extension=extension, config=config):

        path = os.path.join(BUNDLE_PATH, chunk['name'])
        if os.path.exists(path):
            with io.open(path, 'r', encoding='utf-8') as f:
                if chunk['name'].endswith(('.js', '.js.gz')):
                    tags.append(JS_INLINE.format(chunk=f.read()))
                elif chunk['name'].endswith(('.css', '.css.gz')):
                    tags.append(CSS_INLINE.format(chunk=f.read()))
        else:
            if chunk['name'].endswith(('.js', '.js.gz')):
                tags.append(JS_EXTERNAL.format(url=chunk['url'], attrs=attrs))
            elif chunk['name'].endswith(('.css', '.css.gz')):
                tags.append(CSS_EXTERNAL.format(url=chunk['url'], attrs=attrs))
    return mark_safe(''.join(tags))
