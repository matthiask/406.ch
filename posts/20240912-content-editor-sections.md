Title: django-content-editor now supports nested sections
Categories: Django, Programming, feincms3
Draft: remove-this-to-publish


[django-content-editor](https://django-content-editor.readthedocs.io/) (and
it's ancestor FeinCMS) has been the Django admin extension for editing content
consisting of reusable blocks since 2009. In the last years we have more and
more often started [automatically grouping related
items](https://feincms3.readthedocs.io/en/latest/guides/rendering.html#grouping-plugins-into-subregions),
e.g. for rendering a sequence of images as a gallery. Sometimes it's nice to
give editors more control. This has been possible by using blocks which open a subsection and blocks which close a subsection for a long time, but it hasn't been friendly to content managers, especially when using nested sections.

The content editor now has first-class support for such nested sections. Here's
a screenshot showing the nesting:

![django-content-editor with sections](https://406.ch/assets/20240911-content-editor-sections.png)




