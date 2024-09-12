Title: django-content-editor now supports nested sections
Categories: Django, Programming, feincms3


[django-content-editor](https://django-content-editor.readthedocs.io/) (and
it's ancestor FeinCMS) has been the Django admin extension for editing content
consisting of reusable blocks since 2009. In the last years we have more and
more often started [automatically grouping related
items](https://feincms3.readthedocs.io/en/latest/guides/rendering.html#grouping-plugins-into-subregions),
e.g. for rendering a sequence of images as a gallery. But, sometimes it's nice
to give editors more control. This has been possible by using blocks which open
a subsection and blocks which close a subsection for a long time, but it hasn't
been friendly to content managers, especially when using nested sections.

The content editor now has first-class support for such nested sections. Here's
a screenshot showing the nesting:

![django-content-editor with sections](https://406.ch/assets/20240911-content-editor-sections.png)

Finally it's possible to visually group blocks into sections, collapse those
sections as once and drag and drop whole sections into their place instead of
having to select the involved blocks individually.

The best part about it is that the content editor still supports all Django
admin widgets, as long as those widgets have support for the Django
administration interface's [inline form
events](https://docs.djangoproject.com/en/latest/ref/contrib/admin/javascript/)!
Moving DOM nodes around breaks attached JavaScript behaviors, but we do not
actually move DOM nodes around after the initialization -- instead, we use
[Flexbox
ordering](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Ordering_flex_items)
to visually reorder blocks. It's a bit more work than using a ready-made
sortable plugin, but -- as mentioned -- the prize is that we don't break any
other Django admin extensions.


## Simple patterns

I previously already reacted to a blog post by Lincoln Loop here in my post [My
reaction to the block-driven CMS blog
post](https://406.ch/writing/my-reaction-to-the-block-driven-cms-blog-post/).

The latest blog post, [Solving the Messy Middle: a Simple Block Pattern for
Wagtail
CMS](https://lincolnloop.com/insights/simple-block-pattern-wagtail-cms/) was
interesting as well. It dives into the configuration of a
[Wagtail](https://wagtail.org/) stream field which allows composing content out
of reusable blocks of content ([sounds
familiar!](https://406.ch/writing/i-just-learned-about-wagtail-s-streamfield/)).
The result is saved in a JSON blob in the database with all the advantages and
disadvantages that entails.

Now, django-content-editor is a worthy competitor when you do not want to add
another interface to your website besides the user-facing frontend and the
Django administration interface.

The example from the Lincoln Loop blog post can be replicated quite closely
with django-content-editor by using sections. I'm using the
[django-json-schema-editor](https://pypi.org/project/django-json-schema-editor/)
package for the section plugin since it easily allows adding more fields if
some section type needs it.

Here's an example model definition:

    :::python
    # Models
    from content_editor.models import Region, create_plugin_base
    from django_json_schema_editor.plugins import JSONPluginBase
    from feincms3 import plugins

    class Page(models.Model):
        # You have to define regions; each region gets a tab in the admin interface
        regions = [Region(key="content", title="Content")]

        # Additional fields for the page...

    PagePlugin = create_plugin_base(Page)

    class RichText(plugins.richtext.RichText, PagePlugin):
        pass

    class Image(plugins.image.Image, PagePlugin):
        pass

    class Section(JSONPluginBase, PagePlugin):
        pass

    AccordionSection = Section.proxy(
        "accordion",
        schema={"type": "object", {"properties": {"title": {"type": "string"}}}},
    )
    CloseSection = Section.proxy(
        "close",
        schema={"type": "object", {"properties": {}}},
    )


Here's the corresponding admin definition:

    :::python
    # Admin
    from content_editor.admin import ContentEditor
    from django_json_schema_editor.plugins import JSONPluginInline
    from feincms3 import plugins

    @admin.register(models.Page)
    class PageAdmin(ContentEditor):
        inlines = [
            plugins.richtext.RichTextInline.create(models.RichText),
            plugins.image.ImageInline.create(models.Image),
            JSONPluginInline.create(models.AccordionSection, sections=1),
            JSONPluginInline.create(models.CloseSection, sections=-1),
        ]

The somewhat cryptic ``sections=`` argument says how many levels of sections
the individual blocks open or close.

To render the content including accordions I'd probably use a [feincms3
renderer](https://feincms3.readthedocs.io/en/latest/guides/rendering.html#using-marks).
At the time of writing the renderer definition for sections is a bit tricky.

    :::python
    from feincms3.renderer import RegionRenderer, render_in_context, template_renderer

    class PageRenderer(RegionRenderer):
        def handle(self, plugins, context):
            plugins = deque(plugins)
            yield from self._handle(plugins, context)

        def _handle(self, plugins, context, *, in_section=False):
            while plugins:
                if isinstance(plugins[0], models.Section):
                    section = plugins.popleft()
                    if section.type == "close":
                        if in_section:
                            return
                        # Ignore close section plugins when not inside section
                        continue

                    if section.type == "accordion":
                        yield render_in_context("accordion.html", {
                            "title": accordion.data["title"],
                            "content": self._handle(plugins, context, in_section=True),
                        })

                else:
                    yield self.render_plugin(plugin, context)

    renderer = PageRenderer()
    renderer.register(models.RichText, template_renderer("plugins/richtext.html"))
    renderer.register(models.Image, template_renderer("plugins/image.html"))
    renderer.register(models.Section, "")


## Closing thoughts

Sometimes, I think to myself, I'll "just" write a "simple" blog post. I get
what I deserve when using those forbidden words. This blog post is neither
short or simple. That being said, the rendering code is a bit tricky, the rest
is quite straightforward. The amount of code in django-content-editor and
feincms3 is reasonable as well. Even though it may look like a lot you'll still
be [running less code in
production](https://406.ch/writing/run-less-code-in-production-or-youll-end-up-paying-the-price-later/)
than when using comparable solutions built using Django.
