Title: CMS thoughts
Categories:
Draft: remove-this-to-publish

# CMS thoughts

I maybe want to write a series about implementing CMS nicely with Django and
django-content-editor and friends.


## Why not use Wagtail, django CMS or any of those alternatives?

- Stock admin is actually great. Immediately profit from all improvements!
- Less maintenance is great.
- Running less code is great.
- The update cycle of everything else is much slower even though there are many
  many more people involved with those projects.

I'm always thinking about long term maintenance. I really don't want to
maintain some of these larger projects, or even parts of them.

My situation is special: I cannot spend a lot of time on a single project. I
spend little time on many many projects.

I know about someone who would have payed tens of thousands of francs just for
a CMS upgrade. They'd rather reimplement it on top of a less capable but much
more maintainable platform.


## Editing heterogenous collections of content

Django admin's inlines are great, but they are not sufficient for building a
CMS. You need something to manage different types. django-content-editor does
that and has done that since 2009.

The Wagtail stream field innovation isn't anything new. (I don't think anybody
said it was.)


## Why not put everything in one big rich text area?

Structured content is actually great.

"Designing connected content", also mentioned in
[feincms may still be relevant](https://406.ch/writing/feincms-may-still-be-relevant/)

Also, [What did FeinCMS get right?](https://406.ch/writing/what-did-feincms-get-right/)


## JSON plugins are great

Requirements change all the time. Using one database schema for many content
types is hard. Reducing everything into atoms and grouping them is much more
work than having meaningful plugins.


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
