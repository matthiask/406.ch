Title: Weeknotes (2023 week 50)
Date: 2023-12-13
Categories: Django, Programming, Weeknotes

## django-json-schema-editor

I have extracted a JSON editing component based on
[@json-editor/json-editor](https://www.npmjs.com/package/@json-editor/json-editor)
from a client's project and released it as open source. It isn't the first JSON editing component by far but I like it a lot for the following reasons:

- It works really well.
- It supports editing arrays of objects using a tabular presentation. Tabular
  isn't always better, but stacked definitely isn't always better as well.
- The data structure is defined as [JSON schema](https://json-schema.org/),the
  data which is being entered is validated on the server using the
  [fastjsonschema](https://pypi.org/project/fastjsonschema/) library. Having a
  schema and schema-based validation fixes most problems I have with less
  structured data than when using only Django model fields (without JSON).

Here's a screenshot of the editing component used as a [django-content-editor](https://django-content-editor.readthedocs.io/) plugin:

![django-json-schema-editor screenshot](/assets/20231313-json-schema-editor.png)

Within the first few days of having released the package it has already proven
useful in several other projects. A pleasant (but not totally unexpected)
surprise.

## django-imagefield

The path building scheme used by [django-imagefield](https://pypi.org/project/django-imagefield/) has proven problematic: It's too likely that processed images will have the same path.

I have changed the strategy used for generating paths to use more data from the
source; it's now possible (and recommended!) to set `IMAGEFIELD_BIN_DEPTH` to
a value greater than 1; 2 or 3 should be sufficient. The default value is 1
which corresponds to the old default so that the change won't be backwards
incompatible. However, you'll always get a deprecation warning if you don't set
a bigger value yourself. The default will probably change in the future.

## Advent of Code

I have always felt a bit as an imposter because I do not have any formal CS
education; not so much in the last few years but certainly earlier in my
career. I have enjoyed participating in the [Advent of Code
2022](https://adventofcode.com/) a lot and I have definitely learned to know
when to use and how to use a few algorithms I didn't even know before. I'm
again working through the puzzles in my own pace and have managed to solve
almost all of them up to today this year. The big exception is yesterday's
puzzle, I don't even know where to start 😅.

## Health

To absolutely nobody's surprise the family and myself have continued to be sick
in the last two weeks. Nothing really bad happened, so we're still lucky.
There's unfortunately no way to solve a societal problem individually, so that
will probably continue to be our life for now. Maybe it's over as of today, but
we'll see.

## Releases

- [django-imagefield 0.18](https://pypi.org/project/django-imagefield/): See
  above.
- [feincms3-sites 0.20.1](https://pypi.org/project/feincms3-sites/): Added
  additional validation (cleaning) checks. Showing error messages is
  preferrable to crashing with `IntegrityError` exceptions after all.
- [django-js-asset 2.2.0](https://pypi.org/project/django-js-asset/): Hatchling
  seems to dislike it if the project name and the Python module name do not
  match. I actually like `django-js-asset`'s Python module to be `js_asset`
  but I'm beginning to rethink this decision.
- [django-json-schema-editor 0.0.4](https://pypi.org/project/django-json-schema-editor/): See above.
