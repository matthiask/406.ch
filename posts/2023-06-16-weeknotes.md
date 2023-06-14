Title: Weeknotes (2023 week 24)
Date: 2023-06-16
Categories: Django, Programming, Weeknotes, feincms

Life happened and I missed a month of weeknotes. Oh well.

## django-debug-toolbar 4.1

We have released [django-debug-toolbar
4.1](https://pypi.org/project/django-debug-toolbar/). Another cycle where I
mostly contributed reviews and not much else. Feels great :-)

## Going all in on hatch and hatchling

I got to know hatch because django-debug-toolbar was converted to it. I was
confused as probably anyone else with the new state of packaging in Python
world. After listening to a few Podcasts (for example [Hatch: A Modern Python
Workflow](https://talkpython.fm/episodes/show/408/hatch-a-modern-python-workflow))
I did bite the bullet and started converting projects to hatch as mentioned
[some time ago](https://406.ch/writing/weeknotes-2023-week-13-and-14/). I have
converted a few other projects in the meantime because the development
experience is nicer. Not much, but enough to make it worthwile.
[feincms3-sites](https://pypi.org/project/feincms3-sites/) is the latest
package I converted.

## CKEditor 5's new license and django-ckeditor

The pressure is on to maybe switch away from CKEditor 4 since it probably will not be supported after [June 2023](https://support.ckeditor.com/hc/en-us/articles/115005281629-How-long-will-CKEditor-4-be-supported-). It's totally understandable that the CKEditor 5 license isn't the same as before, but I'm not sure what that means for the Django integration [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor/issues/482) which I'm maintaining since a few years. I don't actually like the new capabilities of CKEditor all that much and don't intend to use them; maybe it would be better to use a build of [ProseMirror]() in the CMS since [we're intentionally only using a very small subset of the features most rich text editors offer](https://django-content-editor.readthedocs.io/en/latest/#about-rich-text-editors).

## Mountain biking.

My mountain bike is repaired, I'm back on the trail.
