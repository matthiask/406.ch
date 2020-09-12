from django.http import HttpResponseRedirect
from django.urls import re_path

from . import feeds, views


urlpatterns = [
    re_path(r"^feed/$", feeds.PostFeed(), name="blog_post_feed"),
    re_path(r"^archive/$", views.ArchiveIndexView.as_view(archive=True)),
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
    re_path(
        r"^category-(?P<slug>[^/]+)/$",
        views.CategoryArchiveIndexView.as_view(),
        name="blog_category_detail",
    ),
    re_path(
        r"^category-(?P<slug>[^/]+)/feed/$",
        feeds.CategoryFeed(),
        name="blog_category_feed",
    ),
    re_path(
        r"^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/$",
        views.post_detail_redirect,
    ),
    re_path(r"^(?P<slug>[^/]+)/$", views.post_detail, name="blog_post_detail"),
    re_path(
        r"^category/([^/]+)/$",
        lambda r, slug: HttpResponseRedirect("../../category-%s/" % slug),
    ),
    re_path(
        r"^category/([^/]+)/feed/$",
        lambda r, slug: HttpResponseRedirect("../../../category-%s/feed/" % slug),
    ),
]
