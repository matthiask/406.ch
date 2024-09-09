Title: Weeknotes (2024 week 37)
Categories: Django, Programming, Weeknotes
Draft: remove-this-to-publish

## django-debug-toolbar alpha with async support!

I have helped mentoring Aman Pandey who has worked all summer to add async
support to
[django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar/).
[Tim](https://github.com/tim-schilling) has released an alpha which contains
all of the work up to a few days ago. Test it! Let's find the breakages before
the final release.

## Releases

- [django-debug-toolbar 5.0.0a0](https://pypi.org/project/django-debug-toolbar/5.0.0a0/): See above.
- [form-designer 0.26.2](https://pypi.org/project/form-designer/): The values
  of choice fields are now returned as-is when sending mails or exporting form
  submissions instead of only returning the slugified version.
- [django-authlib 0.17.1](https://pypi.org/project/django-authlib/): The
  [role-based permissions
  backend](https://406.ch/writing/keep-content-managers-admin-access-up-to-date-with-role-based-permissions/)
  had a bug where it wouldn't return all available permissions in all
  circumstances, leading to empty navigation sidebars in the Django
  administration. This has been fixed.
- [feincms3 5.2.3](https://pypi.org/project/feincms3/): Bugfix release, the
  page moving interface is no longer hidden by an expanded navigation sidebar.
  I almost always turn off the sidebar in my projects so I haven't noticed
  this.
