Title: Weeknotes (2026 week 27)
Categories: Django, Programming, Weeknotes

The [last entry in this series](https://406.ch/writing/weeknotes-2026-week-17/) was published 10 weeks ago so it really is time for another review of the releases I did during this time.


## Releases

### feincms3-forms

The [feincms3-forms](https://pypi.org/project/feincms3-forms/) forms builder has gained a [documentation page](https://feincms3-forms.readthedocs.io/) on the wonderful Read the Docs service. The 0.6.1 release doesn't contain any code changes, just `pyproject.toml` updates and the mentioned documentation rework.

### django-imagefield

django-imagefield 0.23 is still in alpha. The handling of image fields when using libvips is optimized to use less memory hopefully. We'll see. I also added some tests to verify that `.mpo` files are handled properly.

### feincms3

The Vimeo embed now always sets the `dnt=1` parameter on the `<iframe>`, which asks Vimeo to not track the user.

### django-mptt

I wrote about the [somewhat annoying maintenance](https://406.ch/writing/anything-new/) again. The library is still officially unmaintained, but I did a lot of work either just closing issues or also fixing them. The docs also contain many clarifications. I only released 0.19rc1 for now.

### feincms3-sites and feincms3-language-sites

[Last time](https://406.ch/writing/weeknotes-2026-week-17/#feincms3-sites-and-feincms3-language-sites) I mentioned that default HTTP/S ports are now stripped so that the host matching can determine the correct site. Now a new case appeared where trailing dots weren't stripped. The normalization of hosts has been extended. I'm sure we're still missing some exotic cases where we should do more normalization, but we'll cross that bridge when we get there.

### django-prose-editor and django-js-asset

Various upgrades to the editor and especially the importmaps rework in both packages -- the importmap infrastructure should now be CSP-compatible! I wrote more about that in the last post [The 2026 way of using importmaps in Django](https://406.ch/writing/the-2026-way-of-using-importmaps-in-django/).

### django-content-editor

Minor bugfixes and a major version bump because of the rework of the JavaScript code into multiple ES modules. The content editor now uses importmaps as well.

### django-fhadmin

Small bugfix so that links aren't underlined in the app groups list when they shouldn't be, matching how the Django admin itself behaves.

### django-cabinet

The cabinet / prose editor integration for the file (or image) picker is final and released as a stable version.

### django-json-schema-editor

This small release only contains more correct German translations of strings.

### Honorable mention: django-debug-toolbar

I didn't actually create this release, but I contributed various changes to it. The changelog for 7.0 is [here](https://django-debug-toolbar.readthedocs.io/en/latest/changes.html).
