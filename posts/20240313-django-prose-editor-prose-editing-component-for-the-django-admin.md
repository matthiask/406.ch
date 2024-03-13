Title: django-prose-editor – Prose-editing component for the Django admin
Date: 2024-03-13
Categories: Django, Programming
Draft: remove-this-to-publish

During the last few days I have been working on a prose-editing component for
the Django admin which will replace the basically dead
[django-ckeditor](https://406.ch/writing/django-ckeditor/) in all of my
projects. It is based on [ProseMirror](https://prosemirror.net/), in my opinion
the greatest toolkit for building prose editors for the web.

Here's a screenshot:

![django-prose-editor screenshot](https://406.ch/assets/20240313-prose-editor.png)

The editor is in active development; it's [available on
PyPI](https://pypi.org/project/django-prose-editor/) and is developed in the
open [here on GitHub](https://github.com/matthiask/django-prose-editor/). The
version at the time of writing is 0.2, and it's not yet used in production
environments, only in staging/preview environments. That will soon change
though.


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


## Alternatives

A schema bsed

Besides the additional flexibility a schema-based editor offers the
The **upsides** of using a schema-based editor is that styling is so much easierthe editor always ensures that all content conforms to a more or less narrow schema. This makes is so much easier to

An alternative route would have been to find a CKEditor alternative -- an editor for editing HTML on the web.

## Alternatives

During my research I have stumbled upon many alternatives. All of them are great and I don't want to take anything away from them, but maybe the reasons why I have decided to roll my own package (while standing on the shoulders of giants) are interesting.

Packages
* **django-tinymce**: The venerable TinyMCE editor. I have been switching back and forth between TinyMCE and CKEditor for years. Both are great options if you weant
* **django-summernote**: It seemed to me that maintenace
