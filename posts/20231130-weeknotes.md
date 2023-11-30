Title: Weeknotes (2023 week 48)
Date: 2023-11-30
Categories: Django, Programming, Weeknotes

A few weeks have passed since the last update. The whole family was repeatedly
sick with different viruses etc... I hope that the worst is over now. Who
knows.

## 12-factor Django storage configuration

I should maybe write a longer and separate post about this, but [speckenv](https://pypi.org/project/speckenv/) has gained support for the Django `STORAGES` setting. No documentation yet, but it supports two storage backends for now, the file system storage and [django-s3-storage](https://github.com/etianen/django-s3-storage/), my go-to library for S3-compatible services.

Using it looks something like this:

    from speckenv import env
    from speckenv_django import django_storage_url

    STORAGES = {
        "default": django_storage_url(
            env(
                "STORAGE_URL",
                default="file:./media/?base_url=/media/",
                warn=True,
            ),
            base_dir=BASE_DIR,
        ),
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
        },
    }

Then, if you want to use S3 you can put something like this in your `.env` file:

    STORAGE_URL=s3://access-key:secret@bucket.name.s3.eu-central-1.amazonaws.com/media/

Or maybe something like this, if you want to serve media files without authentication:

    STORAGE_URL=s3://access-key:secret@bucket.name.s3.eu-central-1.amazonaws.com/media/?aws_s3_public_auth=False&aws_s3_max_age_seconds=31536000

## Releases

- [speckenv 6.1.1](https://pypi.org/project/speckenv/): See above.
- [feincms3-meta 4.6](https://pypi.org/project/feincms3-meta/): York has contributed support for emitting structured data records. Looks nice. No documentation yet.
- [django-tree-queries 0.16.1](https://pypi.org/project/django-tree-queries/): `.values()` and `.values_list()` queries are now handled better and more consistently than before.
