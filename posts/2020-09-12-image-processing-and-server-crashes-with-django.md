Title: Image processing and server crashes with Django
Slug: image-processing-and-server-crashes-with-django
Date: 2020-09-12
Categories: Django, Programming

# Image processing and server crashes with Django

The default [ImageField](https://docs.djangoproject.com/en/3.1/ref/models/fields/#imagefield) model and form fields do not verify that [Pillow](https://pillow.readthedocs.io/en/stable/) is able to actually process the image file at all. They only verify the image files' headers. This is by design, since processing full images opens websites up to denial of service attacks.

The downside of this is that thumbnailing libraries have to guard against all sorts of invalid images. If they do not do this thoroughly an invalid (e.g. truncated) image file may crash a whole website. The worst which can happen (and this has happened to me a few times) is that it may even be impossible to replace the invalid image through the administration panel, because the customized admin widget _also_ crashes while generating a thumbnail. Now you need a programmer with access to the database to even be able to replace the image. And maybe the website editors upload the invalid image again...

Anyway, these experiences lead me to repeatedly researching solutions and in the end, in the spirit of the following [XKCD comic](https://xkcd.com/927/) I set out to write my own image field.

![XKCD Standards](https://imgs.xkcd.com/comics/standards.png)

The result of this work is **[django-imagefield](https://github.com/matthiask/django-imagefield)**, first published in March 2018. It has the following differentiating features:

- In-depth validation of images. It does not matter whether the images are uploaded through forms or assigned directly to the model instances. You should always get errors when an image isn't processable by Pillow later.
- Django system check errors when forgetting the width and height field. Django allows you to omit width and height caching fields from models, but when you do this, images are always accessed even when instantiating querysets. This is bad(tm) for performance.
- Ability to define processing pipelines, where thumbnails etc. are created eagerly instead of on-demand.
