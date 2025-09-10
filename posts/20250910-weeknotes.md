Title: Weeknotes (2025 week 37)
Categories: Django, Programming, Weeknotes

I'm having a slow week after the last wisdom tooth extraction. Finally! I'm slowly recuperating from that.

Also, I'm trying to split up the blog posts a bit and writing more standalone pieces instead of putting everything into weeknotes. This seems like a good idea to publish more, and should also help me when I try to find a particular piece of writing later.

## Releases

- [django-content-editor 8.0.2](https://pypi.org/project/django-content-editor/): I fixed the ordering calculation in the cloning functionality; the tests are a bit too forgiving for my taste now but I just can't figure out why the gap for inserting cloned items is sometimes larger than it should be. It doesn't matter though, since ordering values do not have any significance, they only have to provide a definite ordering for content items.
- [django-prose-editor 0.18.2](https://pypi.org/project/django-prose-editor/): Cleaned up the documentation after the 0.18 cleanup (where automatic dependency management has been removed), fixed table styles when using dark mode.
