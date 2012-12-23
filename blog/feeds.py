from django.core.urlresolvers import reverse_lazy
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext_lazy as _

from .models import Post


class PostFeed(Feed):
    feed_type = Atom1Feed
    title = _('406 NOT ACCEPTABLE')
    link = reverse_lazy('blog_post_feed')
    #subtitle = ''

    def items(self):
        return Post.objects.published()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.html
