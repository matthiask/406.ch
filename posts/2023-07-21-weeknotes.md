Title: Weeknotes (2023 week 29)
Date: 2023-07-21
Categories: Django, Programming, Weeknotes

# Weeknotes

I have mainly done work in private projects this week. Not much to talk about.
Except for the ZIP file `content-type` bug which was interesting enough to
justify [its own blog post](https://406.ch/writing/serving-zip-files-using-django/).

## Releases

- [django-cabinet 0.13](https://pypi.org/project/django-cabinet/): I converted
  the package to use ruff, hatchling; started running CI tests using Python
  3.11. The internals of the Django admin's filters have changed to allow
  multi-valued filters, this has required some changes to the implementation of
  the folder filter. I opted to using a relatively ugly `django.VERSION`
  hack; but that's not too bad since such branches will be automatically
  removed by the awesome
  [django-upgrade](https://github.com/adamchainz/django-upgrade). I would have
  tried finding other ways in the past but now that old compatibility code can
  be removed by a single run of `django-upgrade` (respectively
  `pre-commit`) there really is no point to doing it in a different way.
