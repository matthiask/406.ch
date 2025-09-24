Title: My favorite Django packages
Categories: Django, Programming
Draft: remove-this-to-publish

Inspired by other posts I also wanted to write up a list of my favorite Django
packages. Since I've been working in this space for so long and since I'm
maintaining quite a large list of packages I worry a bit about tooting my own
horn too much here; that said, the reasons for choosing some packages hopefully
speak for themselves.

Also, I'm sure I'm forgetting many many packages here. Sorry for that in advance.


## Core Django

- [speckenv](https://pypi.org/project/speckenv/): Loads environment variables from ``.env`` and automatically converts them to their Python equivalent if [`ast.literal_eval`](https://docs.python.org/3/library/ast.html#ast.literal_eval) understands it. Also contains implementations for loading database, cache, email and storage configuration from environment variables (similar to dj-database-url). I added this functionality to speckenv when some of the available environment configuration apps' maintenance state was somewhat questionable.
- [django-cors-headers](https://pypi.org/project/django-cors-headers/): CORS header support for Django. This would be a nice addition to Django itself.
- [sentry-sdk](https://pypi.org/project/sentry-sdk/): I'm using Sentry in almost all projects.
- [django-template-partials](https://pypi.org/project/django-template-partials/): Template partials for Django! This has been added to the upcoming 6.0 release of Django. While the Django template language has always been evolving and improving, this feels like the first larger step in a long time. As I and others have said, the combination of [htmx](https://htmx.org/) and django-template-partials is really really nice. It isn't surprising at all that htmx is so well loved in the Django community.
- [django-s3-storage](https://pypi.org/project/django-s3-storage/): Yes, django-storages exist, but I prefer django-s3-storage because of its focus and simplicity.
- [django-imagefield](https://pypi.org/project/django-imagefield/): Image field which validates images deeply, and supports pre-rendering thumbnails etc. I understand why Django only superficially validates uploaded images because of the danger of denial of service attacks, but I'd rather not have files on the sites I manage which the great [Pillow](https://pillow.readthedocs.io/) library doesn't support.
- [psycopg](https://pypi.org/project/psycopg/): Whenever I can I work with PostgreSQL, and psycopg is how I interface with the database.


## Data structures

- [django-tree-queries](https://pypi.org/project/django-tree-queries/): My
  favorite way to work with trees except when talking about real trees.
- [django-translated-fields](https://pypi.org/project/django-translated-fields/): My preferred way to do model-level internationalization.


## CMS building

I have been working on [FeinCMS](https://github.com/feincms/feincms/) since
2009. So, it shouldn't surprise anyone that this is still my favorite way to
build CMS on top of Django. I like that it's basically a thin layer on top of
Django's administration interface and doesn't want to take over the whole admin
interface or even the whole website.

- [feincms3](https://pypi.org/project/feincms3/): The modern, focussed foundation replacing FeinCMS.
- [django-content-editor](https://pypi.org/project/django-content-editor/): The admin interface extension.
Core components to build
- [django-prose-editor](https://pypi.org/project/django-prose-editor/): A nice HTML editor by yours truly.
- [django-json-schema-editor](https://pypi.org/project/django-json-schema-editor/): JSON schema-based editing using [@json-editor/json-editor](https://www.npmjs.com/package/@json-editor/json-editor).


## Working with external content

- [micawber](https://pypi.org/project/micawber/): Micawber is my favorite tool to embed third party content (YouTube, Vimeo, whatever).
- [feincms3-cookiecontrol](https://pypi.org/project/feincms3-cookiecontrol/): Everyone likes cookie banner (or not). feincms3-cookiecontrol implements not just an informative cookie banner, but actually supports not embedding tracking scripts and third party content unless the user consented, either a blanket or a per-provider consent for embedded media. It does NOT support the very annoying interface where you have to deselect each tracking service individually.


## PDF generation

- [Reportlab](https://pypi.org/project/reportlab/): Reportlab is nice if you need fine-grained control over PDF generation. Reportlab has created more than 10'000 invoices for the company I work at, so I'm definitely grateful for it :-)
- [Weasyprint](https://weasyprint.org/): I have been using Weasyprint more and more for generating PDFs. Using HTML and CSS can be nicer than using Reportlab's Platypus module. Weasyprint doesn't instrument a webbrowser to produce PDFs but instead implements the rendering engine itself. It works really well.


## Testing and development

- I actually do like unittest. I have started using [pytest](https://docs.pytest.org/en/stable/) somewhat more often because using `-k keyword` to filter tests to run is great.
- [factory-boy](https://pypi.org/project/factory-boy/): This package has always treated me well when creating data for tests.
- [playwright](https://playwright.dev/): Playwright is the end-to-end test browser automation library I prefer.

Last but not least, I really like [django-debug-toolbar](https://pypi.org/project/django-debug-toolbar/). So much, that I'm even helping with the maintenance since 2016.


## Serving

We mostly use Kubernetes to serve websites these days. Inside the pods, I'm working with the [granian](https://pypi.org/project/granian/) RSGI/ASGI server and with [blacknoise](https://pypi.org/project/blacknoise/) for serving static files.
