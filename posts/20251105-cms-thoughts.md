Title: Thoughts about Django-based content management systems
Categories: Django, Programming, feincms

I have almost exclusively used Django for implementing content management
systems (and other backends) since 2008.

In this time, content management systems have come and gone. The big three
systems many years back were [django CMS](https://www.django-cms.org/),
[Mezzanine](https://github.com/stephenmcd/mezzanine) and
[our](https://feinheit.ch) own
[FeinCMS](https://406.ch/writing/the-future-of-feincms/).

During all this time I have always kept an eye open for other CMS than our own
but have steadily continued working in my small corner of the Django space. I
think it's time to write down why I have been doing this all this time, for
myself and possibly also for other interested parties.

## Why not use Wagtail, django CMS or any of those alternatives?

Let's start with the big one. Why not use Wagtail?

The Django administration interface is actually great. Even though some people
say that it should be treated as a tool for developers only, recent
improvements to the accessibility and the general usability suggest otherwise.
I have written more about my views on this in [The Django admin is a
CMS](https://406.ch/writing/the-django-admin-is-a-cms/). Using and building on
top of the Django admin is a great way to immediately profit from all current
and future improvements without having to reimplement anything.

I don't want to have to reimplement Django's features, I want to add what I
need on top.

## Faster updates

Everyone implementing and maintaining other CMS is doing a great job and I
don't want to throw any shade. I still feel that it's important to point out
that systems can make it hard to adopt new Django versions on release day:

- The update cycle of many large apps using Django lag behind Django. Wagtail
  declares an [upper version boundary for
  Django](https://github.com/wagtail/wagtail/discussions/12574) which makes it
  hard to adopt Django versions faster than Wagtail releases updates.
- Some django CMS components such as
  [django-filer](https://github.com/django-cms/django-filer) have lagged behind
  in the past. Looking at the project's CI matrix and activity suggests that
  this is not the case anymore. That said, a [simpler alternative
  exists](https://406.ch/writing/django-cabinet-a-media-library-for-django/).

These larger systems have many more (very talented) people working on them. I'm
not saying I'm doing a better job. I'm only pointing out that I'm following a
different philosophy where I'm [conservative about running code in
production](https://406.ch/writing/run-less-code-in-production-or-youll-end-up-paying-the-price-later/)
and I'd rather [have less features when the price is a lot of maintenance
later](https://406.ch/writing/low-maintenance-software/). I'm always thinking
about long term maintenance. I really don't want to maintain some of these
larger projects, or even parts of them. So I'd rather not adopt them for
projects which hopefully will be developed and maintained for a long time to
come. By the way: This experience has been earned the hard way.

## The rule of least power

From [Wikipedia](https://en.wikipedia.org/wiki/Rule_of_least_power):

> In programming, the rule of least power is a design principle that "suggests choosing the least powerful [computer] language suitable for a given purpose". Stated alternatively, given a choice among computer languages, classes of which range from descriptive (or declarative) to procedural, the less procedural, more descriptive the language one chooses, the more one can do with the data stored in that language.

Django itself already provides lots and lots of power. I'd argue that a very
powerful platform on top of Django may be too much of a good thing. I'd rather
keep it simple and stupid.

## Editing heterogenous collections of content

Django admin's inlines are great, but they are not sufficient for building a
CMS. You need something to manage different types. django-content-editor does
that and has done that since 2009.

[When Wagtail introduced the StreamField in
2015](https://torchbox.com/blog/rich-text-fields-and-faster-horses/) it was
definitely a great update to an already great CMS but it wasn't a new idea
generally and not a new thing in Django land. They didn't say it was and
[welcomed the fact that they also started using a better way to structure
content](https://406.ch/writing/i-just-learned-about-wagtail-s-streamfield/).

Structured content is great. Putting everything into one large rich text area
isn't what I want. Django's ORM and admin interface are great for actually
modelling the data in a reusable way. And when you need more flexibility than
what's offered by Django's forms, the community offers many projects extending
the admin. These days, I really like working with the
[django-json-schema-editor](https://406.ch/writing/django-json-schema-editor/)
component; I even reference other model instances in the database and let the
JSON editor handle the referential integrity transparently for me (so that
referenced model instances do not silently disappear).

## More reading

[The future of FeinCMS](https://406.ch/writing/the-future-of-feincms/) and the [feincms category](https://406.ch/writing/category-feincms/) may be interesting. Also, I'd love to talk about these thoughts, either by email or on Mastodon.
