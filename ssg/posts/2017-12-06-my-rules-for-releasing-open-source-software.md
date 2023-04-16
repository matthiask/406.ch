Title: My rules for releasing open source software
Slug: my-rules-for-releasing-open-source-software
Status: published
Date: 2017-12-06
Categories: Django, Programming
Type: markdown

# My rules for releasing open source software

I maintain and help maintain quite a few Open Source Python packages. Possibly well-known packages include **django-debug-toolbar**, **django-ckeditor**, **django-mptt**, and **FeinCMS** resp. **feincms3**.

Open source development used to stress me greatly. I was always worrying whether the code is polished enough, whether I didn't introduce new bugs and whether the documentation is sufficient.

These days I still think about these things, but I do not worry as much as I used to. The reason for this are the following principles:

1. A fully passing test suite on Travis CI is a sufficient quality guarantee for a release.
2. Do not worry about release notes, but always keep the [CHANGELOG](https://django-content-editor.readthedocs.io/en/latest/#change-log) up to date.
3. Put out patch releases even for the smallest bugfixes and feature additions (as long as they are backwards compatible). Nobody wants to wait for the next big release, it always takes longer than intended.
4. Good enough is perfection.
