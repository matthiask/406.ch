Title: Open source activity (April 2018 edition)
Slug: open-source-activity-april-2018-edition
Date: 2018-04-09
Categories: Django, Programming

Again months have gone by without a new post. Still trying to change this, so here's a summary.

# Open source activity (April 2018 edition)

## [django-imagefield](https://pypi.org/project/django-imagefield/)

A more opinionated version of [django-versatileimagefield](https://pypi.org/project/django-versatileimagefield/), which

- keeps the amount of code in production at a minumum
- has a strong preference towards generating images in advance, not on demand (which means it stays fast whatever the storage backend may be)
- fails early when invalid images are uploaded instead of crashing the website later

## [speckenv](https://pypi.org/project/speckenv/)

speckenv helps keep configuration and secrets [in the environment](https://12factor.net/config), not in the code. It knows how to parse `.env` files, and how to read structured values from the environment (not only strings, but also bools, lists, dictionaries -- in short, Python literals)

## [django-curtains](https://pypi.org/project/django-curtains/)

It is useful to give clients protected access to a website in development. django-curtains allows keeping the work in progress secret by only allowing authenticated access (using either Django's authentication system, or HTTP Basic authorization)

---

Of course, activity on older projects hasn't ceased either. New releases of [xlsxdocument](https://pypi.org/project/xlsxdocument/), [django-user-messages](https://pypi.org/project/django-user-messages/), [django-http-fallback-storage](https://pypi.org/project/django-http-fallback-storage/), [html-sanitizer](https://pypi.org/project/html-sanitizer/), [feincms3](https://pypi.org/project/feincms3/), [django-cabinet](https://pypi.org/project/django-cabinet/), [django-authlib](https://pypi.org/project/django-authlib/), etc. are available on PyPI.
