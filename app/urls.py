from authlib.admin_oauth.views import admin_oauth
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import redirect, render
from django.urls import include, path, re_path
from django.views import generic

from blog.sitemaps import PostSitemap
from blog.views import ArchiveIndexView


admin.site.enable_nav_sidebar = False

urlpatterns = [
    path("", ArchiveIndexView.as_view(archive=False), name="blog_post_archive"),
    path("writing/", lambda request: redirect("blog_post_archive")),
    path("projects/", lambda request: redirect("blog_post_archive")),
    path("about/", lambda request: redirect("blog_post_archive")),
    path("contact/", lambda request: redirect("blog_post_archive")),
    path("404/", render, {"template_name": "404.html"}),
    re_path(
        r"^(?P<url>\d{4}/.*)$", generic.RedirectView.as_view(url="/writing/%(url)s")
    ),
    re_path(
        r"^blog/(?P<url>.*)$", generic.RedirectView.as_view(url="/writing/%(url)s")
    ),
    path("writing/", include("blog.urls")),
    path("manage/__oauth__/", admin_oauth, name="admin_oauth"),
    path("manage/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": {"posts": PostSitemap}}),
]

if settings.DEBUG:
    try:
        urlpatterns += [path("__debug__/", include(__import__("debug_toolbar").urls))]
    except ImportError:
        pass

    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
