Title: django-json-schema-editor
Date: 2023-12-13
Categories: Django, Programming

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

## Links:

- [PyPI](https://pypi.org/project/django-json-schema-editor/)
- [GitHub](https://github.com/matthiask/django-json-schema-editor)
