Title: Writing documentation
Slug: writing-documentation
Date: 2018-09-22
Categories: Django, Programming
Type: markdown

# Writing documentation

## Why do I like writing documentation?

A good part of it is that I am writing docs for myself. Similar to writing tests or commit messages, writing docs is a way of thinking about the same issues from a different viewpoint, with a different part of the brain so to speak.

Sometimes code feels bad, but it's hard to tell why. Surprisingly often the badness really shows itself as soon as I start writing docs. The [Zen of Python](https://www.python.org/dev/peps/pep-0020/) says it much better than I could:

> If the implementation is hard to explain, it's a bad idea.
>
> If the implementation is easy to explain, it may be a good idea.

## When do I write documentation?

I mostly start writing documentation when the first or second iteration of a project basically works and when it is time to move towards the beta quality stage. Documenting alpha quality software is mostly not worth the effort; it only adds documentation churn to code churn.

Documenting a 1.0 release is too late except for trivial software, since documenting often surfaces simpler ways to achieve the same results.

## Docs I spent a lot of time on

I'm quite proud of the following projects' documentation:

### [feincms3](https://feincms3.readthedocs.io/)

The first versions were only documented using docstrings and autodoc, the current version is split into different sections: First steps, guides and reference. Readers should be able to understand and use the information in guides independently, without having to read everything.

### [django-translated-fields](https://github.com/matthiask/django-translated-fields)

A simple project with little functionality; the README is the only documentation this project has. Still, the README is almost three times longer than the packages' Python code combined.

### [html-sanitizer](https://github.com/matthiask/html-sanitizer)

I wish all my projects' documentations had a short paragraph at the top explaining what the project is about, how it compares to other solutions attacking the same problem space and provide a list of goals the project is supposed to achieve.
