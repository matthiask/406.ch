Title: Django admin tip: Adding links to related objects in change forms
Categories: Django, Programming

# Django admin tip: Adding links to related objects in change forms

Any issue which came up on the Django Forum and Discord is how to add links to
other objects to the Django administration interface. It's something I'm doing
often and I want to share the pattern I'm using.

It's definitely not rocket science and there are probably better ways to do it,
but this one works well for me.


## Method 1: Override the change form template

In one project users can be the editor of exactly one organization. The link
between organizations and users is achieved using a `Editor` model with a
`ForeignKey(Organization)` and a `OneToOneField(User)`.

I wanted to add a link to the organization page at the bottom of the user form.
An easy way to achieve this is to add a template at
`templates/admin/auth/user/change_form.html` (or something similar if you're
using a custom user model):

    :::html+django
    {% extends "admin/change_form.html" %}

    {% block after_related_objects %}
    {{ block.super }}

    {% if original.editor %}
    <fieldset class="module aligned">
    <h2>Organization</h2>
    <div class="form-row">
      <a href="{% url 'admin:organizations_organization_change' original.editor.organization.pk %}">{{ original.editor.organization }}</a>
    </div>
    </fieldset>
    {% endif %}

    {% endblock after_related_objects %}

The `original` context variable contains the object being edited. The `editor`
attribute is the reverse accessor for the `OneToOneField` mentioned above.


## Method 2: Add a method to the model admin class returning a HTML blob

A terrible but also nice way is to add a method to the `ModelAdmin` class which
returns the HTML containing the links you want, and adding the name of the
method to `readonly_fields`. This is even mentioned in [the official
`readonly_fields`
documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.readonly_fields)
but I discovered this by accident a few years back.

The method name doesn't have to be added anywhere else, not to `fields` nor do
you have to define `fieldsets` for this to work. Just adding it to
`readonly_fields` appends it to the end of the form, before any eventual
inlines you're using.

    :::python
    from django.template.loader import render_to_string
    from app import models

    @admin.register(models.Class)
    class ClassAdmin(admin.ModelAdmin):
        list_display = ["name", "language_code"]
        readonly_fields = ["admin_show_custom_districts"]

        @admin.display(description=_("districts")
        def admin_show_custom_districts(self, obj):
            return render_to_string(
                "admin/admin_show_custom_districts.html",
                {"custom_districts": obj.customdistrict_set.all()},
            )
