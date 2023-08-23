Title: My reaction to the block-driven CMS blog post
Date: 2023-08-23
Categories: Django, Programming, feincms

# My reaction to the block-driven CMS blog post

This morning I read an interesting post on the Lincoln Loop blog called [Building a Future-Proof Platform with Block-Driven CMS](https://lincolnloop.com/insights/block-driven-cms-is-critical-build-a-future-proof/). It shouldn't come as a surprise to those (few 😄) who know my work in the area of content management systems that the post resonated with me. I found the description of the advantages of block-based CMS editing very clear and I like the emphasis on structuring data well so that it can be reused for multiple distribution channels.

Of course [django CMS](https://www.django-cms.org/) isn't the only way to implement a block-driven CMS using Django. Since its inception [FeinCMS](https://406.ch/writing/the-future-of-feincms/) was always the smaller, faster and nimbler counterpart to it, achieving the same _basic_ goals with a fraction of the code and maintenance headaches. django CMS always seems to trail the official releases of Django. django-content-editor and feincms3 are almost always compatible with the development version of Django by way of running the tests with the `main` branch as well. This allows me to be an early adopter of upcoming Django releases with a software stack that's already well tested, or also to report bugs to the Django project itself. All that probably wouldn't be possible if feincms3 and its dependencies supported all the things django CMS does, but it doesn't have to to be useful.

[django-content-editor and feincms3](https://406.ch/writing/the-other-future-of-feincms-django-content-editor-and-feincms3/) are the legacy of FeinCMS in an even smaller, even more maintainable and even more composable package and while I'm definitely always checking out other Django-based CMS I'm persuaded that sticking with feincms3 is a good choice.
