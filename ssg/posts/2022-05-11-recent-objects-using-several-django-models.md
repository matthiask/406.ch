Title: Recent objects using several Django models
Slug: recent-objects-using-several-django-models
Status: published
Date: 2022-05-11
Categories: Django, Programming
Type: markdown

# Recent objects using several Django models

I released a new Python package which builds on the excellent code published by Simon Willison in the blog post [Building a combined stream of recent additions using the Django ORM](https://simonwillison.net/2018/Mar/25/combined-recent-additions/). The rationale etc. for why this is useful is described much better by him and I'll save everyone's time by not repeating it in a worse way.

The new package is [django-recent-objects](https://github.com/matthiask/django-recent-objects/), developed on GitHub and available from PyPI.

The package supports e.g. combining recent articles and comments in a single activity stream:

    from testapp.models import Article, Comment
    from recent_objects.recent_objects import RecentObjects

    ro = RecentObjects(
        [
            {
                "queryset": Article.objects.all(),
                "date_field": "created_at",
            },
            {
                "queryset": Comment.objects.all(),
                "date_field": "created_at",
            },
        ]
    )

    additions = ro.page(paginate_by=10, page=1)

[django-recent-objects](https://github.com/matthiask/django-recent-objects/) adds the following features which aren't available in the blogpost linked above:

- The name of the `date_field` doesn't have to be the same for all objects
- Primary keys of different types are[^1] supported
- The code uses a real paginator and doesn't only support fetching the first few objects

[^1]: Hopefully!
