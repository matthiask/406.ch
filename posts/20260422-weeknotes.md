Title: Weeknotes (2026 week 17)
Categories: Django, Programming, Weeknotes
Draft: remove-this-to-publish

## Releases since the first weeks of March

### feincms3-sites and feincms3-language-sites

I released updates to [feincms3-sites](https://pypi.org/project/feincms3-sites/) and [feincms3-language-sites](https://pypi.org/project/feincms3-language-sites/) fixing the same issue in both projects: When an HTTP client didn't strip the default ports of :80 (for HTTP) or :443 (for HTTPS) from a request, finding the correct site would fail. Browsers generally strip the port already, but some other HTTP clients do not.

### django-tree-queries

As I wrote [elsewhere](/writing/llms-for-open-source-maintenance-a-cautious-case/) I closed many issues in the repositories, mostly documentation issues but also some bugs. `{% recursetree %}` should now work properly and not cache old data anymore, using the primary key in `.tree_fields()` now raises an intelligible error, and I also fixed a bug with table quoting when using [django-tree-queries](https://pypi.org/project/django-tree-queries/) with the not yet released Django 6.1+.

### feincms3-cookiecontrol

[feincms3-cookiecontrol](https://pypi.org/project/feincms3-cookiecontrol/) not only offers a cookie consent banner (which actually supports [only embedding tracking scripts when users give consent](https://406.ch/writing/reusable-cookie-consent-app-for-django/)) but also a third-party content embedding functionality which allows allowlisting individual services.

The privacy policies of these services are now linked inline instead of with an ugly extra link. This reduces content inside the embed which helps on small screens.

1.7 used a buggy trusted publishing workflow so I immediately published 1.7.1 afterwards.

### django-cabinet and django-prose-editor

[django-cabinet](https://pypi.org/project/django-cabinet/) can now be used as a media library directly inside [django-prose-editor](https://pypi.org/project/django-prose-editor/). I'm (ab)using the CKEditor 4 protocol for embedding which uses `window.opener.CKEDITOR.callFunction` to send data back from the file manager popup into the editor. It feels icky but works nicely. This is only available if you're installing the alpha prereleases, but I'm already testing the functionality in production somewhere so I feel quite good about it.

django-prose-editor now also ships brand new [`ClassLoom`](https://django-prose-editor.readthedocs.io/en/latest/classloom.html) and [`StyleLoom`](https://django-prose-editor.readthedocs.io/en/latest/styleloom.html) extensions. Both extensions allow adding either classes or inline styles to text spans or nodes. In an ideal world we maybe wouldn't use something like this, but to make the editor more useful in the real world, editors need more flexibility. These two extensions provide that. I already mentioned `ClassLoom` [in December](/writing/rich-text-editors-how-restrictive-can-we-be/#combining-css-classes), now it's actually available. I'm not completely sold on how they work yet, but both of them are already solving real issues.

### Honorable mentions

[django-debug-toolbar 6.3](https://pypi.org/project/django-debug-toolbar/) has been released, I only contributed reviews during this cycle.
