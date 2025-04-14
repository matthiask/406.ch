Title: Customizing Django admin fieldsets without fearing forgotten fields
Categories: Django, Programming

When defining [fieldsets on Django modeladmin classes](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets) I always worry that I forget updating the fieldsets later when adding or removing new model fields, and not without reason: It has already happened to me several times. Forgetting to remove fields is mostly fine because system checks will complain about it, forgetting to add fields may be real bad. A recent example was a crashing website because a required field was missing from the admin and therefore was left empty when creating new instances!

I have now published another Django package which solves this by adding support for specifying the special `"__remaining__"` field in a fieldsets definition. The `"__remaining__"` placeholder is automatically replaced by all model fields which haven't been explicitly added already or added to `exclude`[^1].

Here's a short example for a modeladmin definition using django-auto-admin-fieldsets:

    :::python
    from django.contrib import admin
    from django_auto_admin_fieldsets.admin import AutoFieldsetsModelAdmin
    from app import models

    @admin.register(models.MyModel)
    class MyModelAdmin(AutoFieldsetsModelAdmin):
        # Define fieldsets as usual with a placeholder
        fieldsets = [
            ("Basic Information", {"fields": ["title", "slug"]}),
            ("Content", {"fields": ["__remaining__"]}),
        ]

I have used Claude Code a lot for the code and the package, and as always, I had to fix bugs and oversights. I hope it didn't regurgitate the code of an existing package -- I searched for an existing solution first but didn't find any.

The package is available on [PyPI](https://pypi.org/project/django-auto-admin-fieldsets/) and is developed on [GitHub](https://github.com/matthiask/django-auto-admin-fieldsets), at least for the time being.

[^1]: Autocreated fields such as surrogate primary keys or fields which aren't editable are also excluded automatically of course.
