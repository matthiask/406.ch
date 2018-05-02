from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import redirect, render
from django.views import generic

from authlib.admin_oauth.views import admin_oauth
from blog.sitemaps import PostSitemap


urlpatterns = [
    url(r'^$', lambda request: redirect('blog_post_archive')),

    url(r'^about/$', render, {'template_name': 'base.html'}),
    url(r'^404/$', render, {'template_name': '404.html'}),
    url(r'^projects/$', render, {'template_name': 'projects.html'}),
    url(
        r'^contact/',
        generic.RedirectView.as_view(url='/'),
    ),
    url(
        r'^(?P<url>\d{4}/.*)$',
        generic.RedirectView.as_view(url='/writing/%(url)s')
    ),
    url(
        r'^blog/(?P<url>.*)$',
        generic.RedirectView.as_view(url='/writing/%(url)s'),
    ),
    url(r'^writing/', include('blog.urls')),
    url(
        r'^manage/__oauth__/$',
        admin_oauth,
        name='admin_oauth',
    ),
    url(r'^manage/', admin.site.urls),
    url(
        r'^sitemap\.xml$',
        sitemap,
        {
            'sitemaps': {'posts': PostSitemap},
        },
    ),
]

if settings.DEBUG:
    try:
        urlpatterns += [
            url(r'^__debug__/', include(__import__('debug_toolbar').urls)),
        ]
    except ImportError:
        pass

    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
