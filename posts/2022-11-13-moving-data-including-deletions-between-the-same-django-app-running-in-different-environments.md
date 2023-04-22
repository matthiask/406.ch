Title: Moving data including deletions between the same Django app running in different environments
Slug: moving-data-including-deletions-between-the-same-django-app-running-in-different-environments
Date: 2022-11-13
Categories: Django, Programming

# Moving data including deletions between the same Django app running in different environments

Many projects use different environments to stabilize the code; they have a _production_ environment which is actually seen by users, a _stage_ where code is tested in an environment close to production and maybe several additional environments where more experimental code is published or developed, either on internal or protected webservers or maybe on the workstations of developers themselves.

The same process may be desired for content; an environment where the content lives which is seen by users and other environments where the content can be changed without impacting the production environment. When using Django and the [Django admin site](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/) there is no ready-made solution for doing this and maybe there shouldn't be.

## Django's serialization framework and its shortcomings for the use case outlined above

Django comes with a [serialization framework](https://docs.djangoproject.com/en/4.1/topics/serialization/) and with the `dumpdata` and `loaddata` management commands which can be used to dump and load data, e.g. to and from JSON. It's also easily possible to specify a list of primary keys on the command line if you only want to dump a subset of the existing data. When loading this subset data which isn't included isn't changed in any way, and that's good!

**However!**

Let's assume we're working with the question and choice models from [Django's tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial02/#creating-models).

- The serialization framework doesn't offer a way to easily include related data in a dump. There's no easy way to automatically include all choices of a question.
- Even if there was a way to include the related data the target environment wouldn't have a way to replicate deletions. If a choice has been removed in the source environment it will not be included in the dump, and the target environment will just do nothing with the now redundant choice.

## [feincms3-data](https://github.com/matthiask/feincms3-data/)

[feincms3-data](https://github.com/matthiask/feincms3-data/) solves these problems in (I think) a nice way, by building on the serialization framework and augmenting the JSON dump with a few additional properties which tell the loader what to do with the dataset. The code doesn't have a dependency on [feincms3](https://feincms3.readthedocs.io/) but of course it's very useful when used to dump and load structured data as is generated when using a CMS.

The following datasets configuration would work for the use case outlined above:

    from feincms3_data.data import specs_for_models
    from polls import models

    def questions(args):
        pks = [int(pk) for pk in args.split(",") if pk]
        return [
            *specs_for_models(
                [models.Question],
                {"filter": {"pk__in": pks}},
            ),
            *specs_for_models(
                [models.Answer],
                {"filter": {"question__pk__in": pks}, "delete_missing": True},
            ),
        ]

    def datasets():
        return {"default": {"specs": questions}}

Now, you have to point the `FEINCMS3_DATA_DATASETS` setting at the `datasets()` function above and now you could use `./manage.py f3dumpdata default:3,4` to dump the questions with ID 3 and 4 including their choices. The JSON can be loaded in a different instance. The questions with ID 3 and 4 will be created or updated, and choices which match the `questions__pk__in=[3,4]` filter _but aren't included in the JSON_ will be removed from the database.

Despite its pre-1.0 version number it's used for several clients to implement a workflow where they set a "request update" flag on some parent object, and the relevant data will be synced periodically between systems. I'm quite confident that the code is correct and that it does what it should. A thorough test suite helps a lot there! But you never now, but I'm sure everyone uses backups by now. But who knows.
