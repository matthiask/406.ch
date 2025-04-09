Title: Weeknotes (2025 week 15)
Categories: Django, Programming, Weeknotes


## Djangonaut Space

We have already reached the final week of the [Djangonaut
Space](https://djangonaut.space/) session 4. I had a great time as a navigator
and am looking forward to participate more, but for now I'm also glad that I do
not have the additional responsibility at least for the close future.

We have done great work on the
[django-debug-toolbar](https://pypi.org/project/django-debug-toolbar/) in our
group, more is to come.


## Progress on the prose editor

I have done much work on
[django-prose-editor](https://pypi.org/project/django-prose-editor/) in the
last few weeks and after a large list of alphas and betas I'm nearing a state
which I want to release into the wild.

The integration has been completely rethought (again) and now uses JavaScript
modules and importmaps. The ground work to support all of that in Django has
been laid in [django-js-asset](https://pypi.org/project/django-js-asset/).

The nice thing about using JavaScript modules and importmaps is that we now
have an easy way to combine the power of modern JavaScript customization with
easy cache busting using Django's `ManifestStaticFilesStorage`. A longer post
on this is brewing and I hope to have it ready soon-ish.

As a sneak peek, here's the way it works:

    :::python
    from django_prose_editor.fields import ProseEditorField

    content = ProseEditorField(
        extensions={
            "Bold": True,
            "Italic": True,
            "BulletList": True,
            "Link": True,
        },
        # sanitize=True is the default when using extensions
    )

The nice thing about it is that the sanitization allowlist for
[nh3](https://github.com/messense/nh3) only includes tags and attributes which
are enabled via the `extensions` dict. So, you don't have to do anything else
to be safe from XSS etc.

Check out the pre-releases on
[PyPI](https://pypi.org/project/django-prose-editor/#history) or have a look at
the [documentation](https://django-prose-editor.readthedocs.io/) to learn more
about this project!


## Using Claude Code

I have been using Claude Code (without editor integrations, thank you very
much) more and more. It's a good coding companion when it comes to throwing
around ideas, drafting docs and writing unit tests including integration tests.

Sometimes I'm really surprised at how good it is. Other times... less so. The
tool often finds a way to get tests passing, but when the editor integration
tests directly manipulate `innerHTML` and then Claude proclaims that
interacting with the editor is now shown to work I have to chuckle a bit. And
when I insist on doing what I mean and not just finding broken workarounds it
doesn't really change anything. After spinning more we're always back where we
started.

I am somewhat glad that this is where we're at now. I'm not 100% sure if it's
progress. At least it's surprisingly funny at times.


## Releases

I haven't written a regular weeknotes entry since the end of January, so
naturally the list here is longer than usual.

- [feincms3-forms 0.5.1](https://pypi.org/project/feincms3-forms/): I
  inadvertently bumped the Django dependency without actually wanting that;
  this patch release reverts that (while adding official support for new Django
  and Python versions).
- [django-mptt 0.17](https://pypi.org/project/django-mptt/): Mariusz has done
  all the hard work for supporting newer versions of Django. I just had to
  press the release button. That being said, four years after marking the
  package as unmaintained I'm still maintaining it. At least I don't get
  complaints anymore...
- [django-json-schema-editor
  0.4](https://pypi.org/project/django-json-schema-editor/): Added a dependency
  on the pre-release of django-prose-editor and added a test suite including
  integration tests so that we actually now when stuff breaks the next time!
- [django-debug-toolbar 5.1](https://pypi.org/project/django-debug-toolbar/):
  See above.
- [feincms3-data](https://pypi.org/project/feincms3-data/): Added fixes to dump
  distinct objects. Spent more time than useful on the Django change which
  added a final newline to JSON-serialized data.
- [django-js-asset 3.1.2](https://pypi.org/project/django-js-asset/):
  Importmaps support, added a `static_lazy` helper which is useful to define
  module-scoped static URLs. The later wouldn't work with the
  `ManifestStaticFilesStorage` because the manifest doesn't yet exist when
  `collectstatic` runs, so the actual evaluation of static URLs has to be
  postponed. The lazy version solves this nicely.
- [feincms3-sites 0.21.1](https://pypi.org/project/feincms3-sites/) and [feincms3-language-sites 0.4.1](https://pypi.org/project/feincms3-language-sites/): See the relevant [TIL](https://406.ch/writing/til-tools-exist-which-do-not-lowercase-domain-names-when-requesting-websites-over-http-s/) blogpost.
