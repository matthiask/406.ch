Title: Weeknotes (2024 week 39)
Categories: Django, Programming, Weeknotes

## CSS for Django forms

Not much going on in OSS land. I have been somewhat active in the official
Django forum, discussing ways to add Python-level hooks to allow adding CSS
classes around form fields and their labels. The discussion on the
[forum](https://forum.djangoproject.com/t/proposal-make-it-easy-to-add-css-classes-to-a-boundfield/32022)
and on the [pull request](https://github.com/django/django/pull/18266) goes in
the direction of allowing using custom `BoundField` classes per form or even
per project (instead of only per field as is already possible today). This
would allow overriding `css_classes`, e.g. to add a simple `class="field"`.
Together with `:has()` this would probably allow me to skip using custom HTML
templates in 99% of all cases.

I have also been lurking in the Discord, but more to help and less to promote
my packages and ideas :-)


## Releases

- [django-user-messages 1.1](https://pypi.org/project/django_user_messages/):
  Added Django 5.0, 5.1 to the CI, and fixed the migrations to no longer
  mention `index_together` at all. It seems that squashing the migrations
  wasn't sufficient, I also had to actually delete the old migrations.
- [blacknoise 1.1](https://pypi.org/project/blacknoise/):
  [Starlette](https://www.starlette.io/)'s `FileResponse` has gained support
  for the HTTP Range header, allowing me to remove my homegrown implementation
  from the package. The blacknoise implementation is now half as long as it was
  in 1.0.
- [django-fhadmin 2.3](https://pypi.org/project/django_fhadmin/): No new
  features, only tweaks to the styling and behavior prompted by updates to
  Django's admin interface.
- [django-cabinet 0.17](https://pypi.org/project/django-cabinet/): I have
  pruned the CI matrix and accepted a pull request adding a ru translation. I
  feel conflicted about that since I strongly believe that everything is
  political, but I don't know if rejecting translations helps anyone.
