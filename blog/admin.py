from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class PublishedOnListFilter(admin.DateFieldListFilter):
    def choices(self, cl):
        for choice in super(PublishedOnListFilter, self).choices(cl):
            yield choice

        param_dict = {'%sisnull' % self.field_generic: 'True'}
        yield {
            'selected': self.date_params == param_dict,
            'query_string': cl.get_query_string(
                param_dict, [self.field_generic]),
            'display': _('Not published'),
        }


admin.site.register(
    models.Category,
    prepopulated_fields={'slug': ('title',)},
)
admin.site.register(
    models.Post,
    date_hierarchy='published_on',
    filter_horizontal=('categories',),
    list_display=('title', 'published_on', 'author'),
    list_filter=(
        ('published_on', PublishedOnListFilter),
        'author',
        'categories',
    ),
    prepopulated_fields={'slug': ('title',)},
    search_fields=('title', 'content', 'author')
)
