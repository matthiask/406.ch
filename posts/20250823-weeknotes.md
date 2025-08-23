Title: Weeknotes (2025 week 34)
Categories: Django, Programming, Weeknotes
Draft: remove-this-to-publish

Summer was and is nice. The hot days seem to be over (for now), but in the last
years summer hasn't really left until the end of September, so we'll see.


## Releases

- [django-debug-toolbar 6.0](https://pypi.org/project/django-debug-toolbar/):
  We have released a new version of the toolbar which supports persisting
  debugging data to the database. This is especially useful when using ASGI,
  because we cannot use threadlocal storage for this data then.
- [django-prose-editor 0.17](https://pypi.org/project/django-prose-editor/):
  Reworked the menu system to support dropdowns, not just button groups. Added
  a custom ``TextClass`` extension which allows adding classes to spans. Tiptap
  supports adding arbitrary styles, I'd rather limit this a bit more and only
  offer predefined CSS classes.
- [django-content-editor 8.0](https://pypi.org/project/django-content-editor/):
  Added support for cloning content. Made the region tabs stick to the top of
  the browser window.
