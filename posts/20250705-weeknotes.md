Title: Weeknotes (2025 week 27)
Categories: Django, Programming, Weeknotes

I have again missed a few weeks, so the releases section will be longer than usual since it covers six weeks.

## django-prose-editor

I have totally restructured the documentation to make it clearer. The [configuration chapter](https://django-prose-editor.readthedocs.io/en/latest/configuration.html) is shorter and more focussed, and the [custom extensions chapter](https://django-prose-editor.readthedocs.io/en/latest/custom_extensions.html) actually shows all required parts now.

The most visible change is probably the refactored menu system. Extensions now
have an `addMenuItems` method where they can add their own buttons to the menu
bar. I wanted to do this for a long time but have only just this week found a
way to achieve this which I actually like.

I've reported a bug to Tiptap where a `.can()` chain always succeeded even though the actual operation could fail ([#6306](https://github.com/ueberdosis/tiptap/issues/6306)).

Finally, I have also switched from [esbuild](https://esbuild.github.io/) to
[rslib](https://rslib.rs/); I'm a heavy user of rspack anyway and am more at
home with its configuration.


## django-content-editor

The 7.4 release mostly contains minor changes, one new feature is the
`content_editor.admin.RefinedModelAdmin` class. It includes tweaks to Django's
standard behavior such as supporting a `Ctrl-S` shortcut for the "Save and
continue editing" functionality and an additional warning when people want to
delete inlines and instead delete the whole object. This seems to happen often
even though people are shown the full list of objects which will be deleted.


## Releases

- [django-prose-editor 0.15](https://pypi.org/project/django-prose-editor/): See above
- [django-content-editor 7.4.1](https://pypi.org/project/django-content-editor/): See above.
- [django-json-schema-editor 0.5.1](https://pypi.org/project/django-json-schema-editor/): Now supports customizing the prose editor configuration (when using `format: "prose"`) and also includes validation support for foreign key references in the JSON data.
- [html-sanitizer 2.6](https://pypi.org/project/html-sanitizer/): The sanitizer started crashing when used with `lxml>=6` when being fed strings with control characters inside.
- [django-recent-objects 0.1.1](https://pypi.org/project/django_recent_objects/): Changed the code to use `UNION ALL` instead of `UNION` when determining which objects to fetch from all tables.
- [feincms3 5.4.1](https://pypi.org/project/feincms3/): Added experimental support for rendering sections. Sections can be nested, so they are more powerful than subregions. Also, added warnings when registering plugin proxies for rendering *and* fetching, since that will mostly likely lead to duplicated objects in the rendered output.
- [django-tree-queries 0.20](https://pypi.org/project/django-tree-queries/): Added `tree_info` and `recursetree` template tags. Optimized the performance by avoiding the rank table if easily possible. Added stronger recommendations to pre-filter the table using `.tree_filter()` or `.tree_exclude()` when working with small subsets of large datasets.
- [django-ckeditor 6.7.3](https://pypi.org/project/django-ckeditor/): Added a trove identifeir for recent Django versions. It still works fine, but it's deprecated and shouldn't be used since it still uses the unmaintained CKEditor 4 line (since we do not ship the commercial LTS version).
- [feincms3-cookiecontrol 1.6.1](https://pypi.org/project/feincms3-cookiecontrol/): Golfed the generated CSS and JavaScript bundle down to below 4000 bytes again, including the YouTube/Vimeo/etc. wrapper which only loads external content when users consent.
