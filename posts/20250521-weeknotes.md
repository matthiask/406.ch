Title: Weeknotes (2025 week 21)
Categories: Django, Programming, Weeknotes

I have missed two co-writing sessions and didn't manage to post much outside of that, but let's get things back on track.


## django-prose-editor 0.12

The [last weeknotes
entry](https://406.ch/writing/weeknotes-2025-week-15/#progress-on-the-prose-editor)
contains more details about the work of really connecting Tiptap extensions
with server-side sanitization. 0.12 includes many improvements and bugfixes
which have been made during real-world use of the prose editor in
customer-facing products.

I'm not completely happy about the way we're specifying the editor
configuration and haven't been able to settle on either ``extensions`` or
``config`` as a keyword argument. The field supports both ways, at least for
now. It's probably fine.

## Releases

- [django-auto-admin-fieldsets 0.2](https://pypi.org/project/django-auto-admin-fieldsets/): I wrote a blog post here: [Customizing Django admin fieldsets without fearing forgotten fields](https://406.ch/writing/customizing-django-admin-fieldsets-without-fearing-forgotten-fields/)
- [django-debug-toolbar 5.2](https://pypi.org/project/django-debug-toolbar/): This release contains the second half of improvements from [Djangonaut Space](https://djangonaut.space/) session four where I helped out as a Navigator. The toolbar properly supports code highlighting in dark mode, sanitizes request variables better, allows customizing redirects, supports projects using [django-template-partials](https://github.com/carltongibson/django-template-partials/) and more!
- [FeinCMS 25.5.1](https://pypi.org/project/FeinCMS/): The first FeinCMS release of 2025. We're still maintaining the project and fixing bugs!
- [django-prose-editor 0.12](https://pypi.org/project/django-prose-editor/): See above.
- [django-json-schema-editor 0.4.1](https://pypi.org/project/django-json-schema-editor/): Fixes much too small checkboxes when used inside tables.
