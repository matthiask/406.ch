Title: Configuring Django backends using speckenv’s 12factor support
Slug: configuring-django-backends-using-speckenvs-12factor-support
Date: 2022-08-18
Categories: Django, Programming

# Configuring Django backends using speckenv's 12factor support

There are many many 12factor utility apps available to configure databases, caches and the email backend in Django apps, for example [dj-database-url](https://github.com/jazzband/dj-database-url/), [django-cache-url](https://github.com/epicserve/django-cache-url/) and [dj-email-url](https://github.com/migonzalvar/dj-email-url/). As I wrote in my 2020 blog post [Using environment variables to configure Django](https://406.ch/writing/using-environment-variables-to-configure-django/) I liked using them -- a lot. However, this has changed a bit because I don't like the fact that all released versions of those libraries modify the `urllib.uses_netloc` list with their own protocols (when it's not necessary at all) and I don't like it either that some bugs still exist in some libraries which make upgrading projects in our environments from Django 3.2 to Django 4.0 harder than it should be; the problem isn't really caused by Django's new built-in features but rather surfaced by it.

Anyway, since I already had a library which helped reading settings from the environment, adding another utility which transforms DSNs to configuration dictionaries understood by Django was straightforward. And that's why I'm now happily using [speckenv's Django support](https://github.com/matthiask/speckenv/#django-support) for those use cases.

Reducing the amount of dependencies in a project maybe shouldn't be a goal in itself, but replacing generic utilities with more opinionated utilities is certainly a net positive in my book (if it is possible!)
