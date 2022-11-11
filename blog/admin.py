from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from blog import models


class PublishedOnListFilter(admin.DateFieldListFilter):
    def choices(self, cl):
        yield from super().choices(cl)

        param_dict = {"%sisnull" % self.field_generic: "True"}
        yield {
            "selected": self.date_params == param_dict,
            "query_string": cl.get_query_string(param_dict, [self.field_generic]),
            "display": _("Not published"),
        }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "post_count")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]

    @admin.display(description=_("posts"))
    def post_count(self, instance):
        return instance.posts.published().count()


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

        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Post, PostAdmin)
