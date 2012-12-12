from django.conf.urls import patterns, include, url
from django.views import generic

from .models import Category, Post


urlpatterns = patterns('',
    url(r'^$', generic.ArchiveIndexView.as_view(
        date_field='published_on',
        queryset=Post.objects.published(),
        ), name='blog_post_archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/$',
        generic.DateDetailView.as_view(
            date_field='published_on',
            month_format='%m',
            queryset=Post.objects.published(),
            ), name='blog_post_detail'),
)
