Title: Weeknotes (2024 week 51)
Categories: Django, Programming, Weeknotes

## Building forms using Django

I last wrote about this topic [in April](https://406.ch/writing/building-forms-with-the-django-admin/). It has [resurfaced on Mastodon this week](https://mastodon.social/@webology/113669270531953652). I'm thinking about writing a [feincms3-forms](https://github.com/feincms/feincms3-forms) demo app, but I already have too much on my plate. I think composing a forms builder on top of [django-content-editor](https://django-content-editor.readthedocs.io/) is the way to go, instead of replacing the admin interface altogether -- sure, you can always do that, but it's so much less composable...

## Releases

- [blacknoise 1.2](https://pypi.org/project/blacknoise/): No real changes, added support for Python 3.13 basically without changing anything. It's always nice when this happens.
- [django-imagefield 0.21](https://pypi.org/project/django-imagefield/)
- [django-prose-editor 0.10](https://pypi.org/project/django-prose-editor/): I rebuilt django-prose-editor from the ground up [and wrote about that two weeks ago](https://406.ch/writing/rebuilding-django-prose-editor-from-the-ground-up/). The 0.10 release marks the final point of this particular rewrite.
- [django-js-asset 3.0](https://pypi.org/project/django-js-asset/): See the blog post from [this week](...)
