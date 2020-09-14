from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .models import Category, Post


class PostMixin(object):
    allow_empty = True
    date_field = "published_on"
    make_object_list = True
    month_format = "%m"
    archive = None

    def get_queryset(self):
        if self.archive is False:
            posts = Post.objects.current()
        elif self.archive is True:
            posts = Post.objects.archive()
        else:
            posts = Post.objects.published()

        if self.request.GET.get("q"):
            posts &= Post.objects.search(self.request.GET["q"])
        if self.request.GET.get("o") == "chronological":
            return posts.reverse()
        return posts


class ArchiveIndexView(PostMixin, generic.ArchiveIndexView):
    pass


class YearArchiveView(PostMixin, generic.YearArchiveView):
    template_name_suffix = "_archive"


class MonthArchiveView(PostMixin, generic.MonthArchiveView):
    template_name_suffix = "_archive"


class DayArchiveView(PostMixin, generic.DayArchiveView):
    template_name_suffix = "_archive"


class CategoryArchiveIndexView(ArchiveIndexView):
    template_name_suffix = "_archive"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return (
            super(CategoryArchiveIndexView, self)
            .get_queryset()
            .filter(categories=self.category)
        )

    def get_context_data(self, **kwargs):
        return super(CategoryArchiveIndexView, self).get_context_data(
            category=self.category, **kwargs
        )


def post_detail_redirect(request, year, month, day, slug):
    return redirect(get_object_or_404(Post.objects.published(), slug=slug))


def post_detail(request, slug):
    if request.user.is_staff:
        posts = Post.objects.all()
    else:
        posts = Post.objects.published()

    instance = get_object_or_404(posts, slug=slug)

    return render(request, "blog/post_detail.html", {"post": instance})
