import sys

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views import generic

from blog.sitemaps import PostSitemap


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', generic.RedirectView.as_view(
        url='/writing/',
        permanent=False,
        )),
    url(r'^home/$', generic.TemplateView.as_view(
        template_name='home.html',
        )),
    url(r'^404/$', generic.TemplateView.as_view(
        template_name='404.html',
        )),
    url(r'^(?P<url>\d{4}/.*)$', generic.RedirectView.as_view(
        url='/writing/%(url)s',
        )),
    url(r'^blog/(?P<url>.*)$', generic.RedirectView.as_view(
        url='/writing/%(url)s',
        )),

    url(r'^writing/', include('blog.urls')),
    url(r'^photos/', include('chet.urls')),
    url(r'^manage/', include(admin.site.urls)),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {
        'sitemaps': {
            'posts': PostSitemap,
        }}),
)

if 'runserver' in sys.argv:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
