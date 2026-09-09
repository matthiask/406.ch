Title: Weeknotes (2026 week 37)
Categories: Climate, Django, Programming, Weeknotes

Tonight the temperature will drop to 10°C. I like it when it's hot, but now I really enjoy the slightly cooler temperatures in Europe. The [last post](/writing/weeknotes-2026-week-33/#holidays-and-the-heat-wave) was written in the middle of the heat wave. Yesterday we still had temperatures of over 30°C, which is a lot for September. But it will be the new normal. [Next year probably won't be cooler](https://en.wikipedia.org/wiki/El_Ni%C3%B1o%E2%80%93Southern_Oscillation).

## Releases from the last four weeks

Lots of activity!

### django-authlib

[django-authlib 0.19](https://pypi.org/project/django-authlib/) hardens the OAuth2 implementation a bit against replay attacks, provides utilities for removing password logins from the Django administration interface, and removes some of the confusion around role-based permissions. Upgrading is recommended.

### django-content-editor

[django-content-editor 9.0.2](https://pypi.org/project/django-content-editor/) fixes a bug in the function which allows cloning plugins from other regions. The bug was most visible when using something like [django-json-schema-editor](https://django-json-schema-editor.readthedocs.io/)'s plugins which are only [proxy models](https://docs.djangoproject.com/en/6.1/topics/db/models/#proxy-models). Their type was lost because I was using `_base_manager`, which didn't do the downcasting properly. (Sorry for the word salad.)

### django-tree-queries

[django-tree-queries 0.26.1](https://pypi.org/project/django-tree-queries/) now uses annotations instead of `.extra()` to add the `tree_path` and `tree_depth` fields. This is great because the ORM knows these fields properly and we can now use e.g. `.filter(tree_depth=1)` instead of `.extra(where=["..."])`.

This change was mainly motivated by the renewed interest in deprecating `.extra()` at some unknown future point in time.

### django-debug-toolbar

[django-debug-toolbar 8.0](https://pypi.org/project/django-debug-toolbar/) ships a new design! I again didn't contribute a lot, but I'm very proud that we were able to ship this as a team.

### feincms3

[feincms3 6.0.2](https://pypi.org/project/feincms3/) ships new utilities and, most importantly, fixes crashes when passing `%00` to the root middleware. Using null bytes when comparing text field values on PostgreSQL leads to crashes. These are mostly an annoyance without data exposure, but definitely worth fixing.

The reason for the major version bump is that we finally dropped support for Django 3.2. That's the only breaking change, so upgrading should be easy for everyone.

### django-js-asset

[django-js-asset 4.1](https://pypi.org/project/django-js-asset/) fixes issues around lazy CSP nonce handling as well as the same issue Django itself had around [rendering HTML-safe strings](https://code.djangoproject.com/ticket/37262).

### django-prose-editor

[django-prose-editor 0.27.2](https://pypi.org/project/django-prose-editor/) adds a default menu item for the code block extension and updates ProseMirror and Tiptap. It also adapts to the changed CSS of the Django 6.1 administration interface.

### django-json-schema-editor

[django-json-schema-editor 0.14.1](https://pypi.org/project/django-json-schema-editor/) includes a fix for saving JSON schema fields when the schema doesn't contain any properties, plus fixes for the Django 6.1 admin CSS.

### django-admin-ordering

[django-admin-ordering 0.21](https://pypi.org/project/django-admin-ordering/) now activates orderables properly when the same model was orderable both in the change list and in the change form. I developed the fix for this in early 2025 but never released it. It's what happens.

### feincms3-cookiecontrol

[feincms3-cookiecontrol 1.7.2](https://pypi.org/project/feincms3-cookiecontrol/) includes bugfixes for edge cases while bringing down the byte count for the cookie banner and media embedding script from 3961 (in 1.7.1) to 3909 bytes.

### feincms3-data

[feincms3-data 0.11.1](https://pypi.org/project/feincms3-data/) brings fixes for handling unique fields when the same unique value is removed and then re-added with a different primary key.

### django-translated-fields

[django-translated-fields 0.14](https://pypi.org/project/django-translated-fields/) contains no relevant code changes to the module itself at all. It was just time to release a new version more than two years after the last release to show that the project is still active and update the Trove classifiers.
