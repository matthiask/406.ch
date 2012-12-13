from collections import defaultdict

from django.core.urlresolvers import reverse
from django.db.models import Sum

from .models import Category, Post


class ContextObject(object):
    def __init__(self, request):
        self.request = request

    def categories(self):
        return Category.objects.all()

    def posts_by_month(self):
        months = defaultdict(int)
        for date in Post.objects.published().values_list(
                'published_on', flat=True):
            months[date.date()] += 1

        for date, count in sorted(months.items(), reverse=True):
            yield (
                date,
                count,
                reverse('blog_post_archive_month', kwargs={
                    'year': date.strftime('%Y'),
                    'month': date.strftime('%m'),
                    })
                )


def blog(request):
    return {'blog': ContextObject(request)}
