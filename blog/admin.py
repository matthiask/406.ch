from django.contrib import admin

from . import models


admin.site.register(models.Category,
    prepopulated_fields={'slug': ('title',)},
    )
admin.site.register(models.Post,
    date_hierarchy='published_on',
    list_display=('title', 'published_on', 'author'),
    list_filter=('published_on',),
    prepopulated_fields={'slug': ('title',)},
    )
