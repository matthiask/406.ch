Title: Weeknotes (2024 week 07)
Date: 2024-02-16
Categories: Django, Programming, Weeknotes

This is a short weeknotes entry which mainly contains a large list of releases. The reason for the large list is that I haven't published a weeknotes entry in weeks.

## Releases

- [form-designer 0.23](https://pypi.org/project/form-designer/): Only small changes, mainly updated the package for current Django and Python versions.
- [feincms3-cookiecontrol 1.4.6](https://pypi.org/project/feincms3-cookiecontrol/): A minor change: Swallow exceptions which happen during startup when clobbering the scripts data fails. As an aside: I find it funny that I have discovered the `.f3cc` class in some cookie banner blocklists. It feels good to be recognized even if this maybe isn't the nicest way, but it works for me since I actually do not like cookie banners either. At least feincms3-cookiecontrol doesn't inject anything without users' consent, and doesn't require a third party service to run.
- [django-simple-redirects 2.2.0](https://pypi.org/project/django_simple_redirects/): Minor release which adds a search field to the admin changelist. django-simple-redirects is a repackaged version of `django.contrib.redirects` without the `django.contrib.sites` dependency.
- [speckenv 6.2](https://pypi.org/project/speckenv/): `django_cache_url` now supports parsing redis configuration for a leader-replica redis installation with a read-write leader host and read-only replica hosts. I use the same configuration format as [django-cache-url](https://github.com/epicserve/django-cache-url) does.
- [django-debug-toolbar 4.3](https://pypi.org/project/django-debug-toolbar/): I haven't done much here, just some reviewing here and there. I enjoy the Djangonaut Space contributions a lot.
- [django-cabinet 0.14](https://pypi.org/project/django-cabinet/): I have removed the constraint which enforces unique names for subfolders. Enforcing the uniqueness does make sense, but it also makes bulk-updating the media library using serialized data more painful than it should be. It's a clear case of worse is better for me. If people want to confuse themselves I'm not going to stop them (anymore, in this case) but it makes the rest of the code so much easier to write that it's not even funny.
- [html-sanitizer 2.3](https://pypi.org/project/html-sanitizer/): This release contains a nice contribution which removes some whitespace which has been added by the sanitizer when merging adjacent tags of the same type, e.g. `<strong>abc</strong><strong>def</strong>`.
- [django-ckeditor 6.7.1](https://pypi.org/project/django-ckeditor/): See above.
- [django-json-schema-editor 0.0.11](https://pypi.org/project/django-json-schema-editor/): Fixed a crash which happened when not providing the optional (!) configuration. Shit happens. I should really have a test suite for this package.
- [feincms3 4.5.2](https://pypi.org/project/feincms3/): Disables the CKEditor version check.
- [django-content-editor 6.4](https://pypi.org/project/django-content-editor/): The first release since December 2022! Very stable software. The editor now restores the collapsed state of inlines and the scroll position when using "Save and continue editing". This is especially useful if editing an object with many content blocks.
