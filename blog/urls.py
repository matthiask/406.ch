from django.conf.urls import patterns, include, url

from . import feeds, views


urlpatterns = patterns('',
    url(r'^feed/$', feeds.PostFeed(), name='blog_post_feed'),

    url(r'^$', views.ArchiveIndexView.as_view(), name='blog_post_archive'),
    url(r'^(?P<year>\d{4})/$',
        views.YearArchiveView.as_view(), name='blog_post_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.MonthArchiveView.as_view(), name='blog_post_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.DayArchiveView.as_view(), name='blog_post_archive_day'),

    url(r'^category/(?P<slug>[^/]+)/$',
        views.CategoryArchiveIndexView.as_view(), name='blog_category_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/$',
        views.post_detail_redirect),
    url(r'^(?P<slug>[^/]+)/$', views.post_detail,
        name='blog_post_detail'),
)
