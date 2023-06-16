Title: FeinCMS is a dead end (but feincms3 is not)
Date: 2023-06-19
Categories: Django, Programming, feincms

# FeinCMS is a dead end (but feincms3 is not)

I wouldn't encourage people to start new sites with FeinCMS. Five years ago I wrote that [FeinCMS is used in a few flagship projects which we’re still actively developing, which means that FeinCMS won’t be going away for years to come.](https://406.ch/writing/the-future-of-feincms/) That's still true but less and less so. We're actively moving away from FeinCMS where we can, mostly towards feincms3 and django-content-editor.

[FeinCMS lives on in django-content-editor and feincms3](https://406.ch/writing/the-other-future-of-feincms-django-content-editor-and-feincms3/); not only in spirit but also in (code) history, since django-content-editor contains the whole history of FeinCMS up to and including the beginning of 2016.

The implementation of FeinCMS is too expensive to clean up without breaking backwards compatibility. I still wish I had pursued an incremental way back then which would have allowed us to evolve old projects to the current best way of doing things (tm), but it didn't happen and I'm not shedding too many tears about that since I'm quite happy with where we're at today.

That basically means that I won't put any effort into [bringing FeinCMS and django-content-editor closer together](https://406.ch/writing/bringing-feincms-and-django-content-editorfeincms3-closer-together/). I haven't spent much time on that anyway but now my mind is made up that this wouldn't be time well spent. That being said, some of the items mentioned in the blog post linked above are available in django-content-editor now.
