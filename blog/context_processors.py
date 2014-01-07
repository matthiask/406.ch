from collections import defaultdict

from django.core.urlresolvers import reverse
from django.db.models import Count

from .models import Category, Post


class ContextObject(object):
    def __init__(self, request):
        self.request = request

    def categories(self):
        return Category.objects.all()

    def posts_by_category(self):
        items = Post.categories.through.objects.filter(
            post__in=Post.objects.published(),
        ).values(
            'category__title',
            'category__slug',
        ).annotate(Count('post')).order_by('category__title')

        for row in items:
            yield (
                row['category__title'],
                row['post__count'],
                reverse('blog_category_detail', kwargs={
                    'slug': row['category__slug'],
                }),
            )

    def posts_by_month(self):
        months = defaultdict(int)
        for date in Post.objects.published().values_list(
                'published_on', flat=True):
            months[date.date().replace(day=1)] += 1

        for date, count in sorted(months.items(), reverse=True):
            yield (
                date,
                count,
                reverse('blog_post_archive_month', kwargs={
                    'year': date.strftime('%Y'),
                    'month': date.strftime('%m'),
                }),
            )

    def feed_url(self):
        return self.request.build_absolute_uri(reverse('blog_post_feed'))


def blog(request):
    return {'blog': ContextObject(request)}
