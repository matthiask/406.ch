Title: Weeknotes (2024 week 18)
Categories: Django, Programming, Weeknotes

## Google Summer of Code has begun

We have a student helping out with adding async support to the [Django Debug
Toolbar](https://github.com/jazzband/django-debug-toolbar/). It's great that
someone can spend some concentrated time to work on this. Tim and others have
done all the necessary preparation work, I'm only helping from the sidelines so
don't thank me.


## Bike to Work

Two teams from my company are participating in the [Bike to Work Challenge
2024](https://www.biketowork.ch/). It's what I do anyway (if I'm not working
from home) but maybe it helps build others some motivation to get on the
bicycle once more. Public transports in the city where I live are great but
I'll always take the bike when I can. I also went on my first mountain bike
ride in a few months yesterday, good fun.


## JSON blobs and referential integrity

The [django-json-schema-editor](https://github.com/matthiask/django-json-schema-editor/) has gained support for referencing Django models. Here's an example schema excerpt:

    {
        ...
        "articles": {
            "type": "array",
            "format": "table",
            "title": _("articles"),
            "minItems": 1,
            "maxItems": 3,
            "items": {
                "type": "string",
                "title": _("article"),
                "format": "foreign_key",
                "options": {
                    "url": "/admin/articles/article/?_popup=1&_to_field=id",
                },
            },
        },
        ...
    }

The ID field is stringly typed; using an integer directly wouldn't work because
the empty string isn't a valid integer.

The problem with referencing models in this way is that there's no way to know
if the referenced object is still around or not, or even to protect it against
deletion. The bundled django-content-editor `JSONPlugin` now supports
automatically generating a `ManyToManyField` with a `through` model which
protects articles from deletion as long as they are referenced from a
`JSONPlugin` instance. The `register_reference` line creates the mentioned
model with an `on_delete=models.PROTECT` foreign key to articles and a
`post_save` handler which updates said references.

    from django_json_schema_editor.plugins import JSONPluginBase, register_reference
    from articles.models import Article

    class JSONPlugin(JSONPluginBase, ...):
        pass

    register_reference(JSONPlugin, "articles", Article)


## Releases since the beginning of April

- [django-json-schema-editor 0.0.14](https://pypi.org/project/django-json-schema-editor/): See above. Also, some styling work and a patch update to the vendorized json-editor.
- [django-content-editor 6.4.6](https://pypi.org/project/django-content-editor/): Many small stylistic fixes. The target indicator when dragging plugins is now also shown when plugins are collapsed. It's now possible to directly drag a plugin to the end, and not just to the second to last position.
- [django-prose-editor 0.3.4](https://pypi.org/project/django-prose-editor/): Switched to the nh3 sanitizer because it's faster and because ProseMirror never emits HTML which has to be cleaned up first. Stopped generating menu items for nodes and marks which aren't in the schema. Added the possibility to reduce the functionality per editor instance. Small tweaks and fixes.
- [django-tree-queries 0.19](https://pypi.org/project/django-tree-queries/): Added support for pre-filtering the tree (much more efficient when only querying a part of the tree). Added support for adding additional fields to the CTE so that you can collect values from ancestors for other fields than the default fields too.
- [FeinCMS 24.4.2](https://pypi.org/project/FeinCMS/): Added support for webp images. Fixed a few of the admin list filters to work with Django 5.
- [django-cabinet 0.14.3](https://pypi.org/project/django-cabinet/): Fixed the support for the `extra_context` argument to our `changelist_view` implementation.
