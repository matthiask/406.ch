from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.ArchiveIndexView.as_view(), name='blog_post_archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/$',
        views.DateDetailView.as_view(), name='blog_post_detail'),
)
