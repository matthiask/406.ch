from django.http import HttpResponseRedirect
from django.urls import path, re_path

from blog import feeds, views


urlpatterns = [
    path("feed/", feeds.PostFeed(), name="blog_post_feed"),
    path("archive/", views.ArchiveIndexView.as_view(archive=True)),
    re_path(
        r"^(?P<year>\d{4})/$",
        views.YearArchiveView.as_view(),
        name="blog_post_archive_year",
    ),
    re_path(
        r"^(?P<year>\d{4})/(?P<month>\d{2})/$",
        views.MonthArchiveView.as_view(),
        name="blog_post_archive_month",
    ),
    re_path(
        r"^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$",
        views.DayArchiveView.as_view(),
        name="blog_post_archive_day",
    ),
    path(
        "category-<str:slug>/",
        views.CategoryArchiveIndexView.as_view(),
        name="blog_category_detail",
    ),
    path(
        "category-<str:slug>/feed/",
        feeds.CategoryFeed(),
        name="blog_category_feed",
    ),
    re_path(
        r"^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/$",
        views.post_detail_redirect,
    ),
    path("<str:slug>/", views.post_detail, name="blog_post_detail"),
    re_path(
        r"^category/([^/]+)/$",
        lambda r, slug: HttpResponseRedirect("../../category-%s/" % slug),
    ),
    re_path(
        r"^category/([^/]+)/feed/$",
        lambda r, slug: HttpResponseRedirect("../../../category-%s/feed/" % slug),
    ),
]
