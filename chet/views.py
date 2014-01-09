from django.shortcuts import get_object_or_404, render
from django.views import generic

from chet.models import Album, Photo


def visible_albums(user):
    if user.is_staff:
        return Album.objects.active()
    else:
        return Album.objects.public()


def visible_photos(user):
    if user.is_staff:
        return Photo.objects.active()
    else:
        return Photo.objects.public()


class AlbumMixin(object):
    allow_empty = True
    date_field = 'date'
    make_object_list = True
    month_format = '%m'
    paginate_by = 10
    paginate_orphans = 3

    def get_queryset(self):
        return visible_albums(self.request.user)


class AlbumArchiveView(AlbumMixin, generic.ArchiveIndexView):
    pass


def album_detail(request, year, slug):
    album = get_object_or_404(
        visible_albums(request.user),
        date__year=year,
        slug=slug,
    )

    return render(request, 'chet/album_detail.html', {
        'album': album,
        'object': album,
        'photos': visible_photos(request.user).filter(album=album),
    })


def photo_detail(request, year, slug, photo):
    photo = get_object_or_404(
        visible_photos(request.user),
        album__date__year=year,
        album__slug=slug,
        pk=photo,
    )

    return render(request, 'chet/photo_detail.html', {
        'photo': photo,
        'object': photo,
    })
