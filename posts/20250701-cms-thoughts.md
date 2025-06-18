Title: Thoughts about Django-based content management systems
Categories: Django, Programming
Draft: remove-this-to-publish

!!! Attention
    This article contains polemics.

I have almost exclusively used Django for implementing content management
systems since 2008. (I have also choosed Django most of the time for everything
else related to backends.)

In this time, content management systems have come and gone. The big three
systems many years back were [django CMS](https://www.django-cms.org/),
[Mezzanine](https://github.com/stephenmcd/mezzanine) and
[our](https://feinheit.ch) own
[FeinCMS](https://406.ch/writing/the-future-of-feincms/).

During all this time I have always kept an eye open for other CMS than our own
but have steadily continued working in my small corner of the Django space. I
think it's time to write down why I have been doing this all this time, for
myself and only incidentally for others to read.


## Why not use Wagtail, django CMS or any of those alternatives?

The Django administration interface is actually great. Even though some people
suggest that it should be treated as a tool for developers only, recent
improvements to the accessibility and the general usability suggest otherwise.
I have written more about my views on this in [The Django admin is a
CMS](https://406.ch/writing/the-django-admin-is-a-cms/). Using and building on
top of the Django admin is a great way to immediately profit from all current
and future improvements without having to reimplement anything.

So, I don't want to have to reimplement Django's features, I want to add new
features on top.

Note that I don't want to dunk on anyone. But, I think it should be pointed out
that other systems do make it hard to adopt new Django versions on release day:

- The update cycle of many large apps using Django lag behind Django. Wagtail
  (in)famously declared an [upper version boundary for
  Django](https://github.com/wagtail/wagtail/discussions/12574) which makes it
  hard to adopt Django versions faster than Wagtail releases updates.
- Some django CMS components such as django-filer have lagged behind in the
  past. Looking at the CI matrix and the activity right now suggests that this
  is not the case anymore. (I wanted to use django-filer and have used it in a
  few projects, but have written
  [django-cabinet](https://406.ch/writing/django-cabinet-a-media-library-for-django/)
  after being discouraged by the complexity of the package.)

These larger systems have many more (very talented) people working on them. I'm
not saying I'm doing a better job. I'm saying that thinking about the code
you're running in production and being conservative about features you might
not need is a good thing. (See also [Run less code in production or you’ll end
up paying the price
later](https://406.ch/writing/run-less-code-in-production-or-youll-end-up-paying-the-price-later/)
and [Low maintenance
software](https://406.ch/writing/low-maintenance-software/).) I'm always
thinking about long term maintenance. I really don't want to maintain some of
these larger projects, or even parts of them. So I'd rather not adopt them for
projects which hopefully will be developed and maintained for a long time to
come.


## The rule of least power

From [Wikipedia](https://en.wikipedia.org/wiki/Rule_of_least_power):

> In programming, the rule of least power is a design principle that "suggests choosing the least powerful [computer] language suitable for a given purpose". Stated alternatively, given a choice among computer languages, classes of which range from descriptive (or declarative) to procedural, the less procedural, more descriptive the language one chooses, the more one can do with the data stored in that language.

Django itself already provides lots and lots of power, and adding even more
power to that maybe makes the tool a little bit too sharp to use safely.


## Editing heterogenous collections of content

Django admin's inlines are great, but they are not sufficient for building a
CMS. You need something to manage different types. django-content-editor does
that and has done that since 2009.

[When Wagtail introduced the StreamField in
2015](https://torchbox.com/blog/rich-text-fields-and-faster-horses/) it was
definitely a great update to an already great CMS but it wasn't a new idea
generally and not a new thing in Django land. They didn't say it was and [welcomed the fact that they also started using a better way to structure content](https://406.ch/writing/i-just-learned-about-wagtail-s-streamfield/).


## Why not put everything in one big rich text area?

Structured content is actually great.

"Designing connected content", also mentioned in
[feincms may still be relevant](https://406.ch/writing/feincms-may-still-be-relevant/)

Also, [What did FeinCMS get right?](https://406.ch/writing/what-did-feincms-get-right/)


## JSON plugins are great

Requirements change all the time. Using one database schema for many content
types is hard. Reducing everything into atoms and grouping them is much more
work than having meaningful plugins.

Of course, Django and the Django admin helps you less once you start using
JSON. Trade offs are unavoidable. Either you do dark magic with dynamic forms
or you reimplement widgets all over the place. Either you accept that
referenced models may not be there anymore or you write somewhat complicated
code to automatically update a m2m table with the data from the JSON, but then
you still wouldn't get all the benefits which you'd get normally when using the
[``on_delete``](https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ForeignKey.on_delete)
option.


## Great ways to automatically convert the list of plugins into something else

- Mobile first / content first: Everything has a defined order, but desktop
  devices can actually show things side-by-side.
- Automatic grouping of content into subregions.
- Section plugins, making decisions explicit when implementing a smart renderer
  gets too complicated (FCZ example!)
    - I wish the editor showed those sections and allowed me to treat them as
      such. I don't want to add tree behavior though. Open/close is a more
      flexible paradigm for this than adding parent relationships (as django CMS
      did).
- If the content editing interface isn't expressive enough to model deep nested
  relationships, the time has probably come anyway to think about the
  information architecture some more and extract meaningful units of complex
  content into their own content types. One of the simpler examples for
  something like this might be a photo album, which can either me modelled
  using a sequence of automatically grouped image plugins or as an album with
  photos in them. The former has the advantage that you can edit everything in
  one place, the latter the advantage that you can create a tailor-made
  interface for the album and you can also potentially reuse albums in
  different parts of your website.
