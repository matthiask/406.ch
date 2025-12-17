Title: Rich text editors: How restrictive can we be?
Categories: Django, Programming, feincms

How restrictive should a rich text editor be? It's a question I keep coming back to as I work on FeinCMS and Django-based content management systems.

I published the last blog post on [django-prose-editor](https://github.com/feincms/django-prose-editor) specifically in August 2025, [Menu improvements in django-prose-editor](https://406.ch/writing/menu-improvements-in-django-prose-editor/). The most interesting part of the blog post was the short mention of the `TextClass` extension at the bottom which allows adding a predefined list of CSS classes to arbitrary spans of text.

In the meantime, I have spent a lot of time working on extensions that try to answer this question: the [`TextClass` extension](https://django-prose-editor.readthedocs.io/en/latest/textclass.html) for adding CSS classes to inline text, and more recently the [`NodeClass` extension](https://django-prose-editor.readthedocs.io/en/latest/nodeclass.html) for adding classes to nodes and marks. It's high time to write a post about it.

## Rich Text editing philosophy

> All of this convinced me that offering the user a rich text editor with too much capabilities is a really bad idea. The rich text editor in FeinCMS only has bold, italic, bullets, link and headlines activated (and the HTML code button, because that's sort of inevitable – sometimes the rich text editor messes up and you cannot fix it other than going directly into the HTML code. Plus, if someone really knows what they are doing, I'd still like to give them the power to shoot their own foot).

-- [Commit in the FeinCMS repository, August 2009](https://github.com/feincms/feincms/commit/70cd7a1244438d2ba97852256f77daa2c870c345#diff-556c5559a716059d4fb714ad34de6a9845870e8d55bbd2cb9d77c732eb961388), current version from [django-content-editor design decisions](https://django-content-editor.readthedocs.io/en/latest/design-decisions.html)

## Should we let users shoot themselves in the foot?

Giving power users an HTML code button would have been somewhat fine if only the editors themselves were affected. Unfortunately, that was not the case.

As a team we have spent more time than we ever wanted debugging strange problems only to find out that the culprit was a blob of CSS or JavaScript inserted directly into an unsanitized rich text editor field. We saw everything from a few reasonable and well scoped lines of CSS to hundreds of KiBs of hotlinked JavaScript code that broke layouts, caused performance issues, and possibly even created security vulnerabilities.

We have one more case of [Betteridge's law of headlines](https://en.wikipedia.org/wiki/Betteridge%27s_law_of_headlines) here.

## The pendulum swings

The first version of django-prose-editor which replaced the venerable CKEditor 4 in our project was much more strict and reduced -- no attributes, no classes, just a very short list of allowlisted HTML tags in the schema.

We quickly hit some snags. When users needed similar headings with different styles, we worked around it by using H2 and H3 — not semantic at all. I wasn't exactly involved in this decision; I just didn't want to rock the boat too much, since I was so happy that we were even able to use the more restricted editor at all in this project.

Everything was good for a while, but more and more use cases crept up until it was clear that something had to be done about it. First, the [`TextClass` extension](https://django-prose-editor.readthedocs.io/en/latest/textclass.html) was introduced to allow adding classes to inline text, and later also the [`NodeClass` extension](https://django-prose-editor.readthedocs.io/en/latest/nodeclass.html) mentioned above. This was a compromise: The customer wanted inline styles, we wanted as little customizability as possible without getting in the way.

That said, we obviously had to move a bit. After all, going back to a less strict editor or even offering a HTML blob injection would be worse. If we try to be too restrictive we will probably have to go back to allowing everything some way or the other, after all:

> The more you tighten your grip, Tarkin, the more star systems will slip through your fingers.

-- Princess Leia

## Combining CSS classes

The last words are definitely not spoken just yet. As [teased on Mastodon](https://hachyderm.io/@matthiask/115650714479718340) at the beginning of this month I am working on an even more flexible extension which unifies the `NodeClass` and `TextClass` extensions into a single `ClassLoom` extension.

The code is getting real world use now, but I'm not ready to integrate it yet into the official repository. However, you can use it if you want, it's 1:1 the version from a project repository. [Get the `ClassLoom` extension here](https://gist.github.com/matthiask/64ea64b539d63d45ff71467752c2f307).

This extension also allows combining classes on a single element. If you have 5 colors and 3 text styles, you'd have to add 15 combinations if you were only able to apply a single class. Allowing combinations brings the number of classes down to manageable levels.

## Conclusion

So, back to the original question: How restrictive can we be?

The journey from CKEditor 4's permissiveness through django-prose-editor's initial strictness to today's `ClassLoom` extension has been one of finding that balance. Each extension — `TextClass`, `NodeClass`, and now `ClassLoom` — represents a step toward controlled flexibility: giving content editors the styling options they need while keeping the content structured, maintainable, and safe.
