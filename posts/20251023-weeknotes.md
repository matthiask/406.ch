Title: Weeknotes (2025 week 43)
Categories: Django, Programming, Weeknotes

I published the last weeknotes entry in the first half of September.

## Drama in OSS

I have been following the Ruby gems debacle a bit. Initially at [Feinheit](https://feinheit.ch/) we used our own PHP-based framework [swisdk2](https://github.com/matthiask/swisdk2) to build websites. This obviously didn't scale and I was very annoyed with PHP, so I was looking for alternatives.

I remember comparing Ruby on Rails and Django, and decided to switch from PHP/swisdk2 to Python/Django for two reasons: The automatically generated admin interface and the fact that Ruby source code just had too much punctuation characters for my taste. It's a very whimsical reason and I do not put any weight on that. That being said, given how some of the exponents in Ruby/Rails land behave I'm very very glad to have chosen Python and Django. While not everything is perfect (it never is) at least those communities agree that trying to behave nicely to each other is something to be cheered and not something to be sneered at.

## Copilot

I assigned some GitHub issues to Copilot. The result wasn't very useful. I don't know if I want to repeat it, local tools work fine for when I really need them.

## Python and Django compatibility

It's the time again to update the GitHub actions matrix and Trove identifiers. I do not like doing it. You can expect all maintained packages to be compatible with the latest and best versions, no upper bounds necessary. Man, if only AI could automate _those_ tasks...

## Updated packages since 2025-09-10

- [feincms3](https://pypi.org/project/feincms3/): We use `hashlib.md5`, but not for security.
- [django-tree-queries 0.21.2](https://pypi.org/project/django-tree-queries/): django-tree-queries now bundles an admin interface for trees.
- [django-content-editor 8.0.3](https://pypi.org/project/django-content-editor/): Minor CSS fix so that the editor looks nicer with Django 6.0.
- [django-json-schema-editor 0.8.1](https://pypi.org/project/django-json-schema-editor/): Fixes for multiple JSON editors in the same window, better `JSONPlugin.__str__` default implementation.
- [django-cabinet 0.18.1](https://pypi.org/project/django-cabinet/): Fix a minor bug around the selected folder handling. Invalid folder ID values could crash the backend under some circumstances.
- [django-prose-editor 0.18.5](https://pypi.org/project/django-prose-editor/): No large changes, mainly Tiptap updates.
