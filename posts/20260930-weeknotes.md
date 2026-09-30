Title: Weeknotes (2026 week 40)
Categories: Django, Programming, Weeknotes

I have been at [Django on the Med 🏖️](https://djangomed.eu/) and already wrote a [lengthy post](https://406.ch/writing/looking-back-at-django-on-the-med-2026/) about that.

I did a lot of work on a [DEP for adding import map support to Django](https://github.com/django/deps/pull/101) which is currently also being discussed on the [forum](https://forum.djangoproject.com/t/integrate-importmap/35243). Apart from that I'm not going to repeat anything from the post linked above, so check it out if you want to know more.

Motivated by a discussion I had at the sprint I also improved my release process. I now have a `make-release` script in my dotfiles which updates the CHANGELOG with the version, bumps the version itself in the repo and commits and tags the release. The rest is handled by [trusted publishing](https://406.ch/writing/switching-all-of-my-python-packages-to-pypi-trusted-publishing/). I'm now finally also properly handling patch releases so that you don't have to check the history to know what's in a patch release. I already did that for minor and major version bumps, but was a bit too lazy. Now I can be even lazier and still more correct, and it feels great.

Next, I refactored the static site generator script for this blog to be much faster. I now do not have to wait when saving before refreshing the browser. Much nicer.

## Releases from the last three weeks

### django-js-asset

[django-js-asset 5.0a1](https://pypi.org/project/django-js-asset/) implements the API proposed in the [DEP](https://github.com/django/deps/pull/101). This is an alpha release because the DEP is still being discussed and I don't want to break people's code again and again if, during discussion, it appears that the API should be different.

### django-json-schema-editor, django-prose-editor and django-content-editor

The three alpha releases [django-json-schema-editor 0.15a1](https://pypi.org/project/django-json-schema-editor/), [django-prose-editor 0.28a2](https://pypi.org/project/django-prose-editor/) and [django-content-editor 9.1a1](https://pypi.org/project/django-content-editor/) depend on django-js-asset 5.0a1 mentioned above and implement the necessary changes for the new import map definition style.

### django-authlib

[django-authlib 0.20](https://pypi.org/project/django-authlib/) adds support for specifying the tenant when using Microsoft Entra ID.

### feincms3-downloads

[feincms3-downloads 0.6](https://pypi.org/project/feincms3-downloads/) includes translation fixes, uses different error codes when `pdftocairo` or `convert` are missing, and changed the `PATH` environment variable handling to be less annoying for local development.
