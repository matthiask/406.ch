Title: django-prose-editor – Prose-editing component for the Django admin
Date: 2024-03-13
Categories: Django, Programming

During the last few days I have been working on a prose-editing component for
the Django admin which will replace the basically dead
[django-ckeditor](https://406.ch/writing/django-ckeditor/) in all of my
projects. It is based on [ProseMirror](https://prosemirror.net/), in my opinion
the greatest toolkit for building prose editors for the web.

Here's a screenshot:

![django-prose-editor screenshot](https://406.ch/assets/20240313-prose-editor.png)

django-prose-editor is in active development; it's [available on
PyPI](https://pypi.org/project/django-prose-editor/) and is developed in the
open [here on GitHub](https://github.com/matthiask/django-prose-editor/). The
version at the time of writing is 0.2, and it's not yet used in production
environments, only in staging/preview environments. That will soon change
though.


## Researching alternatives to django-ckeditor

I have spent a lot of time evaluating alternatives. All of them are great
choices, and I don't want to bash any of them. But, I didn't feel good betting on any of the choices from the [WYSIWYG editors grid on Django Packages](https://djangopackages.org/grids/g/wysiwyg/).

A few packages have potential licensing issues. CKEditor 5's change to the GPL
is what basically killed django-ckeditor. The upcoming TinyMCE 7 version will
also change to the GPL according to the [TinyMCE GitHub
repository](https://github.com/tinymce/tinymce/). Froala only has a free trial.
The [django-summernote app](https://github.com/summernote/django-summernote/)
doesn't have a dedicated maintainer, so I wouldn't bet on it.
[django-prose](https://github.com/withlogicco/django-prose) uses Trix; there
are various reasons why I didn't want to bet on Trix, among them my personal
experience that it sometimes gets into a buggy state where only a full page
reload unfreezes the editor.

Other packages are basically [Markdown](https://en.wikipedia.org/wiki/Markdown)
editors. I like Markdown and use it for my blog. I don't think Markdown is a
good choice for a CMS which is used by people of many different skill levels. I
don't want to teach people to use the Markdown link syntax or the heading
syntax even if the editor helps out a bit.

Some of the remaining choices are using JavaScript widgets which haven't been
updated for a really long time or they are really code editors, not WYSIWYG
editors, also a no go.


## Deciding on going with ProseMirror

I have worked with [ProseMirror](https://prosemirror.net/) on and off since
October 2015, soon after the crowdfunding ended. It is used in a project where
people can write their own book with a standardized pipeline and process, where
the technical side of the project is implemented using Django, ProseMirror and
LaTeX. A hacked
[prosemirror-example-setup](https://github.com/ProseMirror/prosemirror-example-setup/)
still is good enough for this project.

The ProseMirror deep dive came much later, only a few years back, when
implementing an editor with more custom functionality such as annotations,
different ways of marking up text and even interactive elements within the
text, for example to use it as a cloze in teaching materials.

The learning curve is steep. I haven't worked with another library which was so
hard to get started with. It is my conviction that the reason for this is that
rich-text editing is actually a hard problem. The ProseMirror architecture and
implementation definitely makes sense when it finally clicks.

As additional bonuses the ProseMirror community is nice and ProseMirror is used
in a few large software projects which make me believe that the software has a
non-zero probability of being maintained in the long run.


## Current plans

The only thing which is configurable right now is the server-side sanitizing of
submitted HTML content. I plan on allowing some configurability, for example to
disable links when the content will only be used inside a card teaser which
itself is already a link. Too much configurability isn't a good thing though in
my mind, so I'll probably be slow to add features and rather keep complexity
low.

I'm definitely interested to hear from people who want to use the package but
cannot do so right now or who would want some additional features. Issues and
pull requests are welcome!
