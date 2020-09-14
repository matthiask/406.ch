from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from .models import Category, Post


class PostFeed(Feed):
    feed_type = Atom1Feed

    def title(self):
        return "Matthias Kestenholz"

    def link(self):
        return reverse("blog_post_feed")

    def items(self):
        return Post.objects.published()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.html


class CategoryFeed(PostFeed):
    def get_object(self, request, slug):
        return get_object_or_404(Category, slug=slug)

    def title(self, obj):
        return "Matthias Kestenholz: Posts about %s" % obj

    def link(self, obj):
        return reverse("blog_category_feed", kwargs={"slug": obj.slug})

    def items(self, obj):
        return Post.objects.published().filter(categories=obj)[:20]
