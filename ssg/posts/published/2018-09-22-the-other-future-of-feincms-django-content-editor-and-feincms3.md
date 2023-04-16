Title: The other future of FeinCMS: django-content-editor and feincms3
Slug: the-other-future-of-feincms-django-content-editor-and-feincms3
Date: 2018-09-22
Categories: Django, feincms, Programming
Type: markdown

# The other future of FeinCMS: django-content-editor and feincms3

The FeinCMS ItemEditor code lives on in a new project, [django-content-editor](https://django-content-editor.readthedocs.io/)<sup>1</sup>.

By contrast [feincms3](https://feincms3.readthedocs.io/) is a completely new project, which was the result of starting to build websites with a stripped down environment of django-content-editor and django-mptt<sup>2</sup> only.

feincms3 avoids many of the downsides of FeinCMS 1.x by doing less. At first sight it sounds like building a website with feincms3 will be more work. In my view this does not have to be, since feincms3 offers more direct ways of achieving the same results.

feincms3 addresses [FeinCMS' issues](https://406.ch/writing/the-state-of-things-in-feincms-1x-land/) by:

- It does not offer concrete models, only mixins. Because of this, all problems with dynamic model creation and the extensions mechanism simply disappear.
- You write the page model yourself, so you'll know what fields it has.
- No request and response processors, and plugins (content types in FeinCMS 1.x) do not have any ways of interferring with request and response processing. This makes at all times obvious what's going to happen when processing a request. Redirects? Easy, DIY in your own, short view function.
- The automatic creation of inlines for the admin interface is gone. This avoids the custom `feincms_item_editor_inline` protocol, and its coupling of models and the administration interface.
- Models do not have a render method. Instead, there's a [renderer](https://feincms3.readthedocs.io/en/latest/build-your-cms.html#rendering-and-templates) where you're supposed to register plugins. This makes it straightforward to use different renderers for different purposes, and the preferred way to achieve this is obvious.
- The new application mixin (replacing FeinCMS 1.x `ApplicationContent`) works with Django's own `reverse()` without any monkey patching.
- And last but not least feincms3 does not only not ship a complicated view function, it does not ship a view function _at all_. The reason is that [writing feincms3 views is extremely straightforward](https://feincms3.readthedocs.io/en/latest/build-your-cms.html#views-and-urls) and mostly requires only a few feincms3-specific lines of code in real-world projects.

1. The TreeEditor has been added to [django-mptt](https://django-mptt.readthedocs.io/en/latest/admin.html#mptt-admin-draggablempttadmin) as `DraggableMPTTAdmin`.
2. We have since moved to [django-tree-queries](https://github.com/matthiask/django-tree-queries), but now's not the time for this story. Search through feincms3's [CHANGELOG](https://feincms3.readthedocs.io/en/latest/project/changelog.html) if you want to know more right now.

This post is part of a series, [The future of FeinCMS](https://406.ch/writing/the-future-of-feincms/).
