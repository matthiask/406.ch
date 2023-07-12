Title: Weeknotes (2023 week 28)
Date: 2023-07-12
Categories: Django, Programming, Weeknotes, feincms

## Releases

- [html-sanitizer 2.2](https://pypi.org/project/html-sanitizer/): Made the
  sanitizer's configuration initialization more strict. Strings cannot be used
  anymore in places where the sanitizer expects a set (resp. any iterable).
  It's useful that strings are iterable in Python and I wouldn't want to change
  that, but the fact that `("class")` is a string and not a tuple makes me sad.
  The fact that tuples are created by `,` and not by `()` will always trip up
  people.
- [feincms3-language-sites
  0.1](https://pypi.org/project/feincms3-language-sites/): The version number
  is wrong but whatever. I'm certainly happy with the state of things. The big
  change in 0.1 is that `Page.get_absolute_url` no longer generates
  protocol-relative URLs. Depending on the value of `SECURE_SSL_REDIRECT` it
  automatically prepends either `http:` or `https:`.
- [django-authlib 0.15](https://pypi.org/project/django-authlib/):
  django-authlib's admin Single Sign On module now supports a hook to
  automatically create staff users when a matching user doesn't exist already.
  I don't plan to use this functionality myself and I have recommended people
  to implement the functionality themselves using the tools in django-authlib
  if they need it, but the change was so small and well-contained that adding
  it to the core made sense to me.

## pipx inject

We learned that [pipx](https://pypa.github.io/pipx/) seems to remember injected
packages even across `pipx reinstall` invocations. Not too surprising now that
we know it, but we certainly spent some time scratching our heads. `pipx
uninject` was the thing we needed to stop pipx from installing an old version
of a dependency instead of the one being specified in `pyproject.toml`.

## hatchling and data files

I'm very confused by the way [hatchling](https://hatch.pypa.io/) sometimes
includes data files and sometimes it doesn't. I had to add `[tool.hatch.build]
include=["authlib/"]` to [django-authlib's `pyproject.toml`
file](https://github.com/matthiask/django-authlib/commit/67d4673e4039eac277b5d2557c0736c1f01442ac)
to make it include HTML files from subpackages. Maybe the subpackages are the
reason, but I'm not sure.

## Payment providers that must not be named

I have spent hours and hours battling with the badly documented, incomplete,
inconsistent and confusing API of a (not that well known) payment provider
based in Switzerland. I'm surprised that this still happens years and years
after Stripe started offering a really well thought out and documented API
geared towards programmers. It's really sad because when the same structure is
named with differing naming conventions (e.g. `snake_case` vs. `camelCase`) in
different parts of the API you just know that somebody spent too much time
writing too much code instead of reusing already existing functionality.
