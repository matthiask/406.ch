Title: Weeknotes (2026 week 47)
Categories: Django, Programming, Weeknotes

I haven't done any blogging in the last 4 weeks. Instead, I've been writing a lot of code and have let the agent write even more code. I have finally managed to implement some tools I would have liked to implement a long time ago.


## Working with LLM agents

The [relationship with LLM agents](/writing/llms-for-open-source-maintenance-a-cautious-case/) doesn't get any easier, I have to admit. That said, the quality argument against LLMs seems less and less plausible to me. Some people (especially on Mastodon) will say that's because I'm losing view of what's actually important. As I see it, human-written code was never perfect either (maybe apart from the [Apollo Guidance Computer](https://en.wikipedia.org/wiki/Margaret_Hamilton_(software_engineer))). I can actually do good and solve more problems for real users with more than acceptable code quality now and that seems like a net benefit to me.


## [Governance](https://github.com/feinheit/governance) -- a Django app for Holacracy

As some people may know, we are using [Holacracy](https://www.holacracy.org/) as our organizational model at [Feinheit](https://feinheit.ch/). Holacracy One, the company behind Holacracy, also offers a SaaS solution for managing the structure consisting of circles, roles, policies etc. The tool is unfortunately quite buggy and slow, and hasn't improved in recent years -- to the contrary.

I have reimplemented the parts we actually use using Django, Bootstrap and htmx while profiting from years and years of product engineering going into [the Workbench agency software](/writing/workbench-the-django-based-agency-software/).

It won't surprise anyone that after the first rush of getting a half-functioning, half-assed prototype out of the agent it was a lot of work to actually make the tool somewhat consistent, usable and correct. The bar to replace the tool we've been using before wasn't that high, so I was able to cross that in a few days of concentrated work.

I think that this project wouldn't have been doable without the deep knowledge of the organizational model (the domain knowledge) and the product engineering and UX background.


## An experimental API and CLI for [feincms3](https://feincms3.readthedocs.io/)

The [feincms3-api](https://pypi.org/project/feincms3-api/) and [feincms3-api-cli](https://pypi.org/project/feincms3-api-cli/) allow interacting with a feincms3-managed site. The API allows reading and writing pages and other objects with their regions and plugins, django-json-schema-editor data and django-cabinet files. It's meant for scripts, importers and agents, next to the Django admin, not instead of it. The CLI (`f3api`) makes the API available from the command line. Writes can be tried as a dry run first, and changes show up in the admin's history like any other edit.

Permissions, editable fields etc. are all handled by the Django admin. Since feincms3 and django-content-editor lean heavily on [Django's administration interface](/writing/the-django-admin-is-a-cms/) this was an easy decision to make. Plugins can be arbitrary models and we don't have an obvious way to discover them, or even know what their structure is apart from introspection or manual work. The constraints of working in an agency are such that I cannot spend a lot of time on each individual project; I really need reusable tools which can be applied to many websites and projects at once. It can be acceptable for the result to not be perfect or a little awkward as long as it is [simple and understandable](https://en.wikipedia.org/wiki/Leaky_abstraction).


## Releases

### feincms3 and django-content-editor

The rendering engine from [feincms3](https://pypi.org/project/feincms3/) has been ported to [django-content-editor](https://pypi.org/project/django-content-editor/) and lives there now. [Nested sections](/writing/django-content-editor-now-supports-nested-sections/) stay in feincms3 as a backwards compatible implementation, the new implementation in django-content-editor is much nicer because it doesn't require section closing plugins. Instead, all plugins have a `depth` field and form a tree structure that way; a new level is opened by a plugin which is marked as a container. Many such container plugins can coexist.

Also, the new releases fully build on the [importmap DEP API](/writing/weeknotes-2026-week-40/), and include many bugfixes which will not be mentioned in detail here.

[feincms3-sites](https://pypi.org/project/feincms3-sites/) has also received a small update and a few bugfixes.

### [django-cabinet](https://pypi.org/project/django-cabinet/)

The media library now supports moving files with drag'n'drop and has a collapsible folder tree on the left for quicker navigation.

### [django-json-schema-editor](https://pypi.org/project/django-json-schema-editor/)

The proxy models created by `JSONPluginBase.proxy()` are automatically injected into the Python module now; this allows Django's model autoimporter in `./manage.py shell` to discover those models, which avoids many, many warnings.

### [django-prose-editor](https://pypi.org/project/django-prose-editor/)

I am always tracking Tiptap and ProseMirror closely. The editor now has a deeper integration with django-cabinet -- inserted files keep their ID around. Apart from that, mostly minor changes.

### [django-js-asset](https://pypi.org/project/django-js-asset/)

I have released django-js-asset 5.0 implementing the `ImportMap` specification which I'm still hoping to bring to Django core.

### [form-designer](https://pypi.org/project/form-designer/)

Bugfixes, French, Catalan and Spanish translations, and a small security fix (don't inadvertently add formulas to generated XLSX files, the fix is in xlsxdocument below).

### [django-authlib](https://pypi.org/project/django-authlib/)

Hardened the Microsoft Entra ID adapter. Fixed a few bugs and improved docs.

### [django-imagefield](https://pypi.org/project/django-imagefield/)

I did finally release a new stable release of django-imagefield containing the still experimental vips backend.

### [django-translated-fields](https://pypi.org/project/django-translated-fields/)

`TranslatedField` now handles model fields with broken^Wcustomized `deconstruct` methods properly. For example, feincms3's `ChoicesCharField` hides the choices from Django's migrations, so changing choices doesn't create pointless migrations (they wouldn't produce any SQL anyway). However, the previous implementation required that fields are reconstructible from the return value of `deconstruct`, which means that such fields could not be used with `TranslatedField`. Now they can.

### [django-tree-queries](https://pypi.org/project/django-tree-queries/)

Fixed an edge case crash, allowed customizing the node moving machinery to reject targets and slightly modernized the code.

### [feincms3-cookiecontrol](https://pypi.org/project/feincms3-cookiecontrol/)

The cookie banner now supports Google's advanced consent mode out of the box, if you opt in to it as the one implementing it (not as a visitor to the website!). I think supporting that mode is good, because while the mode itself is very questionable, having a simple and straightforward implementation for it is better than having to choose one of the really, really complex and user-hostile consent management platforms.

### [feincms3-forms](https://pypi.org/project/feincms3-forms/)

The proxy models created by the forms builder are now injected into their module. Same problem as above, in django-json-schema-editor.

### Other releases

- I still seem to be maintaining [django-mptt](https://pypi.org/project/django-mptt/), even though it has been marked as unmaintained for years. Fixed some tree corruption bugs and regressions.
- [xlsxdocument](https://pypi.org/project/xlsxdocument/) doesn't insert formulas anymore except if they are tagged using a new `Formula` object. form-designer uses it for its XLSX export.
- [speckenv](https://pypi.org/project/speckenv/) now supports configuring Django's `MAILERS` setting from the environment as well. The format is the same as the one used by `django_email_url` and `dj-email-url`. Also includes more fixes for configuration cases I hadn't encountered before.
- [towel](https://pypi.org/project/towel/) and [towel-foundation](https://pypi.org/project/towel-foundation/), two packages from back in the day when I was a stronger believer in the DRY principle. Note that I have been moving away from that for years. I'd rather have some repetition than more indirection these days.
- [html-sanitizer](https://pypi.org/project/html-sanitizer/) now knows how to preserve whitespace within `<pre>` tags.
- The venerable [FeinCMS](https://pypi.org/project/FeinCMS/) and [feincms-elephantblog](https://pypi.org/project/feincms-elephantblog/) are in maintenance mode, but have received updates and releases.
- Fixed a minor bug affecting [django-admin-ordering](https://pypi.org/project/django-admin-ordering/) models which handled comparisons with unrelated objects incorrectly.
- Updated the [django-sitemaps](https://pypi.org/project/django-sitemaps/) README and published a new release, just because.
- [django-ckeditor](https://pypi.org/project/django-ckeditor/) now uses the new django-js-asset API.
- [django-email-hosts](https://pypi.org/project/django-email-hosts/) now supports `MAILERS`.
