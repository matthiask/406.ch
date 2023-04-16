Title: Continuous Integration
Slug: continuous-integration
Date: 2014-01-14
Categories: Programming
Type: markdown

How did I ever manage to release working packages without continuous integration?

More often than not I didn't. The first minor releases were always buggy, you had to wait until the first or second patch level if you wanted a complete and working package.

Of course a contributing factor to this was the desolate state of Python packaging. The state of affairs is much better than back then, and more improvements are already underway.

The tool I’m using for almost all of my regularly updated Python / Django packages is [Travis CI](https://travis-ci.org/).

The FeinCMS page status page is an example demonstrating (a small part of) what Travis CI is capable of: [FeinCMS](https://travis-ci.org/feincms/feincms).
