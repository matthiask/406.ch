from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class VisibilityModel(models.Model):
    is_active = models.BooleanField(_('is active'), default=True)
    is_public = models.BooleanField(_('is public'), default=False)

    class Meta:
        abstract = True


class AlbumManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def public(self):
        return self.filter(is_active=True, is_public=True)


class Album(VisibilityModel):
    created_on = models.DateTimeField(_('created on'), default=timezone.now)
    date = models.DateField(_('date'), default=timezone.now)
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200, unique=True)

    objects = AlbumManager()

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = _('album')
        verbose_name_plural = _('albums')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('chet_album_detail', kwargs={
            'year': self.date.strftime('%Y'),
            'slug': self.slug,
        })


class PhotoManager(models.Manager):
    def active(self):
        return self.filter(
            is_active=True,
            album__is_active=True,
        )

    def public(self):
        return self.filter(
            is_active=True,
            album__is_active=True,
            is_public=True,
            album__is_public=True,
        )


class Photo(VisibilityModel):
    created_on = models.DateTimeField(_('created on'), default=timezone.now)
    file = models.ImageField(_('file'), upload_to='chet/photos/%Y/%m/')

    album = models.ForeignKey(
        Album, verbose_name=_('album'), related_name='photos')
    shot_on = models.DateTimeField(_('shot on'), default=timezone.now)
    title = models.CharField(_('title'), max_length=200, blank=True)

    is_dark = models.BooleanField(
        _('is dark'), default=False,
        help_text=_('Dark images are shown on a light background.'))

    objects = PhotoManager()

    class Meta:
        get_latest_by = 'created_on'
        ordering = ['-created_on']
        verbose_name = _('photo')
        verbose_name_plural = _('photos')

    def __unicode__(self):
        return self.title or self.file.name

    def get_absolute_url(self):
        return reverse('chet_photo_detail', kwargs={
            'year': self.album.date.strftime('%Y'),
            'slug': self.album.slug,
            'photo': self.pk,
        })
