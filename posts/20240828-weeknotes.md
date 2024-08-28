Title: Weeknotes (2024 week 35)
Categories: Django, Programming, Weeknotes

## Getting deep into htmx and django-template-partials

I have been skeptical about [htmx](https://htmx.org/) for some time because basically everything the library does is straightforward to do myself with a few lines of JavaScript. I am a convert now because, really, adding a few HTML attributes is nicer than copy pasting a few lines of JavaScript. Feels good.

The combination of htmx with [django-template-partials](https://github.com/carltongibson/django-template-partials/) is great as well. I didn't know I had been missing template partials until I started using them. Includes are still useful, but replacing some of them with partials makes working on the project much more enjoyable.

I haven't yet had a use for [django-htmx](https://django-htmx.readthedocs.io/) but I may yet surprise myself.

## Releases

- [django-authlib 0.17](https://pypi.org/project/django-authlib/): django-authlib bundles `authlib.little_auth` which offers an user model which uses the email address as the username. I have also introduced the concept of [roles instead of permissions](https://406.ch/writing/keep-content-managers-admin-access-up-to-date-with-role-based-permissions/); now I have reorganized the user admin fieldset to hide user permissions altogether. Group permissions are still available as are roles. I'm personally convinced that user permissions were a mistake.
- [feincms3-forms 0.5](https://pypi.org/project/feincms3-forms/): Allowed setting a maximum length for the bundled URL and email fields through the Django administration interface.
- [django-content-editor 7.0.7](https://pypi.org/project/django-content-editor/): Fixed a bug where plugins with several fieldsets weren't collapsed completely.
- [django-imagefield 0.19.1](https://pypi.org/project/django-imagefield/): Allowed deactivating autogeneration of thumbnails completely through the ``IMAGEFIELD_AUTOGENERATE`` setting. This is very useful for batch processing. Also, documented all available settings.
- [django-prose-editor 0.8](https://pypi.org/project/django-prose-editor/): Added support for translating the interface elements and for restricting the available heading levels in the UI.
- [form-designer 0.25](https://pypi.org/project/form-designer/): Fixed the type of the author field for the send-to-author processing action.
- [feincms3 5.2.2](https://pypi.org/project/feincms3/): Added support for embedding [SRF play](https://www.srf.ch/play/tv) external content. They do not support oEmbed unfortunately.
- [feincms3-cookiecontrol 1.5.3](https://pypi.org/project/feincms3-cookiecontrol/): Added support for SRF play embeddings as well. The difference is that the feincms3-cookiecontrol embedding requires consent before embedding external content.
