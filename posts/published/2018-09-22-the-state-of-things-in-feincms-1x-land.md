Title: The state of things in FeinCMS 1.x land
Slug: the-state-of-things-in-feincms-1x-land
Date: 2018-09-22
Categories: Django, feincms, Programming
Type: markdown

# The state of things in FeinCMS 1.x land

[FeinCMS](https://github.com/feincms/feincms) is still in active use, but not very actively developed. This does not have to be a bad thing -- FeinCMS is compatible with the recently released Django 2.1 back to Django 1.7, it works well and it's pain points are generally well known by long time users. Slow development also means minimal breakage because of new incompatibilities, not bad either.

That being said, here's a list of things with I find bothersome when working with FeinCMS:

- The extension mechanism and `create_content_type` are brittle. Many hacks and workarounds and fumbling with Django's internals were necessary over the years to avoid invalid and/or incomplete model meta information. Also, testing the dynamic creation of models is hard to test and most breakages were very hard to reproduce.
- It has a few features which make it hard to know what's going on. There's no single place to look if you want to know what fields the page model has. There's no place no look if you want to know what happens when processing a request because request and response processors and also the content types themselves all have ways to interfere and even short circuit request processing.
- The implicitness of the automatic registration of content type inlines with the administration interface made it necessary to invent new hacks (`feincms_item_editor_form` and `feincms_item_editor_inline`) to still be able to customize the inline class.
- Models and rendering is coupled too closely. Adding a `render()` method to content type models works well enough for small-to-medium sized websites, but falls apart quickly for infrastructure projects. The coupling itself does not prevent people from implementing better and more decoupled solutions, but doing the ugly thing is just too easy.
- The `ApplicationContent` way of integrating apps was nice, but mostly you wouldn't want more than one app per page anyway. The complexity cost of this flexibility e.g. for running apps (calling the resolver ourselves) and for reversing URLs (impossible to use Django's `reverse()` function directly) is higher than necessary.
- To be honest I don't understand the `feincms.extensions.translations` extension and its redirect mechanisms anymore.
- The reusability of the base model and the page view is enormously bad. Reimplementing the view by calling all processors and content types' `process()` and `finalize()` methods and so on is just horrible.

That being said, FeinCMS is used in a few flagship projects which we're still actively developing, which means that FeinCMS won't be going away for years to come.

This post is part of a series, [The future of FeinCMS](https://406.ch/writing/the-future-of-feincms/).
