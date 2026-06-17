Title: The 2026 way of using importmaps in Django
Categories: Django, Programming

I last wrote about [Django, JavaScript modules and importmaps](/writing/django-javascript-modules-and-importmaps/) in May 2025, slightly over a year ago.

The main topic of this post is the [django-js-asset](https://github.com/feincms/django-js-asset) 4.0 release. The library is used in many places, some of the more well-known packages using it are [django-mptt](https://github.com/django-mptt/django-mptt) and [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor).
I have since done a lot of work evolving the ways of integrating importmaps but the efforts to standardize upon an approach have stalled a bit.
The main reason for this, apart from time and energy, was that I wasn't really all that happy with the global importmap. When I had only a few modules using the importmap facility, I didn't care all that much. Now that the recently released [django-content-editor 9.0](https://github.com/feincms/django-content-editor) also uses importmaps for shipping a refactored, much more modular JavaScript implementation while still keeping all the benefits of cache busting using `ManifestStaticFilesStorage`[^manifest], having a global importmap got annoying. The content editor JavaScript is only used within the [Django administration interface](/writing/the-django-admin-is-a-cms/), but when using a single global importmap object, the importmap entries were always there on each page that used an importmap at all.

[^manifest]: Without having to do any overrides to enable ESM support.

A better solution was needed. I'm a big fan of using [`forms.Media`](https://docs.djangoproject.com/en/6.1/topics/forms/media/) for collecting CSS and JavaScript from widgets, forms and utilities. It helps me avoid inline JavaScript since [at least 2017](https://406.ch/writing/django-admin-apps-and-content-security-policy-compliance/). I'm not using it for site-wide CSS and JavaScript, I'm still transpiling, PostCSS-ing and bundling the assets using [rspack](https://rspack.rs/) as for example written about [here](https://406.ch/writing/avoiding-empty-javascript-files-in-css-only-entrypoints-from-rspack-builds/) and [here](https://406.ch/writing/how-i-m-bundling-frontend-assets-using-django-and-rspack-these-days/).


## Why importmaps?

A quick refresher on why this matters at all. Django's `ManifestStaticFilesStorage` hashes the contents of each file into its name for cache busting, but out of the box it doesn't rewrite the `import` statements inside JavaScript modules. Importmaps bridge the gap: your code imports a stable name:

    :::javascript
    import { initializeEditors } from "django-prose-editor/editor"

and the importmap tells the browser where that name actually lives:

    :::html
    <script type="importmap">
    {"imports": {
      "django-prose-editor/editor": "/static/django_prose_editor/editor.6e8dd4c12e2e.js"
    }}
    </script>

So the import stays clean and constant while the file behind it can get a new hash on every deploy.


## django-js-asset 4.0

The updated [django-js-asset 4.0](https://github.com/feincms/django-js-asset) doesn't ship the old, global importmap at all. This means the upgrade might require some work. Instead of one importmap shared across the whole site, you now get a specific importmap assembled for the context at hand -- either by Django itself when it collects the media of your forms, widgets and the admin, or explicitly by you in a view or context processor. The building block in both cases is the `ImportMap` object; when it travels through `js_asset.Media` (a subclass of `django.forms.Media`) the maps are automatically merged into a single `<script type="importmap">`, by customizing and extending what Django does already when merging media instances.

The [release notes](https://github.com/feincms/django-js-asset/blob/main/CHANGELOG.rst) go into more detail.

## In practice

If you're using a package such as [django-prose-editor](https://github.com/feincms/django-prose-editor) in the Django admin you don't have to do anything, things should just work.



If you're using such a package outside the admin, you have to remove `"js_asset.context_processors.importmap"` from your list of context processors. On one particular website the prose editor is the only package with importmap entries outside the admin, so I have to add the `importmap` to the template context myself:


    :::python
    from django_prose_editor.widgets import importmap

    def view(request, ...):
        return render(request, "template.html", {
            # ...
            "importmap": importmap,
        })

The template then just renders it in the `<head>`:

    :::html
    ... {{ importmap }}</head>

On a different site, I have a slightly more involved scenario where I previously used `importmap.update(...)` to add my own entries to the importmap. There, I'm using a custom context processor to always add these entries to the importmap too:

    :::python
    from django_prose_editor.widgets import importmap as dpe_importmap
    from js_asset import ImportMap, static_lazy

    _site_importmap = ImportMap({
        "imports": {
            "my-module": static_lazy("my-module.js"),
        }
    })
    _importmap = dpe_importmap | _site_importmap

    def importmap(request):
        return {"importmap": _importmap}

This importmap is merged once at server startup and then served repeatedly to the client. Because we use the lazy version of the `static` function we can do this during startup and not worry about files not yet collected by `collectstatic` -- we'll get the correct paths later.

On the same site as the previous example, I also have an admin inline which requires some JavaScript and also an importmap:

    :::python
    from django.contrib import admin
    from django.forms import Script
    from js_asset import Media, ImportMap

    # Initializing this once. Not necessary but I like it better that way.
    _importmap = ImportMap({
        "imports": {
            # ...
        }
    })

    class ModelInline(admin.StackedInline):
        @property
        def media(self):
            return Media(
                js=[
                    _importmap,
                    Script("module.js", type="module"),
                ]
            )

As of 4.0, `JS` and `CSS` produce Django's own `Script` and `Stylesheet` objects, so you can import and use `Script` directly from `django.forms` as shown above (on Django 4.2–5.1, import it from `js_asset` instead, which backports it). The familiar `JS("module.js", {"type": "module"})` wrapper still works unchanged if you prefer it — it just takes a positional dict instead of keyword arguments.

Here, it's really important to use the `js_asset.Media` and not `django.forms.Media`. `js_asset.Media` knows how to handle importmaps -- all importmaps are collected from all media lists, merged and added to the output before all other CSS and especially JavaScript. The reason for that is that browsers only honour a single importmap per page, and it really has to appear before all JavaScript modules referencing any entries in the importmap.

The nice thing about `js_asset.Media` is that it doesn't have to appear first in the list of media classes which are merged -- it can also appear in the middle or last, and still can do its magic after all `Media` objects have been merged into a single one.

The rest is handled by Django itself, since it already supports collecting media assets. The missing piece was just the importmap object and the `js_asset.Media` class which knows how to special case them, and which -- through the power of overriding `__add__` and `__radd__` takes over all the other media instances.



## What's next

I haven't yet used CSP nonces using [`{% csp_nonce_attr media %}`](https://docs.djangoproject.com/en/6.1/ref/templates/builtins/#std-templatetag-csp_nonce_attr) in production myself, but it should just work, even with importmaps and everything else. Given that I have a passing test suite I have no reason to believe it doesn't already work, but I'd like to have a confirmation.

I'm hoping to standardize some more. If we could get something like this in Django core that would be really nice. Maybe I'll be able to work on that at [Django on the Med 🏖️](https://djangomed.eu/). Since no browser supports multiple importmaps as of today having multiple implementations of importmaps in the Django ecosystem will lead to trouble down the road. I think there is a clear case to be made for importmap support in Django and I would obviously love it if the approach implemented today in django-js-asset would be the basis for the official solution.
