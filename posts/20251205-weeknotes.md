Title: Weeknotes (2025 week 49)
Categories: Django, Programming, Weeknotes

I seem to be publishing weeknotes monthly, so I'm now thinking about renaming the category :-)

## Mosparo

I have started using a self-hosted [mosparo](https://mosparo.io/) instance for my captcha needs. It's nicer than Google reCAPTCHA. Also, not sending data to Google and not training AI models on traffic signs feels better.

## Fixes for the YouTube 153 error

Simon Willison published a nice writeup about [YouTube embeds failing with a 153 error](https://simonwillison.net/2025/Dec/1/youtube-embed-153-error/). We have also encountered this problem in the wild and fixed the [feincms3](https://feincms3.readthedocs.io/en/latest/ref/embedding.html) embedding code to [also set the required referrerpolicy attribute](https://github.com/feincms/feincms3/commit/3f00e5d2a15991d52f9ae0118b49fe231ea328d0).

## Updated packages since 2025-11-04

- [django-sitemaps 2.0.2](https://pypi.org/project/django-sitemaps/): Uploaded a new release which includes a wheel build. Rebuilding the wheel all the time when creating new container images was getting annoying. The code itself is unchanged.
- [django-prune-uploads 0.3.1](https://pypi.org/project/django_prune_uploads/): The package now supports pruning a storage backed by django-s3-storage efficiently. I have also looked at [django-prune-media](https://pypi.org/project/django-prune-media/) but since the package uses the storage API instead of enumerating files using boto3 directly it's unusably slow for my use case.
- [feincms3-forms 0.6](https://pypi.org/project/feincms3-forms/): Much better docs and a new way to reference [individual form fields in custom templates](https://github.com/feincms/feincms3-forms?tab=readme-ov-file#custom-templates-for-compound-fields).
- [django-json-schema-editor 0.11](https://pypi.org/project/django-json-schema-editor/): Switched from JSON paths to `jmespath` instances. Made the JSON model instance reference support easier and more fun to use. Added new ways of customizing the generated proxy model for individual JSON plugin instances.
- [form-designer 0.27.1](https://pypi.org/project/form-designer/): Added support for the [mosparo captcha](https://mosparo.io/) to the default list of field types.
- [asgi-plausible 0.1.1](https://pypi.org/project/asgi-plausible/): No code change really, just added required dependencies to the package metadata.
- [django-tree-queries 0.23](https://pypi.org/project/django-tree-queries/): The package now ships a `OrderableTreeNode` base model which you can use when you want to order siblings manually. feincms3 already uses this base model for its pages model.
- [feincms3-data 0.10](https://pypi.org/project/feincms3-data/): This is quite a big one. I discovered issues with the way `save_as_new` (to copy data) and `delete_missing` interacted. First the code was cleaned up to delete less data, and then to delete enough data. I'm now somewhat confident that the code does what it should again.
- [django-prose-editor 0.22.3](https://pypi.org/project/django-prose-editor/): Started returning an empty string for an empty document instead of `<p></p>` also when using the frontend integration; previously, this transformation was only implemented when using at least the form if not the model field. Also, `<ol>` tags now have a `data-type` attribute since Chrome cannot case-sensitively match e.g. `type="a"` vs `type="A"` for lowercase or uppercase letters. I previously only tested the code in Firefox and there it worked nicely.
