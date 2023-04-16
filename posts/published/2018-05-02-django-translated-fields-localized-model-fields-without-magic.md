Title: django-translated-fields – localized model fields without magic
Slug: django-translated-fields-localized-model-fields-without-magic
Date: 2018-05-02
Categories: Django, Programming
Type: markdown

# django-translated-fields -- localized model fields without magic

There are many ways to save and retrieve multilingual content in a database; countless blog posts, emails and [software packages](https://djangopackages.org/grids/g/model-translation/) have been written discussing or helping with this problem.

Two main approaches exist to tackle the problem:

1. Use a table for the language-independent content, and a table for language-specific content. The latter most often has a foreign key to the former and a language field. There will be a record in the latter table for each record in the former, or less if some dataset isn't available in all languages. [django-hvad](https://github.com/KristianOellegaard/django-hvad), [django-parler](https://github.com/django-parler/django-parler) and also [FeinCMS 1's translations module](https://github.com/feincms/feincms/blob/master/feincms/translations.py) follow this approach.
2. Use only one table, but use several fields to store the localized data. [django-modeltranslation](https://github.com/deschler/django-modeltranslation) is probably the best known app implementing this approach.

(Other ways of course exist. Among the more interesting packages (to me) are [django-nece using Postgres' JSONB fields](https://github.com/tatterdemalion/django-nece) and [django-vinaigrette using gettext](https://github.com/ecometrica/django-vinaigrette).)

## Why write another package?

The features they provide are at costly to implement and hard to maintain. For example, django-modeltranslation supports adding translations to third party apps which themselves do not support any translations, but to do this it has to not only provide properties for attribute access on models, but also hook into querying, into form generation, into model admin classes, and implement generic fallback logic etc. so that the current language is respected everywhere transparently.

_This does not only sound complex, it is!_ And the efforts and ingenuity that went into supporting those features have to be respected -- I certainly do.

But, couldn't I just help out instead of [adding another package solving the same problem?](https://xkcd.com/927/). Yes, that I could. But time is limited, and even taking future maintenance into account it sometimes is easier -- and more fun -- to [rewrite](https://signalvnoise.com/posts/3856-the-big-rewrite-revisited) than to refactor, _especially if you're not trying to solve the exact same problem_.

## django-translated-fields

And that's where [django-translated-fields](https://github.com/matthiask/django-translated-fields) enters the fray.

While other packages contain thousands of lines of code, this package contains a good-enough solution [in less than 50 lines of code](https://github.com/matthiask/django-translated-fields/blob/f6bd6e650b6b12bb85f731da94dd8066b3b763cb/translated_fields/fields.py), when ignoring the `translated_attributes` class decorator which is orthogonal to the `TranslatedField` class. Lines of code is not the only interesting metric of course, but it is a **very** good predictor of maintenance cost.

Of course the package has significantly less features than any of the other packages mentioned above, but it hits the sweet spot where its features are sufficient for most of our projects.

And living in a country with [four official languages](https://en.wikipedia.org/wiki/Languages_of_Switzerland) (and english isn't even one of those) it should be easy to believe that after a few years you'll have plenty of experience providing users and customers with ways to work with multilingual content, and knowing what is necessary and what isn't.
