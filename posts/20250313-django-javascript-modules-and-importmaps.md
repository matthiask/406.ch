Title: Django, JavaScript modules and importmaps
Categories: Django, Programming
Draft: remove-this-to-publish

# How I'm using Django, JavaScript modules and importmaps together

I have been spending a lot of time in the last few weeks working on
[django-prose-editor](https://github.com/matthiask/django-prose-editor/). First
I've rebuilt the editor on top of
[Tiptap](https://406.ch/writing/rebuilding-django-prose-editor-from-the-ground-up/)
because I wanted a framework for extending the underlying
[ProseMirror](https://prosemirror.net/) and didn't want to reinvent this
particular wheel. While doing that work I noticed that using JavaScript modules
in the browser would be really nice, but Django's `ManifestStaticFilesStorage`
doesn't yet support rewriting `import` statement in modules out-of-the-box
without opting into the experimental support accessible through subclassing the
storage. A better way to use JavaScript modules with the cache busting offered
by `ManifestStaticFilesStorage` would be
[importmaps](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script/type/importmap).



## Motivation

Finally a solution for shipping reusable JavaScript utilities in third party
apps.


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
      // Tiptap extensions
      Document, Paragraph, HardBreak, Text, Bold, Italic,

      // Prose editor utilities
      Menu, createTextareaEditor, initializeEditors,
    } from "django-prose-editor/editor"

    const extensions = [
      Document, Paragraph, HardBreak, Text, Bold, Italic, Menu,
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


## Problems with the current implementation

- One global importmap when it may not be necessary to merge it in the backend
  since multiple importmaps may happen in the future. Also possibly problematic
  because the code might not expect it.

- Double importmaps when using a widget which works for the admin and for the
  frontend. You have to determine in your Django form field if the code is
  asking for a admin widget or another widget, either by inspecting the
  callstack (very ugly) or by looking if the `widget` argument to the form
  field constructor is set to a admin-specific widget (also somewhat ugly,
  since widgets can be classes, instances, or not set at all)

- Clunky. I would like less manual steps here, but I don't know how.


## Comparison to django-esm

[django-esm](https://github.com/codingjoe/django-esm) assumes you're using
JavaScript modules everywhere and solves the different problem of exposing the
correct paths to those modules to the browser, while supporting both private
modules from the repository itself and modules installed into `node_modules`.
(I hope I got that right.)

It doesn't really address the issue where a third-party **Django** app (that
is, a Python package) ships JavaScript modules.

I myself still use a bundler (see below!) to bundle JavaScript from
`node_modules` etc, so I don't really care too much about this use case yet.
That will probably change in the future though.


## Using bundlers

If you're still using a bundler, [as I do](https://rspack.dev/), you want to
ensure that the `import` isn't actually evaluated by the bundler but left
as-is. The [rspack](https://rspack.dev/) configuration I'm using at the moment
is also documented in the django-prose-editor README but I'm duplicating it
here for convenience:

    :::javascript
    module.exports = {
      // ...
      experiments: { outputModule: true },
      externals: {
        "django-prose-editor/editor": "module django-prose-editor/editor",
      },
    }

The dependency is specified to be "external" (and therefore not to be bundled)
and it's also specified that the dependency is a module and should be loaded
using a static `import` statement. This allows using the
[es-module-shims](https://github.com/guybedford/es-module-shims) module so that
the browsers not yet supporting importmaps ([a few percent at the time of
writing](https://caniuse.com/import-maps)) have a fallback which allows them to
proceed as well.


## Using django-compressor or similar packages

Since the compressor insists on producing old-style JavaScript files and not
modules it cannot be used to bundle the JavaScript modules used for this.
