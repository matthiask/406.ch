Title: Low maintenance software
Slug: low-maintenance-software
Date: 2017-06-05
Categories: Django, Programming

I'm passionate about writing low maintenance software.

To achieve this software must be simple, opinionated, and often written as a library, not a framework. While it seems easier to write a framework with extension points it is, in the long run, more useful to build powerful tools.

Applying these principles to Django apps means that often it isn't very useful to supply views and URLconf modules, but instead supply forms and helpers that make writing your own views more straightforward.

Glue code is often different between projects anyway, and in my opinion views are just that: Glue code.

That is why the first release of [django-authlib](https://django-authlib.readthedocs.io/) did not ship with any views; only with helpers that make writing your own views for implementing authentication based on verified email addresses more straightforward.

I now ship views; but those views are not configurable or extensible. The idea is that if those views are not exactly what you need, you should write your own (and in fact we often do exactly that when using authlib in our projects)

Another illustration of these principles is the comparison between [FeinCMS' view code](https://github.com/feincms/feincms/blob/master/feincms/module/mixins.py) and [feincms3's view code](https://github.com/matthiask/feincms3-example/blob/master/app/pages/views.py). The former uses the framework approach: Build a complex (and complicated) machinery with plugin points, processors and whatnot, the latter offers powerful tools which require very little glue code. This makes the location for adding custom behavior more obvious – you can place it directly in the view code. The alternative of using inversion of control, and understanding when and how you can add your own code makes the barrier of entry much higher.
