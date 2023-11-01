Title: Weeknotes (2023 week 44)
Date: 2023-11-01
Categories: Django, Programming, Weeknotes
Draft: remove-this-to-publish

## Unmaintained but maintained packages

There's a discussion going on in the [django-mptt issue tracker](https://github.com/django-mptt/django-mptt/issues/833) about the maintenance state of django-mptt. [I have marked the project as unmaintained in March 2021](https://github.com/django-mptt/django-mptt/commit/6f6c1c485f3adc1d579f8d22e0279ce1d52334f6) and haven't regretted this decision at all. I haven't had to fix [inconsistencies in the tree structure](https://github.com/django-mptt/django-mptt/labels/Broken%20Tree) once since switching to [django-tree-queries](https://406.ch/writing/django-tree-queries/). And if that wasn't enough, I get little but only warm and thankful feedback for the latter, so that's extra nice.

Despite marking django-mptt as unmaintained I seem to be doing a little bit of maintenance still. I'm still using it in old paid projects and so the things I do to make the package work for me is paid work. I'm not personally invested in the package anymore, so I'm able to tell people that there are absolutely no guarantees about the maintenance, and that feels good.

## Read the Docs

I do understand why the `.readthedocs.yaml` file is now necessary. I wish that I wouldn't have to do all the busywork of adding one to projects. I have just resubscribed to the Read the Docs Gold Membership which probably has expired at some point in the past. Read the Docs is excellent and everybody who can should support them.

## Releases

- [towel 0.31](https://pypi.org/project/towel/): Towel is one of my oldest packages which is still being used in real-world projects. Towel is a tool for building CRUD-type applications and is designed to keep you DRY while doing that. The project has been heavily inspired by a Django-based agency software I built many years back. The package even has [docs](https://towel.readthedocs.io/en/latest/)! I'm still quite proud of the mostly transparent support for multitenancy, but apart from that I haven't used it in many new projects.
