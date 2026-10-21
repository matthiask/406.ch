Title: How I decide which Python and Django versions I want to support
Categories: Django, Maintenance, Programming
Draft: remove-this-to-publish

A recent post on Mastodon got me thinking what my philosophy for dropping
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

I, on the other hand, tend to support versions long past their [End of
Life](https://pypi.org/project/norwegianblue/) date. I jokingly said that I
should spend time upgrading old websites instead of spending time writing a
rationale why not. I don't want to argue for my position, I'm writing this post
with the goal of thinking things through, and maybe it will also serve as the
place to point people towards when the question arises again in the future.

So here goes what I'm doing. I don't


## Projects

When working on projects I'm always updating to the current stable version or even the bleeding edge. I want the projects to be as future proof as possible.

As long as the server software allows it, I'm just going to install the newest version of Python available using [uv](https://docs.astral.sh/uv/) which supports all the packages I'm using, or at least which ships binary wheels, because I enjoy not compiling software when deploying too damn much.


## Libraries

The more foundational and widely used a library (potentially) is, the more important it is to me that it supports basically everything which is reasonable. In this context, this means that I try to support everything people could be using with good reasons. People can upgrade their software, but there may be reasons (for example in managed hosting environments) when people cannot freely update the underlying managed server software. This does affect me too and isn't necessarily a problem security-wise as long as there are other measures in place protecting those services. When I'm still actively working on some libraries, I want to use them in all environments, at least when I'm not paying a big price in terms of language features.

Supporting a large range of Django versions, for example 3.2 (reached EOL on 2024-04-01) up to the current main development branch, can be suprisingly easy when you do not reach too much into Django's internals or depend on features added only recently.

Apart from the fact that other people might benefit as well from the wider use these packages get that way I might also get the benefit of additional eyes on the code, and possibly even contributions.

That said, when do I actually drop support for an old version of Python or Django? Generally speaking, I have two reasons:

### 🌳 Keeping CI time down 🌳

I like pruning the CI matrix so as to not spend too much computing. The exception are Django projects such as the django-debug-toolbar and django-tree-queries, both projects which have to work on a wide range of Python and Django versions and database engines.


### New features which I want or need

Sometimes, I just really want to merge dictionaries using the nice [`a | b` syntax](https://github.com/feincms/feincms3-forms/commit/2a758a4e4c34d1118d5e20f42a13c47ce601b029). If this reasoning sounds whimsical to you it is, but only partially. Programming cannot just be a job, everybody needs to have fun sometimes.

Sometimes, I really need some API or behavior Django has only introduced recently, such as the way bound fields work in forms. For example, [form validation didn't go through bound fields before 4.0](https://github.com/mosparo/django-integration/pull/58).

## Developer workstations

When it comes to developer workstations I don't really have the patience for outdated software though. I don't see a reason why developer tooling can't be up to date. This came up recently in the [django-debug-toolbar issue tracker](https://github.com/django-commons/django-debug-toolbar/issues/2506). I'm totally fine with requiring an up to date version of Python for our pre commit hooks, for example.


## What is the downside?

Some people just don't want to upgrade at all, and when they suddenly have to because all hell breaks loose (because of security problems or something like that) then it will be so much harder when they have large version ranges to go until they reach actually supported versions. That said, in my experience that's not a big problem with Django at all. On the other hand, when the projects still use npm packages from 2015... oh my.
