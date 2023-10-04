Title: Weeknotes (2023 week 40)
Date: 2023-10-04
Categories: Django, Programming, Weeknotes, feincms

## More work on hosting several websites from a single Django application server using feincms3-sites

I have mentioned feincms3-sites last week in my last weeknotes entry; I have
again given this package a lot of attention in the last days, so another update
is in order.

It is now possible to override the list of languages available on each site.
That's especially useful for an upcoming campaign site where the umbrella
group's site is available in three languages, but (most?) individual group
sites (hosted on subdomains) will only have a subset of languages. Since I live
in a country with four national languages (english isn't one of them, but is
spoken by many!) supporting more than one language, or even many languages is
totally commonplace. It's great that Django has good support for
internationalization. For the sake of an example, I have the following sites:

- `example.com`: The default. The host has to match exactly.
- `subdomain.example.com`: One individual group's site. The host has to match the regex `^subdomain\.` (sorry, I actually do like regexes).

### Overriding configured hosts for local development

One thing which always annoyed me when using `django.contrib.sites` was that
"just" pulling the database from production to the local development
environment always produced links pointing back to the remote host instead of
working locally (when producing absolute URLs). This problem was shared by
feincms3-sites as well. I have now found a very ugly but perfectly workable
solution: Overwrite `Site.get_host()` locally:

    :::python
    if DEBUG:
        domain = "example.com"  # Or whatever
        _get_host = lambda site: site.host.replace(domain, "localhost:8000")
        FEINCMS3_SITES_SITE_GET_HOST = _get_host

This works especially well when using `example.com` and maybe subdomains of
`example.com`: All absolute links will point to `localhost:8000` or
`subdomain.localhost:8000`. Since `*.localhost` always resolves to the local IP
the browser knows where it should connect to, and since
`subdomain.localhost:8000` also matches the `^subdomain\.` regex mentioned
above, the site selection logic works as well.

Of course if you have more domains, not just subdomains, you could adapt the
`get_host` override and the relevant regexes to those use cases.

### Closing words

We're at 100% code coverage now when running the test suite. That's really nice.

## Logging into the Django admin using your Google account

This functionality has long been provided by
[django-admin-sso](https://pypi.org/project/django-authlib/); however, as
mentioned a long time ago this package still uses a deprecated OAuth2 library.
[django-authlib](https://github.com/matthiask/django-authlib/) supports using a
Google account to authenticate with the Django admin since 2017. I have now
fixed a small problem with it: If you are logged into a single Google account,
and this account's email address doesn't match the configured admin login rule,
you were out of luck: There was no way to add another account at that time
because the library didn't request the account selection. That has changed now,
if the first login attempt doesn't work, it now explicitly tells Google to let
the user select their Google account. A small quality of life improvement for
those using more than one Google account (voluntarily or not).

## Releases

- [feincms3 4.4.3](https://pypi.org/project/feincms3/): Polished the CKEditor integration a little bit. Re-enabled the source button now that we're back to using the classic iframe-based editor again.
- [feincms3-sites 0.19.3](https://pypi.org/project/feincms3-sites/): See above.
- [django-authlib 0.16.4](https://pypi.org/project/django-authlib/): See above.
