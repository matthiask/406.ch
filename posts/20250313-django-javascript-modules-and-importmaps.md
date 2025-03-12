Title: Django, JavaScript modules and importmaps
Categories:
Draft: remove-this-to-publish

# Django, JavaScript modules and importmaps

## The history

Thibaud Colas' DEP draft:

https://github.com/django/deps/pull/84

The forum thread about rejuvenating vs. deprecating `forms.Media`:

https://forum.djangoproject.com/t/rejuvenating-vs-deprecating-form-media/21285


## Prior art

https://github.com/codingjoe/django-esm

https://github.com/matthiask/django-js-asset/

https://406.ch/writing/django-admin-apps-and-content-security-policy-compliance/

Official support for object-based media CSS and JS paths:
https://github.com/django/django/commit/4c76ffc2d6c77

Official support for `Script` tags:
https://github.com/django/django/pull/18782


https://406.ch/writing/object-based-assets-for-django-s-forms-media/

## My DEP draft

https://github.com/django/deps/pull/101


## The current effort

Already used in the alpha version of django-prose-editor

    :::python
    importmap.update({
        "imports": {
            "django-prose-editor/editor": static_lazy("django_prose_editor/editor.js"),
        }
    })

A minimal editor implementation using this:

    :::javascript
    import {
      Document,
      Paragraph,
      HardBreak,
      Text,
      Bold,
      Italic,
      Menu,
      createTextareaEditor,
      initializeEditors,
    } from "django-prose-editor/editor"

    const extensions = [
      Document,
      Paragraph,
      HardBreak,
      Text,
      Bold,
      Italic,
      Menu,
    ]

    initializeEditors((textarea) => {
      createTextareaEditor(textarea, extensions)
    })


The importmap looks as follows when using Django's `ManifestStaticFilesStorage`
which produces filenames containing the hash of the file's contents for cache
busting:

    :::html
    <script type="importmap">
    {"imports": {
      "django-prose-editor/editor": "/static/django_prose_editor/editor.6e8dd4c12e2e.js"
    }}
    </script>

This means that the line `import { ... } from "django-prose-editor/editor" is automatically rewritten to the real file in `/static/django_prose_editor/` with the current hash
