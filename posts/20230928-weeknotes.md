Title: Weeknotes (2023 week 39)
Date: 2023-09-28
Categories: Django, Programming, Weeknotes, feincms

Again a few weeks have passed since the last weeknotes entry :-)

## Moving feincms3 repositories into the feincms organization

The [feincms](https://github.com/feincms) GitHub organization has seen more
active days when FeinCMS 1.x was still actively developed. Since my interest
has moved to feincms3 some years ago I haven't kept the organization up to
date. That has changed this week, and I have moved most feincms3-related
repositories into the organization.

This move doesn't change much though, but it certainly feels more official now.

## Adding scheduled tests

I have started using the cronjob schedule feature of GitHub actions to ensure that tests run at least once a month in a few important projects. I want to get notified of changes in Django@main affecting my packages not only when actively working on them. I try to keep up with Django@main in all packages I maintain.

## Releases

- [feincms3-sites 0.18.2](https://pypi.org/project/feincms3-sites/): Many releases in the last weeks. Stopped using permanent redirects in DEBUG mode. Avoid migrations when Django adds more languages. Added utilities which allow restricting model relations to objects in the same site (trickier than it sounds). Added utilities for building full URLs to other sites without taxing the database as much.
- [feincms3-language-sites 0.2.0](https://pypi.org/project/feincms3-language-sites/): No biggie. No permanent redirects in DEBUG mode anymore.
- [feincms3-cookiecontrol 1.4.5](https://pypi.org/project/feincms3-cookiecontrol/): Reduced the byte size of the CSS and JavaScript some more. Added spanish translations.
- [django-authlib 0.16.3](https://pypi.org/project/django-authlib/): I have published a post last week describing the new [role-based permissions feature](https://406.ch/writing/keep-content-managers-admin-access-up-to-date-with-role-based-permissions/).
- [django-imagefield 0.17](https://pypi.org/project/django-imagefield/): The `process_imagefields` management command now allows specifying globs. If you wanted to prerender all imagefields in the pages app you can use `./manage.py process_imagefields pages.*` now instead of listing all image fields' labels explicitly.
- [feincms3 4.4.1](https://pypi.org/project/feincms3/): I'm enormously unhappy but I had to go back to the classic CKEditor instead of using the inline editor. The latter looked much nicer but overriding the Django admin CSS was very very painful. Also, I can totally understand why CKEditor 5 is completely different and why CKEditor 4 is only maintained in a paid LTS plan. It still is making me look for alternatives.
- [django-mptt 0.15](https://pypi.org/project/django-mptt/): I unfortunately am still using this despite the fact that I have marked it as officially unmaintained since march 2021. I did a mediocre job of making the library run on Django@main again. Parts of the library do not work, but since I'm not using them I don't care too much. I'm still wondering if someone wants to take over maintenance of the library since it still seems to be actively used in projects of others as well. When I don't have to use django-mptt I'm still really happy with [django-tree-queries](https://406.ch/writing/django-tree-queries/).
- [form-designer 0.22](https://pypi.org/project/form-designer/): This is probably my oldest actively developed project these days. 13 years! (Except for django-content-editor of course.) I have modernized the package, switched to hatchling and put out a new release.
