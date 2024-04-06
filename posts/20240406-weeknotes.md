Title: Weeknotes (2024 week 14)
Date: 2024-04-06
Categories: Django, Programming, Weeknotes, Politik

I'm having a bit of a slow week with the easter weekend and a wisdom tooth
extraction. I'm recovering quite quickly it seems and I'm glad about it.

This weeknotes entry is short and quick. I'm trying to get back into the habit
of writing them after a mediocre start this year.

## 20th Anniversary Celebration of Young Greens Switzerland

I have attended the celebration of Young Greens Switzerland. I have been a
founding member and have been active for close to ten years. A lot of time has
passed since then. It has been great to reminisce about old times with friends
and, more importantly, to see how the torch is carried on.

## Releases

- [blacknoise 0.0.5](https://pypi.org/project/blacknoise/): blacknoise is an
  ASGI app for static file serving inspired by
  [whitenoise](https://whitenoise.readthedocs.io/en/latest/). It only supports
  a very limited subset of whitenoise's functionality, but it supports async.
- [html-sanitizer 2.4.1](https://pypi.org/project/html-sanitizer/): The lxml
  library moved the HTML cleaner into its own package,
  [lxml-html-clean](https://pypi.org/project/lxml-html-clean/); this release
  adds support for that. I didn't know that the HTML cleaner is viewed as being
  problematic by the lxml maintainers. I'm having another look at
  [nh3](https://github.com/messense/nh3) and will maybe switch html-sanitizer's
  guts from lxml to nh3 in the future.
- [django-tree-queries 0.18](https://pypi.org/project/django-tree-queries/):
  django-tree-queries now supports ordering siblings by multiple fields and
  even allows descending orderings.
- [django-cabinet 0.14.2](https://pypi.org/project/django-cabinet/): This
  release fixes the CKEditor 4 filebrowser popup when using Django 5 or better.
