Title: What did FeinCMS get right?
Slug: what-did-feincms-get-right
Date: 2018-09-22
Categories: Django, feincms, Programming
Type: markdown

# What did FeinCMS get right?

Here's a list of things FeinCMS got right. The list will never be exhaustive.

- _Sites are different_. Building a framework and not a single product covering all use cases is still a good idea. Also, we are building on top of Django, so we shouldn't have to sell the advantages of using a framework compared to using a ready-made CMS which looks better when comparing features but not when really working with it day to day.
- The ItemEditor and its structuring of content (e.g. keeping images separate, rigidly clean HTML blobs) is still the right way to do it, even though I can't disagree that the interface for editors might be improved.
- Making things reusable (the ItemEditor for blog entries, the TreeEditor for any tree shaped data) was the right thing to do. The tree editor code has its descendants (pun intended) everywhere, in django-mptt, in django-treebeard and also in other projects. It also seems to me that the same ideas ItemEditor implements have found their way into other projects, although I'm certainly not claiming credit for all those.
- Staying close to Django's administration interface instead of diverging (and having to rebuild functionality at great effort and cost) was the right decision to make and helps FeinCMS reach compatibility much faster with new versions of Django and other software FeinCMS depends on.
- Making it extensible, and keeping specialized content types out of the main repository lowered the activity in the repository, especially when compared to some other content management systems. This means less pressure on maintainers and it communicates clearly that writing your own content types is not only possible but expected and well supported.

This post is part of a series, [The future of FeinCMS](https://406.ch/writing/the-future-of-feincms/).
