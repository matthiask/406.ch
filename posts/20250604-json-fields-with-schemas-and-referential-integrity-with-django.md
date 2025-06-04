Title: Preserving referential integrity with JSON fields and Django
Categories: Django, Programming, feincms

## Motivation

The great thing about using [feincms3](https://feincms3.readthedocs.io/) and
[django-content-editor](https://django-content-editor.readthedocs.io/) is that
CMS plugins are Django models -- if using them you immediately have access to
the power of Django's ORM and Django's administration interface.

However, using one model per content type can be limiting on larger sites.
Because of this [we](https://feinheit.ch/) like using JSON plugins with
schemas for more fringe use cases or for places where we have richer data but
do not want to write a separate Django app for it. This works well as long as
you only work with text, numbers etc. but gets a bit ugly once you start
referencing Django models because you never know if those objects are still
around when actually using the data stored in those JSON fields.

Django has a nice
[`on_delete=models.PROTECT`](https://docs.djangoproject.com/en/5.2/ref/models/fields/#django.db.models.ForeignKey.on_delete)
feature, but that of course only works when using real models. So, let's bridge
this gap and allow using foreign key protection with data stored in JSON
fields!


## Models

First, you have to start using the
[django-json-schema-editor](https://github.com/matthiask/django-json-schema-editor)
and specifically its `JSONField` instead of the standard Django `JSONField`. The most important difference between those two is that the schema editor's field wants a JSON schema. So, for the sake of an example, let's assume that we have a model with images and a model with galleries. Note that we're omitting many of the fields actually making the interface nice such as titles etc.

    :::python
    from django.db import models
    from django_json_schema_editor.fields import JSONField

    class Image(models.Model):
        image = models.ImageField(...)

    gallery_schema = {
        "type": "object",
        "properties": {
            "caption": {"type": "string"},
            "images": {
                "type": "array",
                "format": "table",
                "minItems": 3,
                "items": {
                    "type": "string",
                    "format": "foreign_key",
                    "options": {
                        # raw_id_fields URL:
                        "url": "/admin/myapp/image/?_popup=1&_to_field=id",
                    },
                },
            },
        },
    }

    class Gallery(models.Model):
        data = JSONField(schema=gallery_schema)

Now, if we were to do it by hand, we'd define a `through` model for a
`ManyToManyField` linking galleries to images, and adding a
`on_delete=models.PROTECT` foreign key to this through model's `image` foreign
key and we would be updating this many to many table when the `Gallery` object
changes. Since that's somewhat [boring but also tricky code](https://github.com/matthiask/django-json-schema-editor/blob/4bc1ab0cf44eda4c0e824f96f2bd08cd94832c1c/django_json_schema_editor/fields.py#L9-L47) I have already written it (including unit tests of course) and all that's left to do is define the linking:

    :::python
    Gallery.register_data_reference(
        # The model we're referencing:
        Image,
        # The name of the ManyToManyField:
        name="images",
        # The getter which returns a list of stringified primary key values or nothing:
        getter=lambda obj: obj.data.get("images"),
    )

Now, attempting to delete an image which is still used in a gallery somewhere will raise [ProtectedError](https://docs.djangoproject.com/en/5.2/ref/exceptions/#django.db.models.ProtectedError) exceptions. That's what we wanted to achieve.

## Using a gallery instance

When you have a gallery instance you can now use the `images` field to fetch
all images and use the order from the JSON data:

    :::python
    def gallery_context(gallery):
        images = {str(image.pk): image for image in gallery.images.all()}
        return {
            "caption": gallery.data["caption"],
            "images": [images[pk] for pk in gallery.data["images"]],
        }


## JSONPluginBase and JSONPluginInline

I would generally do the instantiation of models slightly differently and use
`django-json-schema-editor`'s `JSONPluginBase` and `JSONPluginInline` which
offer additional niceties such as streamlined JSON models with only one backing database table (using [proxy
models](https://docs.djangoproject.com/en/5.2/topics/db/models/#proxy-models)) and supporting not just showing the primary key of referenced model instances but also their `__str__` value.

The example above would have to be changed to look more like this:

    :::python
    from django_json_schema_editor import JSONPluginBase

    class JSONPlugin(JSONPluginBase, ...):
        pass

    JSONPlugin.register_data_reference(...)

    Gallery = JSONPlugin.proxy("gallery", schema=gallery_schema)

However, that's not documented yet so for now you unfortunately have to read
the [code and the test
suite](https://github.com/matthiask/django-json-schema-editor), sorry for that.
It's used heavily in production though so if you start using it it won't
suddenly start breaking in the future.
