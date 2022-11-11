from django.contrib.sitemaps import Sitemap

from blog.models import Post


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.published()

    def lastmod(self, obj):
        return obj.published_on
