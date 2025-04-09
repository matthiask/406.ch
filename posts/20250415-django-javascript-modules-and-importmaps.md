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

Developing Django applications that include JavaScript has always been challenging when it comes to properly distributing, loading, and versioning those assets. The traditional approach using Django's `forms.Media` works well for simple use cases, but falls short when dealing with modern JavaScript modules.

The ability to ship reusable JavaScript utilities in third-party Django apps has been a pain point for years. Often developers resort to workarounds like bundling all JS into a single file, using jQuery-style global variables, or requiring complex build processes for consumers of their apps.

Importmaps offer a cleaner solution that works with native browser modules, supports cache busting, and doesn't require complex bundling for simple use cases.

## The history

The conversation around better JavaScript handling in Django has been ongoing for years. A significant milestone was Thibaud Colas' DEP draft:

https://github.com/django/deps/pull/84

There has also been lengthy discussion about whether to improve or deprecate `forms.Media`:

https://forum.djangoproject.com/t/rejuvenating-vs-deprecating-form-media/21285

These conversations highlight the tension between supporting modern JavaScript patterns while maintaining backward compatibility and avoiding over-engineering solutions.

## Prior art

Several approaches have been attempted to solve this problem:

- [django-esm](https://github.com/codingjoe/django-esm) provides a solution for using ES modules with Django
- [django-js-asset](https://github.com/matthiask/django-js-asset/) helps with dependency management and proper JavaScript loading
- The article on [Content Security Policy compliance](https://406.ch/writing/django-admin-apps-and-content-security-policy-compliance/) explores better approaches to JavaScript in Django admin

Django has made incremental improvements, such as:
- Official support for object-based media CSS and JS paths: https://github.com/django/django/commit/4c76ffc2d6c77
- Official support for `Script` tags: https://github.com/django/django/pull/18782

I've previously written about [object-based assets for Django's forms.Media](https://406.ch/writing/object-based-assets-for-django-s-forms-media/), which was a step in the right direction.

## My DEP draft

Building on these efforts, I've submitted my own DEP draft for importmap support:

https://github.com/django/deps/pull/101

This proposal aims to provide a clean, standardized way to handle JavaScript modules in Django applications, leveraging the native importmap specification that browsers now support.

## The current effort

I've already implemented this approach in the alpha version of django-prose-editor. Here's how it works:

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

This means that when your code has `import { ... } from "django-prose-editor/editor"`, the browser automatically loads the file from `/static/django_prose_editor/editor.6e8dd4c12e2e.js`. The hashed filename provides cache busting while the import statement remains clean and consistent.

## Problems with the current implementation

While this approach works, there are several issues to address:


- Different modules may want to use their own importmaps. The discussion is ongoing and it isn't clear if this will happen at all. So for now we're stuck with managing a single importmap in the backend.

- The importmap may be added twice to the HTML when using a widget that works in both the admin and frontend contexts. Currently, if you want to avoid this problem or ugliness you have to determine in your Django form field if the code is requesting an admin widget or another widget, either by inspecting the callstack (very ugly) or by checking if the `widget` argument to the form field constructor is set to an admin-specific widget (also somewhat ugly, since widgets can be classes, instances, or not provided at all).

- It would be nice if we the installation of django-prose-editor didn't have more steps than what we have when installing any other Django widget integration. I'd like a more elegant solution, but haven't found one yet that doesn't introduce too much magic.

## Comparison to django-esm

[django-esm](https://github.com/codingjoe/django-esm) takes a different approach. It assumes you're using JavaScript modules everywhere and solves the problem of exposing the correct paths to those modules to the browser. It supports both private modules from your repository and modules installed in `node_modules`.

However, it doesn't fully address the scenario where a third-party **Django** app (a Python package) ships JavaScript modules that need to be integrated into your application.

I still use a bundler for most of my JavaScript from `node_modules`, so I don't need this specific functionality yet, but it may become more important as browser module support improves.

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
        // Or the following, I'm never sure.
        "django-prose-editor/editor": "import django-prose-editor/editor",
      },
    }

This configuration marks the dependency as "external" (so it won't be bundled) and specifies that it should be loaded as a module using a static `import` statement.

For browser compatibility, you can also include [es-module-shims](https://github.com/guybedford/es-module-shims) to support browsers that don't yet handle importmaps natively (around 5% at the time of writing according to [caniuse.com](https://caniuse.com/import-maps)).

## Using django-compressor or similar packages

Tools like django-compressor aren't well-suited for modern JavaScript modules as they typically produce old-style JavaScript files rather than ES modules. They're designed for a different era of web development and don't integrate well with the importmap approach.

## Conclusion

Using importmaps with Django provides a clean solution for managing JavaScript modules in Django applications, especially for third-party apps that need to ship their own JavaScript. While there are still some rough edges to smooth out, this approach works well and offers a path forward that aligns with modern web standards.

I hope my DEP draft gains traction and we can build official support for importmaps into Django. In the meantime, this approach is working well for django-prose-editor and might be useful for other Django applications that need to ship JavaScript modules.

Have you tried using importmaps with Django? I'd be interested to hear about your experiences and approaches.
