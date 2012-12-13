from django.views import generic

from .models import Category, Post


class PostMixin(object):
    date_field = 'published_on'
    month_format = '%m'

    def get_queryset(self):
        return Post.objects.published()


class ArchiveIndexView(PostMixin, generic.ArchiveIndexView):
    pass


class DateDetailView(PostMixin, generic.DateDetailView):
    pass
