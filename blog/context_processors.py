from django.urls import reverse

from blog.models import Category, Post


class ContextObject:
    def __init__(self, request):
        self.request = request

    def categories(self):
        return Category.objects.all()

    def years_with_posts(self):
        return [
            date.year
            for date in Post.objects.published().datetimes(
                "published_on", "year", "DESC"
            )
        ]

    def feed_url(self):
        return self.request.build_absolute_uri(reverse("blog_post_feed"))


def blog(request):
    return {"blog": ContextObject(request)}
