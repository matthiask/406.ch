from django.conf.urls import patterns, url

from chet.views import AlbumArchiveView


urlpatterns = patterns(
    'chet.views',
    url(
        r'^$',
        AlbumArchiveView.as_view(),
        name='chet_album_archive',
    ),
    url(
        r'^(?P<year>\d+)/(?P<slug>[^/]+)/$',
        'album_detail',
        name='chet_album_detail',
    ),
    url(
        r'^(?P<year>\d+)/(?P<slug>[^/]+)/(?P<pk>\d+)/$',
        'photo_detail',
        name='chet_photo_detail',
    ),
)
