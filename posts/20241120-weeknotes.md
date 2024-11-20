Title: Weeknotes (2024 week 47)
Categories: Django, Programming, Weeknotes
Draft: remove-this-to-publish


I missed a single co-writing session and of course that lead to four weeks of no posts at all to the blog. Oh well.


## Debugging

I want to share a few debugging stories from the last weeks.


### Pillow 11 and Django's `get_image_dimensions`

The goal of [django-imagefield](https://github.com/matthiask/django-imagefield)
was to deeply verify that Django and Pillow are able to work with uploaded
files; some files can be loaded, their dimensions can be inspected, but
problems happen later when Pillow actually tries resizing or filtering files.
Because of this django-imagefield does more work when images are added to the
system instead of working around it later. (Django doesn't do this on purpose
because doing all this work up-front could be considered a DoS factor.)

In the last weeks I suddenly got recurring errors from saved files again,
something which shouldn't happen, but obviously did.

Django wants to read image dimensions when accessing or saving image files (by
the way, always use `height_field` and `width_field`, otherwise Django will
open and inspect image files even when you're only loading Django models from
the database...!) and it uses a smart and wonderful[^fn1] hack to do this: It reads a few hundred bytes from the image file, instructs Pillow to inspect the file and if an exception happens it reads more bytes and tries again. This process relies on the exact type of exceptions raised internally though, and the release of Pillow 11 changed the types... for some file types only. Fun times.

The issue had already been reported as
[#33240](https://code.djangoproject.com/ticket/33240). Let's see what happens.
For now, django-imagefield declares itself to be incompatible with Pillow
11.0.0 so that this error cannot happen.

[^fn1]: wonderfully ugly


### rspack and lightningcss shuffled CSS properties

[rspack](https://rspack.dev/) 1.0 started reordering CSS properties which of course lead to CSS properties overriding each other in the incorrect order. That was a fun one to debug. I tracked the issue down to the switch from the swc CSS minimizer to [lightningcss](https://github.com/parcel-bundler/lightningcss) and submitted a reproduction to the [issue tracker](https://github.com/parcel-bundler/lightningcss/issues/805#issuecomment-2358219597). My rust knowledge wasn't up to the task of attempting to submit a fix myself. Luckily, it has been fixed in the meantime.


### rspack problems

I have another problem with rspack where I haven't yet tracked down the issue. rspack produces a broken bundle starting with [1.0.0-beta.2](https://github.com/web-infra-dev/rspack/releases/tag/v1.0.0-beta.2) when compiling a particular project of mine. I have the suspicion that I have misconfigured some stuff related to import paths and yarn workspaces. I have no idea how anyone could have a complete understanding of these things...

Bundlers are complex beasts, and I'm happy that I mostly can just use them.


### Closing thoughts

Debugging is definitely a rewarding activity for me. I like tracking stuff down like this. Unfortunately, problems always tend to crop up when time is scarce already, but what can you do.


## Releases

Quite a few releases, many of them verifying Python 3.13 and Django 5.1 support (if it hasn't been added already in previous releases). The nicest part: If I remember correctly I didn't have to change anything anywhere, everything just continues to work.

- [django-admin-ordering 0.19](https://pypi.org/project/django-admin-ordering/): I added support for automatically renumbering objects on page load. This is mostly useful if you already have existing data which isn't ordered yet.
- [feincms3-data 0.7](https://pypi.org/project/feincms3-data/): Made sure that objects are dumped in a deterministic order when dumping. I wanted to compare JSON dumps by hand before and after a big data migration in a customer project and differently ordered dumps made the comparison impossible.
- [django-prose-editor 0.9](https://pypi.org/project/django-prose-editor/): I updated the ProseMirror packages, and put the editor into read-only mode for `<textarea disabled>` elements.
- [feincms3-language-sites 0.4](https://pypi.org/project/feincms3-language-sites/): Finally released the update containing the necessary hook to validate page trees and their unique paths before moving produces integrity errors. Error messages are nicer than internal server errors.
- [django-authlib 0.17.2](https://pypi.org/project/django-authlib/): The value of the cookie which is used to save the URL where users should be redirected to after authentication wasn't checked for validity when setting it, only when reading it. This meant that attackers could produce invalid header errors in application servers. No real security problem here when using authlib's code.
- [feincms3 5.3](https://pypi.org/project/feincms3/): Minor update which mostly removes support for outdated Python and Django versions.
- [django-imagefield 0.20](https://pypi.org/project/django-imagefield/): See above.
