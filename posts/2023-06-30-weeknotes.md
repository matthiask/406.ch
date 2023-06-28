Title: Weeknotes (2023 week 26)
Date: 2023-06-30
Categories: Django, Programming, Weeknotes, feincms

## Releases

I released updates to a few of my packages; I have continued converting packages to [hatchling](https://hatch.pypa.io) and [ruff](https://github.com/astral-sh/ruff) while doing that.

New releases in the last two weeks include:

- [django-tree-queries 0.15](https://pypi.org/project/django-tree-queries/): Added a new function, `.without_tree_fields()` to the queryset which can be used to avoid the `.with_tree_fields(False)` boolean trap warning.
- [feincms3-cookiecontrol 1.3.1](https://pypi.org/project/feincms3-cookiecontrol/): This small update allows replacing the feincms3 [noembed.com](https://noembed.com) oEmbed code using other libraries such as [micawber](https://github.com/coleifer/micawber/) which support a wider range of URLs while still gating the embed behind users' explicit consent.
- [feincms3-downloads 0.5.3](https://pypi.org/project/feincms3-downloads/): Updated translations.
- [django-ckeditor 6.6.1](https://pypi.org/project/django-ckeditor/): Updated the bundled CKEditor 4 and merged a pull request adding better integration with Django admin's dark mode.
- [django-js-asset 2.1](https://pypi.org/project/django-js-asset/): Just basic maintainability and packaging updates. The `JS()` implementation itself is untouched since February 2022.
- [html-sanitizer 2.0](https://pypi.org/project/html-sanitizer/): Not really a backwards incompatible change (at least not according to the tests); I just wanted to avoid `1.10` and go directly to `2.0` this time.

## GitHub projects

We are using GitHub project boards more and more. It definitely isn't the most versatile way of managing projects but it sort-of hits the sweet spot for us. [I'm mostly happy with it, and it seems to me that applying [the rule of least power](https://en.wikipedia.org/wiki/Rule_of_least_power) to project management software may not be such a bad idea after all.

The built-in workflows are a bit boring and limited; especially the fact that it seems impossible to automatically add issues to the project when using multiple repositories. Luckily, [actions/add-to-project](https://github.com/actions/add-to-project) exists so that's not really a big problem.

## To cloud or not

I had a long discussion with a colleague about containerization, Kubernetes, self-hosting, etc. etc. and I still don't know where I stand. I can honestly say that the old way of hosting (ca. 2010) still works fine. I worry about the deterioriation of service quality we're seeing and sometimes I really would like to have root to apply quick fixes where now I have to jump to hoops just to get what I already know I need. Annoying. But migrations are annoying as well.

## Scheduled publishing

I augmented the script generating this website with scheduled publishing support while again reducing the number of lines in the file. The code is still formatted using black and ruff, while only ignoring line-length errors (I do this everywhere now to avoid breaking up long strings, not to put much code onto single lines) and allowing named lambdas. The weeknotes from two weeks ago where published by GitHub actions' cron scheduling support.

## I like programming more than writing (even though I like writing)

I notice that writing is the first thing I start skipping when I have to
prioritize. Programming, biking, gardening come first. That's fine, really. But
I'm still a bit sad that I do not manage to at least put out a short weekly
weeknotes entry.
