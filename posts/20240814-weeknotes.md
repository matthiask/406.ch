Title: Weeknotes (2024 week 33)
Categories: Django, Programming, Weeknotes

## Partying

It's summer, it's hot, and it's dance week. [Lethargy](https://lethargy.ch/) is over, [Jungle Street Groove](https://www.junglestreetgroove.ch/) is coming up. Good times.


## Releases

- [django-json-schema-editor 0.1](https://pypi.org/project/django-json-schema-editor/): I have finally left the alpha versioning. I'm still not committing to backwards compatibility, but I have started writing a CHANGELOG.
- [django-prose-editor 0.7.1](https://pypi.org/project/django-prose-editor/): Thanks to Carlton's pull request I have finally cleaned up the CSS somewhat and made overriding the styles more agreeable when using the editor outside the Django administration. The confusing active state of menubar buttons has also been rectified. [Docs are now available on Read the Docs.](https://django-prose-editor.readthedocs.io/)
- [django-imagefield 0.19](https://pypi.org/project/django-imagefield/): django-imagefield can now be used with proxy models. Previously, thumbnails weren't generated or deleted when saving proxy models because the signal handlers would only be called if the `sender` matches exactly. I have already debugged this before, but have forgotten about it again. The ticket is really old for this, and fixing it isn't easy since it's unclear what should happen ([#9318](https://code.djangoproject.com/ticket/9318)).
- [django-canonical-domain 0.11](https://pypi.org/project/django_canonical_domain/): django-canonical-domain has gained support for excluding additional domains from the canonical domain redirect. django-canonical-domain is used to redirect users to HTTPS (optionally) and to a particular canonical domain (as the name says). But sometimes you have auxiliary domains, e.g. for an API service, which shouldn't be redirected. The package can now be used in these scenarios as well.
- [FeinCMS 24.8.2](https://pypi.org/project/FeinCMS/): The venerable FeinCMS, now more than 15 years old. The thumbnailing support had a bug where it tried saving JPEGs using RGBA (which obviously doesn't work). This has been fixed.
