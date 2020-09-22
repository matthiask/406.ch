from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


class PublishedOnListFilter(admin.DateFieldListFilter):
    def choices(self, cl):
        for choice in super(PublishedOnListFilter, self).choices(cl):
            yield choice

        param_dict = {"%sisnull" % self.field_generic: "True"}
        yield {
            "selected": self.date_params == param_dict,
            "query_string": cl.get_query_string(param_dict, [self.field_generic]),
            "display": _("Not published"),
        }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "post_count")
    prepopulated_fields = {"slug": ("title",)}

    def post_count(self, instance):
        return instance.posts.published().count()

    post_count.short_description = _("posts")


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "published_on"
    fieldsets = [
        (
            None,
            {
                "fields": (
                    ("is_active", "is_microblog"),
                    ("title", "slug"),
                    "content",
                    "content_type",
                    "url_override",
                    "categories",
                )
            },
        ),
        (
            _("Meta"),
            {
                "fields": ("created_on", "published_on", "author"),
                "classes": ("collapse",),
            },
        ),
    ]
    list_display = ("title", "is_active", "published_on", "author")
    list_filter = (
        ("published_on", PublishedOnListFilter),
        "is_active",
        "author",
        "categories",
        "content_type",
    )
    prepopulated_fields = {"slug": ("title",)}
    radio_fields = {"content_type": admin.HORIZONTAL}
    search_fields = ("title", "content", "author")

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "author" and kwargs.get("request"):
            kwargs.setdefault("initial", kwargs.get("request").user.get_full_name())

        return super(PostAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "categories":
            kwargs.setdefault("widget", forms.CheckboxSelectMultiple())
        return super(PostAdmin, self).formfield_for_manytomany(
            db_field, request=request, **kwargs
        )


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Post, PostAdmin)
