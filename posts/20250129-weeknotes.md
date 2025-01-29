Title: Weeknotes (2025 week 05)
Categories: Django, Programming, Weeknotes

## Djangonaut Space

In December I wrote a few paragraphs about [my decision to not run for the
Django Steering Council](https://406.ch/writing/weeknotes-2024-week-49/),
mentioning that I want to contribute in different ways.

I have offered to contribute to Djangonaut Space to do some mentoring. I'm
already a bit stressed, but that's normal and to be expected. I'll probably
have more to share about that in the close future!


## Releases

- [feincms-cookiecontrol 1.6](https://github.com/feincms/feincms3-cookiecontrol/commits/main/): Removed the hardcoded dependency upon [feincms3](https://feincms3.readthedocs.io/) and some additional code golfing. The cookie banner JavaScript is now back to <4KiB.
- [django-curtains 0.7](https://pypi.org/project/django-curtains/): Updated the CI job list and modernized the package somewhat, no code changes necessary. It's good to release updated versions though just to show that it's still actively maintained.
- [django-prose-editor 0.10.3](https://pypi.org/project/django-prose-editor/): Small CSS fixes and mainly updated TipTap/ProseMirror.
- [django-imagefield 0.22](https://pypi.org/project/django-imagefield/): The updated version no longer autodeletes processed images; this wasn't really a problem before but I was a little bit fearful that images are still referenced elsewhere and this change let's me sleep better.
- [feincms-oembed 2.0](https://pypi.org/project/feincms-oembed/): Oembed support for FeinCMS 1 without actually depending upon the FeinCMS package itself. Still works.
- [django-content-editor 7.2](https://pypi.org/project/django-content-editor/): The ``Region`` type is now hashable; this may be useful, or not.
- [feincms3 5.3.1](https://pypi.org/project/feincms3/): I undeprecated the ``TemplateMixin`` because even though ``PageTypeMixin`` is nicer, sometimes all you need is a template selector.
