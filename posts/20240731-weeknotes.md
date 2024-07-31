Title: Weeknotes (2024 week 31)
Categories: Django, Programming, Weeknotes
Draft: remove-this-to-publish

I have missed almost two months of weeknotes. I've got some catching up to do.

## [django-prose-editor](https://github.com/matthiask/django-prose-editor/)

I have previously written about the
[ProseMirror](https://prosemirror.net/)-based editor for Django websites
[here](https://406.ch/writing/django-prose-editor-prose-editing-component-for-the-django-admin/).
I have continued working on the project in the meantime. Apart from bugfixes
the big new feature is the support for showing typographic characters. For now
the editor supports showing non-breaking spaces and soft hyphens. The project
seems to get a little more interest after the deprecation of django-ckeditor
has become more well known and the project has even received a contribution by
someone else. It's always a lovely moment when this happens.


## [Traduire](https://github.com/matthiask/traduire)

Traduire (french for «translate») is a web-based platform for editing gettext
translations.

It is intended as a replacement for Transifex, Weblate and comparable products.
It is geared towards small teams or agencies which want to allow their
customers and their less technical team members to update translations.

Traduire profits from the great work done on
[django-rosetta](https://github.com/mbi/django-rosetta/). I would still be
using Rosetta if it would work when used with a container orchestator such as
Kubernetes. Since all application storage is ephemeral that doesn't work,
translation editing and deployment have to be separated.

It is built using Django and relies on [polib](https://pypi.org/project/polib/)
to do the heavy lifting.

This is a project which might also be interesting for others. I would
especially appreciate it if someone could contribute an easier way to get it up
and running, e.g. using a Docker Compose configuration or something. I am using
Kubernetes and GitOps to host it, but that's not straightforward at all.
Really, all that's needed to run it is a Django host with any database which is
supported by Django. I prefer using PostgreSQL because I have it, but sqlite
etc. work just as well.


## Releases since the second week of June

- [django-translated-fields 0.13](https://pypi.org/project/django-translated-fields/):
  Nothing much except for CI and pre-commit updates. The implementation
  continues to be rock-solid and basically unchanged.
- [django-content-editor 7.0.6](https://pypi.org/project/django-content-editor/):
  Tweaks and fixes to the new interface. Added better scrolling behavior when
  dragging content around. The editor now also supports colorized icons which
  helps quickly understanding the structure of some content when there are many
  plugins.
- [blacknoise 1.0.2](https://pypi.org/project/blacknoise/):
  Fixed a few bugs in the ``blacknoise.compress`` utility and started running
  the testsuite on GitHub actions.
  [whitenoise](https://github.com/evansd/whitenoise/) has been friendly-forked
  as [ServeStatic](https://github.com/Archmonger/ServeStatic) and I'm
  definitely having a close look at this project as well, but blacknoise is
  simple and works well, so I'm not convinced that switching back to the much
  larger project (in terms of amounts of code) is an improvement now.
- [django-authlib](https://pypi.org/project/django-authlib/):
  Minor bugfixes.
- [feincms3](https://pypi.org/project/feincms3/):
  Allowed registering plugin models with the renderer which aren't supposed to
  be fetched from the database. This is especially useful when used together
  with JSON plugins, where the individual JSON plugins are created as proxies
  for the underlying Django model and fetched all at once. Disabled the version
  check on our CKEditor plugin. Still, really stop using CKEditor 4 if you want
  to use maintained software.
- [FeinCMS 24.7.1](https://pypi.org/project/FeinCMS/):
  Small bugfixes, and made the Read the Docs build work correctly.
- [django-debug-toolbar 4.4.x](https://pypi.org/project/django-debug-toolbar/):
  The toolbar continues to be a nice project to work on. Fixed a few edge cases
  in the new alerts panel.
- [django-admin-ordering 0.18.2](https://pypi.org/project/django-admin-ordering/):
  The value of ``ordering_field`` now has additional sanity checks.
- [django-cabinet 0.16](https://pypi.org/project/django-cabinet/):
  cabinet now supports exporting a folder as a ZIP file while preserving the
  structure you see in the CMS instead of the structure on the file system. The
  inline upload form has been dropped from the ``CabinetForeignKey`` widget
  because the folder dropdown slowed down the page a lot when used on a site
  with many folders. Using the raw ID fields popup isn't that bad.
- [django-prose-editor 0.6.2](https://pypi.org/project/django-prose-editor/):
  See above.
