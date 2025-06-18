Title: CMS thoughts
Categories: Django, Programming
Draft: remove-this-to-publish

# CMS thoughts

I maybe want to write a series about implementing CMS nicely with Django and
django-content-editor and friends.

!!! Attention
    This article contains polemics.


## Why not use Wagtail, django CMS or any of those alternatives?

- Stock admin is actually great. Immediately profit from all improvements!
- Less maintenance is great.
- Running less code is great.
- The update cycle of basically everything which depends on Django itself is
  slower than the update cycle of Django itself. Having more code to check
  makes keeping up with Django harder. That means that django-content-editor
  and friends are usable with the newest versions of Django before they are
  even released while other projects are lagging behind even though there's
  much more people power behind those projects.

I'm always thinking about long term maintenance. I really don't want to
maintain some of these larger projects, or even parts of them.

My situation is special: I cannot spend a lot of time on a single project. I
spend little time on many many projects.

I know about someone who would have payed tens of thousands of francs just for
a CMS upgrade. They'd rather reimplement it on top of a less capable but much
more maintainable platform. And that's what the feincms family of tools is all
about.


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
generally and not a new thing in Django land. They didn't say it was, but still
something.


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
