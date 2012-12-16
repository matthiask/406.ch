from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .models import Category, Post


class PostMixin(object):
    allow_empty = True
    date_field = 'published_on'
    make_object_list = True
    month_format = '%m'
    paginate_by = 25
    paginate_orphans = 1

    def get_queryset(self):
        return Post.objects.published()


class ArchiveIndexView(PostMixin, generic.ArchiveIndexView):
    pass


class YearArchiveView(PostMixin, generic.YearArchiveView):
    template_name_suffix = '_archive'


class MonthArchiveView(PostMixin, generic.MonthArchiveView):
    template_name_suffix = '_archive'


class DayArchiveView(PostMixin, generic.DayArchiveView):
    template_name_suffix = '_archive'


class CategoryArchiveIndexView(ArchiveIndexView):
    template_name_suffix = '_archive'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return super(CategoryArchiveIndexView, self).get_queryset().filter(
            categories=self.category)

    def get_context_data(self, **kwargs):
        return super(CategoryArchiveIndexView, self).get_context_data(
            category=self.category,
            **kwargs)


def post_detail_redirect(request, year, month, day, slug):
    return redirect(get_object_or_404(Post.objects.published(), slug=slug))


def post_detail(request, slug):
    instance = get_object_or_404(Post.objects.published(), slug=slug)
    return render(request, 'blog/post_detail.html', {
        'post': instance,
        })
