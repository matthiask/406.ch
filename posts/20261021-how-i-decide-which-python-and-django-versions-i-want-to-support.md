Title: How I decide which Python and Django versions I want to support
Categories: Django, Maintenance, Programming, Python

A recent post on Mastodon got me thinking about what my philosophy for dropping
support for old versions of Python and Django is. Here's the post:

> 🚨 Important Announcement 🚨
>
> Going forward all my packages will only "officially" support maintained #Python versions. Meaning since October only 3.14 and now 3.15.
>
> This has no effect on Django version support.
>
> CVEs will be backported to older 🐍 releases.
>
> -- [@codingjoe](https://fosstodon.org/@codingjoe/117418591209854460)

I tend to support versions long past their [End of
Life](https://pypi.org/project/norwegianblue/) date. I jokingly said that I
should spend time upgrading old websites instead of spending time writing a
rationale why not. I don't want to argue for my position, but maybe this post
will serve as the place to point people towards when the question arises again
in the future.

The short answer: it depends on whether I'm working on a project, on my own
machine or on a library.

## Projects

When working on projects I'm always updating to the current stable version or even the bleeding edge. I want the projects to be as future-proof as possible and I also want to give [early feedback when stuff breaks](/writing/weeknotes-2023-week-39/#adding-scheduled-tests).

As long as the server software allows it, I'm just going to use [uv](https://docs.astral.sh/uv/) to install the newest Python version that all the packages I'm using support (or at least ship binary wheels for), because I enjoy not compiling software when deploying too damn much.

## Developer workstations

When it comes to developer workstations I don't really have the patience for outdated software. I don't see a reason why developer tooling can't be up to date. This came up recently in the [django-debug-toolbar issue tracker](https://github.com/django-commons/django-debug-toolbar/issues/2506). I'm totally fine with requiring an up-to-date version of Python for our pre-commit hooks, for example.

## Libraries

The more foundational and widely used a library (potentially) is, the more important it is to me that it supports basically everything which is reasonable.

I'm still using my libraries in older projects myself, so they have to work there. I want to use them in all environments, at least when I'm not paying a big price in terms of language features.

Other people may be stuck on older versions too. People can upgrade their software, but there may be situations (for example in managed hosting environments) where people cannot freely update the underlying managed server software. That isn't necessarily a problem security-wise as long as there are other measures in place protecting those services.

When people use my libraries, I might get additional eyes on the code, and possibly even contributions.

Supporting a large range of Django versions, for example 3.2 (reached EOL on 2024-04-01) up to the current main development branch, can be surprisingly easy when you do not reach too much into Django's internals or depend on features added only recently.

That said, when do I actually drop support for an old version of Python or Django? Generally speaking, I have two reasons:

### 🌳 Keeping CI time down 🌳

I like pruning the CI matrix so as to not spend too much compute and energy. The exceptions are packages such as django-debug-toolbar and django-tree-queries: they are widely used and have to work on a wide range of Python and Django versions and database engines, so the additional CI runs are worth it.

When I remove a version from the CI matrix I mostly raise the minimum version in the package metadata as well. I almost never use upper bounds for version ranges, but lower bounds I definitely do use.

### Using new features, either because I want them or because I need them

Sometimes, I just really want to merge dictionaries using the nice [`a | b` syntax](https://github.com/feincms/feincms3-forms/commit/2a758a4e4c34d1118d5e20f42a13c47ce601b029). If this reasoning sounds whimsical to you, it is, but only partially. Programming cannot just be a job, everybody needs to have fun sometimes.

Sometimes, I really need some API or behavior Django has only introduced recently, such as the way bound fields work in forms. For example, [form validation didn't go through bound fields before 4.0](https://github.com/mosparo/django-integration/pull/58).

### What that means right now

Most of my packages currently require Python 3.10 or newer and Django 3.2 or 4.2 or newer. Some of the less actively developed ones still go back as far as Python 3.8, simply because I haven't had a reason to touch them. Python and Django support are linked: Django 4.2 supports Python 3.8 to 3.12 while Django 6.0 requires Python 3.12, so the oldest Django version I support pretty much decides the oldest Python version worth testing.

## What is the downside?

Supporting old versions makes it easier for people to put off upgrading. Some people just don't want to upgrade at all, and my libraries continuing to work on old versions certainly doesn't push them to do it. When they suddenly have to because all hell breaks loose (because of security problems or something like that) it's so much harder: they have a long way to go until they reach supported versions. That said, in my experience that's not a big problem with Django at all. On the other hand, when the projects still use npm packages from 2015... oh my.

The code is also less clean than it could be. Supporting old versions means compatibility shims, and it means not using some of the nicer features newer versions offer.

In the end, both approaches are reasonable, and both have their costs. You should do what brings you more joy.
