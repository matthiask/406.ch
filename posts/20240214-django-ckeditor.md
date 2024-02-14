Title: django-ckeditor
Date: 2024-02-14
Categories: Django, Programming

# django-ckeditor

It has finally happened. The open source version of CKEditor 4 does not contain fixes for known problems, see [the CKEditor 4.24.0 LTS announcement](https://ckeditor.com/cke4/release/CKEditor-4.24.0-LTS).

I totally get why the CKEditor developers did this and can only thank them for all the work that went into the editor.

I wish I didn't have to do the migration work to move basically everything to a different editor. The CKEditor 4 LTS version is only expected to be supported until the end of 2026 and I have a few projects which will be around far longer than this (or at least I hope so). Therefore, buying the LTS package would only delay the inevitable. CKEditor 5 is a completely different editor and uses the GPL license, so that's not really an option either. TinyMCE is well known and I have been using it much earlier in my career, but reimplementing plugins isn't fun to do.

I would prefer moving everything to ProseMirror or some other structured editor, but we have so much legacy content contained in HTML blobs which do not use any schema at all that this isn't workable unfortunately.

Stay tuned for updates -- they will come since I unfortunately cannot just ignore this problem.

Which brings me to [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor). CKEditor shows a very annoying popup to users when it detects a newer version with security fixes, see [the GitHub issue](https://github.com/django-ckeditor/django-ckeditor/issues/761). It's not a bad idea but users cannot do much about it, so I opted to disable the version check (and warning) in django-ckeditor and replaced it with a Django system check which annoys developers instead.

The release containing these changes is available as [django-ckeditor 6.7.1](https://pypi.org/project/django-ckeditor/) on PyPI.
