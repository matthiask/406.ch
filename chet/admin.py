from django.contrib import admin

from chet.models import Album, Photo


admin.site.register(
    Album,
    date_hierarchy='date',
    list_display=('title', 'date', 'is_active', 'is_public'),
    list_editable=('is_active', 'is_public'),
    list_filter=('is_active', 'is_public'),
    prepopulated_fields={'slug': ('title',)},
    search_fields=('title',),
)
admin.site.register(
    Photo,
    date_hierarchy='shot_on',
    # TODO add thumb
    list_display=(
        '__unicode__', 'shot_on', 'is_active', 'is_public', 'is_dark'),
    list_editable=('is_active', 'is_public', 'is_dark'),
    list_filter=('is_active', 'is_public', 'album', 'is_dark'),
    search_fields=('title',),
)
