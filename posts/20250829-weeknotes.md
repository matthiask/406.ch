Title: Weeknotes (2025 week 35)
Categories: Django, Programming, Weeknotes

Summer was and is nice. The hot days seem to be over (for now), but in the last
years summer hasn't really left until the end of September, so we'll see. I
personally like the warm weather but I really hoped that our leaders were
smarter. The [climate emergency](https://406.ch/writing/category-climate/)
could be seen from far away. The pigheadedness is hard to stomach. And of
course it's not the only problem we're facing as humanity at all.

## Releases

I did some longer-form writing about two of the releases here: [Menu improvements in django-prose-editor](https://406.ch/writing/menu-improvements-in-django-prose-editor/) and [django-content-editor now supports cloning of content](https://406.ch/writing/django-content-editor-cloning/)

- [django-debug-toolbar 6.0](https://pypi.org/project/django-debug-toolbar/):
  We have released a new version of the toolbar which supports persisting
  debugging data to the database. This is especially useful when using ASGI,
  because we cannot use threadlocal storage for this data then.
- [django-prose-editor 0.18](https://pypi.org/project/django-prose-editor/):
  Reworked the menu system to support dropdowns, not just button groups. Added
  a custom `TextClass` extension which allows adding classes to spans and a
  `NodeClass` extension which allows adding classes to nodes. Tiptap supports
  adding arbitrary styles, I'd rather limit this a bit more and only offer
  predefined CSS classes.
- [django-content-editor 8.0](https://pypi.org/project/django-content-editor/):
  Added support for cloning content. Made the region tabs stick to the top of
  the browser window.
- [django-mptt 0.18](https://pypi.org/project/django-mptt/): I still seem to be maintaining the project even though I officially marked the project as unmaintained [more than 4 years ago](https://github.com/django-mptt/django-mptt/commit/6f6c1c485f3adc1d579f8d22e0279ce1d52334f6).
