Title: Weeknotes (2023 week 33)
Date: 2023-08-20
Categories: Django, Programming, Weeknotes, feincms

I'm not sure if I should call these posts weeknotes when I see the posting schedule, but oh well. Keep expectations up but also practice forgiveness when not meeting them, it's fine really.

## `py_modules` using hatchling

I converted [speckenv](https://github.com/matthiask/speckenv/) and [django-sitemaps](https://github.com/matthiask/django-sitemaps/) after finding the following very helpful post on packaging projects consisting of Python modules without any packages: [Packaging of single Python module projects with Hatch/Hatchling](https://www.stefaanlippens.net/single-python-module-packaging-hatch.html). It's very easy in hindsight, but that's basically always the case.

The relevant part is including the files in the build:

    :::toml
    [tool.hatch.build]
    include = [
      "speckenv.py",
      "speckenv_django.py",
      "speckenv_django_patch.py",
    ]

That's all.

## django-debug-toolbar and tracing the cause of DB queries in an async world

I have also started investigating what would have to be changed in django-debug-toolbar to make it fully support async Django. We currently patch Django's database cursors per thread, which works fine in sync Django land to attribute SQL queries to a particular request/response cycle.

Since async Django executes DB queries in a thread pool executor and the rest of the work happens inside awaitables (async land) I don't immediately see a way how we could do the same thing. It doesn't seem possible to find out which task spawned another task (without dropping down to C?) but maybe there's something I'm overlooking. I hope that someone smarter than me finds a way :-) or that I find the time and motivation to either find a way using Python or using C/Rust/whatever.

## Releases

- [feincms3-sites 0.16](https://pypi.org/project/feincms3-sites/): I added basic support for `i18n_patterns` when using feincms3-sites with its `default_language_middleware` (which allows setting a default language per site in case there is no other mechanism overriding it, such as `i18n_patterns`).
- [feincms3-cookiecontrol 1.4.1](https://pypi.org/project/feincms3-cookiecontrol/): The privacy policy is now linked inside the banner text instead of adding a link after the text. Looks much nicer.
- [speckenv 5.0](lhttps://pypi.org/project/speckenv/): Finally released changes made a long time ago which make one edge case when parsing settings less surprising.
- [django-debug-toolbar 4.2](https://pypi.org/project/django-debug-toolbar/): I didn't do much work here again, mostly code reviews, some changes to the ruff configuration and general polishing. I also didn't do the release itself, that was handled by Tim. Thanks!
- [FeinCMS 23.8](https://pypi.org/project/FeinCMS/): Fixes for Pillow 10, and some feincms3 / django-content-editor interoperability improvements which make it easier to reuse plugins/content types.
- [feincms3 4.1](https://pypi.org/project/feincms3/): Some basic support for using the apps middleware with async Django. Not documented yet and not deployed anywhere but it basically works. Some documentation edits and changes to the inline CKEditor styling because of the recent changes to Django admin's CSS.
