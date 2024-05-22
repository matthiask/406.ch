Title: Weeknotes (2024 week 21)
Categories: Django, Programming, Weeknotes

There have been times when work has been more enjoyable than in the last few
weeks. It feels more stressful than at other times, and this mostly has to do
with particular projects. I hope I'll be able to move on soon.


## blacknoise

I have released [blacknoise 1.0](https://pypi.org/project/blacknoise/). It's an
ASGI app for static file serving inspired by
[whitenoise](https://github.com/evansd/whitenoise/).

The 1.0 version number is only a big step in versioning terms, not much has
happened with the code. It's a tiny little well working piece of software which
has been running in production for some time without any hickups. The biggest
recent change is that I have parallelized the gzip and brotli compression step;
this makes building images using whitenoise more painful because there the wait
is really really long sometimes. [A pull request fixing this
exists](https://github.com/evansd/whitenoise/pull/484), but it hasn't moved
forwards in months.

I have written a longer post about it earlier this year
[here](https://406.ch/writing/blacknoise-asgi-app-for-static-file-serving/).

## Releases

- [feincms3-cookiecontrol 1.5](https://pypi.org/project/feincms3-cookiecontrol/): Code golfing. Added backwards compatibility with old Django versions so that I can use it for old projects. Also includes optional support for Google consent management.
- [django-fast-export 0.1.1](https://pypi.org/project/django_fast_export/): This is basically a repackaging of the streaming CSV view from Django's documentation as a reusable class. I have switched to using an iterator so that I can export even larger datasets.
- [django-json-schema-editor 0.0.18](https://pypi.org/project/django-json-schema-editor/): Still alpha versioned but used in production in various projects. I should really release an 1.0 version, but there are no integration tests at all. Mainly visual tweaks in this update.
- [django-content-editor 6.5](https://pypi.org/project/django-content-editor/): Better handling of templates and regions when a particular editor instance only shows a subset of configured templates. Disallowed adding plugins when in an unknown region. It's funny how many edge cases exist in software as old as this.
- [blacknoise 1.0](https://pypi.org/project/blacknoise/): See above.
- [html-sanitizer 2.4.4](https://pypi.org/project/html-sanitizer/): Fixed edge cases with whitespace handling when merging elements.
- [feincms3-data 0.6.1](https://pypi.org/project/feincms3-data/): Allowed `./manage.py f3loaddata -` to load JSON data from stdin.
