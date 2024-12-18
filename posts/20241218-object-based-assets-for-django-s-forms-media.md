Title: Object-based assets for Django's forms.Media
Categories: Django, Programming

The pull request for adding [object-based script media assets into
Django](https://github.com/django/django/pull/18782) is in a good state and I
hope it will be merged soon. I have been using object-based assets long before
[Django actually added support for them in
4.1](https://github.com/django/django/commit/4c76ffc2d6c77) ([since
2016](https://github.com/feincms/django-content-editor/commit/82ac91ea7af2409bb3672e11c18871002ddc9753),
that's before Django 1.10!) by using a gross hack. Luckily I have been able to
clean up the code when Django 4.1 landed.

I have been asking myself at times why I haven't proposed the change to Django
myself despite having been a user of something like this for such a long time.
After all, I have been happily contributing issue reports, bug fixes and tests
to Django. The process of adding new features sometimes is terribly frustrating
even when looking (and cheering) from the sidelines, it takes so much time and
energy. It feels bad that adding another package to the [list of packages I
maintain](https://pypi.org/user/matthiask/) so clearly seems to be the better
way to **get things done** compared to proposing a new feature for Django
itself. I hope [processes change
somewhat](https://406.ch/writing/weeknotes-2024-week-49/).

But I digress.

The `ProseEditorWidget` in
[django-prose-editor](https://github.com/matthiask/django-prose-editor/) wants
to ship CSS, JavaScript and some JSON to the browser for the widget. So, of
course I used object-based media assets for this instead of widget HTML
templates. Media assets are deduplicated and sorted by Django. If different
editor presets use differing lists of assets they are smartly merged by
`forms.Media` using a topological sort. You get those niceties for free when
using `forms.Media` and everything just works, so what's not to like?

The only thing which isn't to like is that Django, at the time of writing,
doesn't provide any classes helping with this. You can put strings into
`forms.Media` or you can put objects with a `__html__()` method in there. The
latter of course is all that's needed to support more advanced use cases -- and
that's exactly what
[django-js-asset](https://pypi.org/project/django-js-asset/) now provides, and
what django-prose-editor uses.

[django-js-asset](https://pypi.org/project/django-js-asset/) has long supported
a `JS` class with support for additional
attributes, for example:

    :::python
    from js_asset import JS

    forms.Media(js=[
        JS("asset.js", {"id": "asset-script", "data-answer": "42"}),
    ])

Since 3.0 the package also comes with a `CSS` and `JSON` class:

    :::python
    from js_asset import CSS, JS, JSON

    forms.Media(js=[
        JSON({"cfg": 42}, id="widget-cfg"),
        CSS("widget/style.css"),
        CSS("p{color:red;}", inline=True),
        JS("widget/script.js", {"type": "module"}),
    ])

This produces the following HTML:

    :::html
    <script id="widget-cfg" type="application/json">{"cfg": 42}</script>
    <link rel="stylesheet" href="/static/widget/style.css">
    <style>p{color:red;}</style>
    <script src="/static/widget/script.js" type="module"></script>

The code which is proposed for Django supports the JavaScript use case but with
a slightly different API:

    :::python
    forms.Media(js=[
        Script("widget/script.js", type="module"),
    ])

This looks slightly nicer as long as you don't use e.g. data attributes,
because then you have to do:

    :::python
    forms.Media(js=[
        Script("widget/script.js", **{"data-cfg": ...}),
    ])

I always forget that Python supports passing keyword arguments names which
aren't valid Python identifiers (but only when using `**kwargs`). I personally
don't care much either way, and when my packages can finally drop compatibility
with Django versions which do not support all these functionalities yet I'll
finally be able to retire
[django-js-asset](https://pypi.org/project/django-js-asset/). That won't happen
any time soon though, if only because I like supporting old versions of Django
because I have so many Django-based websites running somewhere.
