from markdown2 import markdown

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200)

    class Meta:
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_category_detail', (), {
            'slug': self.slug,
            })


class PostManager(models.Manager):
    def published(self):
        return self.filter(
            published_on__isnull=False,
            published_on__lte=timezone.now,
            )


class Post(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('markdown', _('Markdown')),
        ('html', _('HTML')),
        )

    created_on = models.DateTimeField(_('created on'), default=timezone.now)
    published_on = models.DateTimeField(_('published on'), blank=True,
        null=True)

    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    content_type = models.CharField(_('content type'), max_length=20,
        choices=CONTENT_TYPE_CHOICES, default=CONTENT_TYPE_CHOICES[0][0])
    html = models.TextField(_('HTML'), editable=False)
    author = models.CharField(_('author'), max_length=200, blank=True)
    categories = models.ManyToManyField(Category, related_name='posts',
        verbose_name=_('categories'), blank=True)

    objects = PostManager()

    class Meta:
        get_latest_by = 'published_on'
        ordering = ['-published_on']
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_post_detail', (), {
            'year': self.published_on.strftime('%Y'),
            'month': self.published_on.strftime('%m'),
            'day': self.published_on.strftime('%d'),
            'slug': self.slug,
            })


@receiver(signals.pre_save, sender=Post)
def render_html(instance, **kwargs):
    if instance.content_type == 'markdown':
        instance.html = markdown(instance.content)
    else:
        instance.html = instance.content
