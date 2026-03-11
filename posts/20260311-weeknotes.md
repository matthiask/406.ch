Title: Weeknotes (2026 week 11)
Categories: Django, Programming, Weeknotes

Last time I wrote that I seem to be publishing weeknotes monthly. Now, a quarter of a year has passed since the [last entry](https://406.ch/writing/weeknotes-2025-week-49/). I do enjoy the fact that I have published more posts focused on a single topic. That said, what has been going on in open source land is certainly interesting too.

## LLMs in Open Source

I have started a longer piece to think about my stance regarding using LLMs in Open Source. The argument I'm thinking about is that there's a balance between LLMs having ingested all of my published open source code and myself using them now to help myself and others again.

The happenings in the last two weeks (think Pentagon, Iran, and the bombings of schools) have again brought to the foreground the perils of using those tools. I therefore haven't been motivated to pursue this train of thought for the moment. When the upsides are somewhat questionable and tentative and the downsides are so clear and impossible to miss, it's hard to use my voice to speak in favor of these tools.

That said, all the shaming when someone uses an LLM that I see in my Mastodon feed also annoys me. I'll quote part of a post here which I liked and leave it at that for the moment:

> The AI hype-cyclone is bad, but so is the anti-AI witch hunt. Commits co-authored by Claude do not mean that a project has "abandoned engineering as a serious endeavor"
>
> [...]

-- [@nedbat on Mastodon](https://hachyderm.io/@nedbat/116133445557306539)

## Other goings-on

- **Health:** My back continues to improve. Some days are still bad, but the idea that the [herniation](https://406.ch/writing/my-2025-in-review/#sports-and-health) may go away entirely doesn't sound totally unreasonable anymore.
- **Gardening:** We started weeding the garden last week. Lots to do! Being outside is fun. Weeding isn't the greatest part ever, but it's meditative.

## Releases since December

- [django-json-schema-editor 0.12.1](https://pypi.org/project/django-json-schema-editor/): CSS fixes. I have again looked at other, more modern JSON schema editor implementations but all of them are more limited than is acceptable to act as a replacement.
- [django-debug-toolbar 6.2](https://pypi.org/project/django-debug-toolbar/): I haven't done much work here! Just some reviewing.
- [django-content-editor 8.1](https://pypi.org/project/django-content-editor/): Started emitting warnings when using non-abstract base classes for plugins. Using multi table inheritance is mostly an accident and not intended in my experience when using django-content-editor, therefore we have started detecting this case and emitting system checks (warnings, not errors).
- [django-imagefield 0.23.0a3](https://pypi.org/project/django-imagefield/): We have done some work on supporting [libvips](https://www.libvips.org/) as an alternative backend to Pillow because I hoped that memory usage in Kubernetes pods might go down a bit. Results are not conclusive yet, and I'm not yet convinced the additional code complexity is worth it. Debugging and monitoring continues.
- [FeinCMS 26.2.1](https://pypi.org/project/FeinCMS/): Released a few bugfixes. FeinCMS is still being maintained ~17 years later!
- [django-auto-admin-fieldsets 0.3](https://pypi.org/project/django-auto-admin-fieldsets/): Added a helper to remove fields from the fieldsets structure.
- [django-tree-queries 0.23.1](https://pypi.org/project/django-tree-queries/): Shipped a small bugfix for `{% recursetree %}` which unintentionally cached children across invocations.
- [feincms3-downloads](https://pypi.org/project/feincms3-downloads/): Used `PATH` from the environment instead of using a very restricted allowlist so that `convert` and `pdftocairo` are detected in more locations. This should help with local development for example on macOS.
- [django-prose-editor 0.24.1](https://pypi.org/project/django-prose-editor/): Read the [CHANGELOG](https://django-prose-editor.readthedocs.io/en/latest/changelog.html); there's too much in there for a short notice.
- [form-designer 0.27.3](https://pypi.org/project/form-designer/): Mosparo captcha support, bugfixes and additional translations.
- [feincms3 5.5](https://pypi.org/project/feincms3/): Started using the `OrderableTreeNode` from django-tree-queries.
