Title: Menu improvements in django-prose-editor
Categories: Django, Programming

I have repeatedly mentioned the [django-prose-editor](https://pypi.org/project/django-prose-editor/) project in my [weeknotes](https://406.ch/writing/category-weeknotes/) but I haven't written a proper post about it since [rebuilding it on top of Tiptap at the end of 2024](https://406.ch/writing/rebuilding-django-prose-editor-from-the-ground-up/).

Much has happened in the meantime. A lot of work went into the menu system (as alluded to in the title of this post), but by no means does that cover all the work. As always, the [CHANGELOG](https://django-prose-editor.readthedocs.io/en/latest/changelog.html) is the authoritative source.

**0.11** introduced HTML sanitization which only allows HTML tags and attributes which can be added through the editor interface. Previously, we used [nh3](https://nh3.readthedocs.io/) to clean up HTML and protect against XSS, but now we can be much more strict and use a restrictive allowlist.

We also switched to using [ES modules and importmaps](https://406.ch/writing/django-javascript-modules-and-importmaps/) in the browser.

Last but not least 0.11 also introduced end-to-end testing using [Playwright](https://playwright.dev/).

The main feature in **0.12** was the switch to Tiptap 3.0 which fixed problems with shared extension storage when using several prose editors on the same page.

In **0.13** we switched from [esbuild](https://esbuild.github.io/) to [rslib](https://lib.rsbuild.dev/). Esbuild's configuration is nicer to look at, but rslib is built on the very powerful [rspack](https://rspack.dev/) which I'm using everywhere.

In **0.14**, **0.15** and **0.16** the `Menu` extension was made more reusable and the way extension can register their own menu items was reworked.

The upcoming **0.17** release (alpha releases are available and I'm using them in production right now!) is a larger release again and introduces a completely reworked menu system. The menu now not only supports button groups and dialogs but also dropdowns directly in the toolbar. This allows for example showing a dropdown for block types:

![Screenshot showing prose editor dropdowns](/assets/20250823-prose-editor-dropdowns.png)

The styles are the same as those used in the editor interface.

The same interface can not only be used for HTML elements, but also for HTML
classes. Tiptap has a
[TextStyle](https://tiptap.dev/docs/editor/extensions/functionality/text-style-kit)
extension which allows using inline styles; I'd rather have a more restricted
way of styling spans, and the prose editor `TextClass` extension does just
that: It allows applying a list of predefined CSS classes to `<span>` elements. Of course the dropdown also shows the resulting presentation if you provide the necessary CSS to the admin interface.
