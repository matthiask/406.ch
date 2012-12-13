from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.ArchiveIndexView.as_view(), name='blog_post_archive'),
    url(r'^(?P<year>\d{4})/$',
        views.YearArchiveView.as_view(), name='blog_post_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.MonthArchiveView.as_view(), name='blog_post_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.DayArchiveView.as_view(), name='blog_post_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/$',
        views.DateDetailView.as_view(), name='blog_post_detail'),
    url(r'^category/(?P<slug>[^/]+)/$',
        views.CategoryArchiveIndexView.as_view(), name='blog_category_detail'),
)
