from __future__ import unicode_literals

from django.apps import apps
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class Widget(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise TypeError('Invalid attribute %s for %s' % (
                    key, self.__class__.__name__))
            setattr(self, key, value)

    def get_context(self):
        return {}

    def render(self, context):
        html = render_to_string(
            'mkadmin/%s.html' % self.__class__.__name__.lower(),
            dict(self.get_context(), widget=self),
            context_instance=context)
        return html


class AtAGlance(Widget):
    models = []
    title = _('At a glance')

    def get_context(self):
        models = [apps.get_model(model) for model in self.models]
        models = [{
            'name': model._meta.verbose_name_plural,
            'count': model._default_manager.count(),
            'admin_url': reverse('admin:%s_%s_changelist' % (
                model._meta.app_label, model._meta.model_name)),
        } for model in models]

        versions = []

        import django
        versions.append('Django %s' % django.get_version())

        try:
            import feincms
            versions.append('FeinCMS %s' % feincms.__version__)
        except ImportError:
            pass

        return {
            'models': models,
            'versions': versions,
        }


class Feed(Widget):
    title = _('Feed')
    url = None

    def get_context(self):
        cache_key = 'feed:%s' % self.url
        value = cache.get(cache_key)
        if value:
            return value

        import feedparser
        import socket

        socket.setdefaulttimeout(5)
        try:
            feed = feedparser.parse(self.url)
            value = {
                'feed': feed,
            }
        except:
            value = {}

        cache.set(cache_key, value, timeout=300)
        return value


class RecentActions(Widget):
    title = _('Recent Actions')


class AllApps(Widget):
    title = _('All apps')


class QuickDraft(Widget):
    title = _('Quick draft')

    def render(self, context):
        from django.utils.safestring import mark_safe
        return mark_safe(
            '<div class="module"><h2>Quick draft</h2>'
            '<form><input/></form></div>')
