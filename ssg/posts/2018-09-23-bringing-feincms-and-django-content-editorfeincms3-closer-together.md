Title: Bringing FeinCMS and django-content-editor/feincms3 closer together
Slug: bringing-feincms-and-django-content-editorfeincms3-closer-together
Status: published
Date: 2018-09-23
Categories: Django, feincms, Programming
Type: markdown

# Bringing FeinCMS and django-content-editor/feincms3 closer together

If I had more time those are the features I would try to implement next:

## Reimplement FeinCMS's TreeEditor using django-mptt's [DraggableMPTTAdmin](https://django-mptt.github.io/django-mptt/admin.html#mptt-admin-draggablempttadmin)

This shouldn't be a big effort. The toggleable booleans are probably the only feature from the `TreeEditor` that haven't made it into django-mptt.

## Add features to django-content-editor

### Moving content blocks as a group

It would be awesome if it was possible to collapse the content blocks' fieldsets, mark consecutive blocks and move them as a group.

### Adding content blocks in the middle and improving reordering

Right now it's only possible to add new content blocks at the end; only after saving is it allowed to move new blocks in-between pre-existing content. This is a limitation of django's `InlineFormset` respectively of django-content-editor's naive reuse which expects new inline instances to always be ordered after existing forms.

I suspect that by using flexbox's `order` attribute and some custom JavaScript code it should be possible to keep the ordering of inlines stable in the HTML code. If that was true the backend code wouldn't have to be changed, which would also keep maintenance lower for the future.

The `ItemEditor` from FeinCMS supports adding content in the middle, but if users dynamically add and remove other content blocks (which makes Django's `inlines.js` renumber all formsets) a crash when saving is almost a certainty.

## Reimplement FeinCMS's ItemEditor using [django-content-editor](https://django-content-editor.readthedocs.io/)

This shouldn't be too hard either. Right now the content editor's JavaScript code assumes too much about the `related_name` field of plugins' `parent` foreign key, but apart from this the content editor's code should work right away.

In FeinCMS-land, the `ItemEditorInline` should extend the `ContentEditorInline`. The biggest pain point with the `ItemEditorInline` is that it supports adding additional fields to individual instances' forms (the `admin_fields` [feature](https://feincms-django-cms.readthedocs.io/en/latest/integration.html#additional-customization-possibilities) of `ApplicationContent` requires this).

## There should be a good way to undo changes

Enough said.
