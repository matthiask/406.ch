Title: Weeknotes (2024 week 11)
Date: 2024-03-16
Categories: Django, Programming, Weeknotes
Draft: remove-this-to-publish

## Tech won't save us

I have recently discovered [Tech won't save us](https://www.techwontsave.us/),
a Podcast which is critical of the technological "progress" offered by Silicon
Valley elites. It's a great antidote for the generative AI hype.

I still have some stupid hope that AGI will solve our problems because maybe
people will trust a computer more than scientists that something has to be done
about the combined crisis we're facing as humans. Who knows. I do not want to
be too negative about it though, there are positive news if you're looking in
the right places.

I myself do not write about those bigger issues [as
much](https://406.ch/writing/category-climate/) [as I used
to](https://406.ch/writing/category-politik/). I support those more important
issues elsewhere.


## AI hype

AI is certainly not helping *me* in my work. I do not want a computer to
generate code which I have to review and maintain when I still enjoy writing
code myself. Maybe that will change at some point in the future. When that
happens I'll probably retire and become a gardener or something.


## Estimates

[Jacob wrote an excellent post on breaking down tasks](https://jacobian.org/2024/mar/11/breaking-down-tasks/). I did like the post a lot. Maybe I'll write a longer reply later, but for now just this. [There definitely are good reasons for the pushback against estimation](https://hachyderm.io/@jacob@jacobian.org/112081126379604868), and it's really not just that some people lack professionalism.

## Releases

- [django-cabinet 0.14.1](https://pypi.org/project/django-cabinet/): Mini
  release containing a Turkish translation. It's always nice if software is
  used.
- [feincms3 4.6](https://pypi.org/project/feincms3/): Fixed a bug where the
  move form wouldn't use a potentially overridden `ModelAdmin.get_queryset`
  method.
- [form-designer 0.24](https://pypi.org/project/form-designer/): Updated the
  package for django-recaptcha 4.0.
- [html-sanitizer 2.3.1](https://pypi.org/project/html-sanitizer/): Fixed an
  edge case sanitization bug (luckily without security implications).
- [django-content-editor
  6.4.2](https://pypi.org/project/django-content-editor/):
  django-content-editor now again supports transitioning plugin fieldsets when
  opening *and* closing thanks to CSS grid's ability to animate the maximum
  height of an element. Also, the initialization in 6.4 was badly broken.
- [django-prose-editor 0.2](https://pypi.org/project/django-prose-editor/): [See the announcement blog post from Wednesday](https://406.ch/writing/django-prose-editor-prose-editing-component-for-the-django-admin/).
