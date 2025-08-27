Title: django-content-editor now supports cloning of content
Slug: django-content-editor-cloning
Categories: Django, Programming

## What is the content editor?

Django’s builtin admin application provides a really good and usable
administration interface for creating and updating content.
`django-content-editor` extends Django's inlines mechanism with an interface
and tools for managing and rendering heterogenous collections of content as are
often necessary for content management systems.

[We](https://feinheit.ch) are using [django-content-editor](https://pypi.org/project/django-content-editor/) in basically all projects, as a part of [feincms3](https://pypi.org/project/feincms3/). The content editor is used not only for building page content, but also for blog entries, for [building multi-step intelligent form wizards](https://github.com/feincms/feincms3-forms), for [learning units](https://feinheit.ch/projekte/finance-mission-world/) and even to digitize teaching materials for schools, including static and interactive content.

The great thing about it is that it enables us to edit complex content inside Django's administration interface without trying to replace it with a completely separate interface, as some other more well-known Django-based CMS want to do.

## Cloning content

The complexity of managed content has grown a bit, especially since we introduced support for [nesting sections](https://406.ch/writing/django-content-editor-now-supports-nested-sections/). Teaching materials are often available in several learning levels, with only minor differences between them. Unfortunately, the differences aren't purely additive: It's not the case that higher levels just have more materials available. Otherwise, we'd probably have used a level on content items to hide content which shouldn't be shown to students. Content is sometimes totally different. Because of this we're using content editor's **regions** for the learning level, one region per level.

Even then, the basic structure is often the same and building that manually for all levels is annoying at best. That's why I finally got the occasion to add support for cloning content between regions to the editor.

Of course, cloning should also take the other features into account and allow selecting sections as a whole instead of having to select individual items. Here's a screenshot of the current interface:

![Screenshot showing the content cloning interface](/assets/20250827-content-editor-cloning.png)

## Closing thoughts

I'm still really happy with the content editor; I wish the Django admin would look a little bit nicer because then people would probably be more encouraged to actually learn how powerful it is. The first impression is unfortunately that it looks old and a bit too technical, but in my experience working with many many customers it's not really the case. Most people are immediately able to work with it and find the interface well structured and appreciate the no bullshit attitude, because working with it really is efficient.
