Title: flake8 and the value of standards
Slug: flake8-and-value-standards
Date: 2014-08-08
Categories: Programming
Type: markdown

I really, really liked tabs for indentation.

I was also convinced that my indentation style -- or more generally, my coding style for that matter -- was the correct one, the only one that makes sense.

Coming back to old code, I can really appreciate the value of standards such as [PEP8](http://www.python.org/dev/peps/pep-0008/) now. My old coding style was too dense. It's hard to parse for a human mind because it lacks whitespace, which in turn means that less brain capacity is available for the actual functionality.

Code I've written a few years ago is also often too smart, using nested list comprehensions, lambdas and reduce all over the place. Those techniques are sometimes useful, and they really can make code easier to understand. But too often they were only used as a tool to put more behavior into less lines of code.

Nowadays, the deployment scripts always run [flake8](http://flake8.readthedocs.org/) and abort if any warnings come up. It enforces a more readable coding style and also finds real errors from time to time before they hit production (or the staging environment).

It’s actually the same about [GNOME](http://www.gnome.org/) or OS X vs. [FVWM](http://www.fvwm.org/) (which I've been using a few years during the last decade). In the end, creating and justifying my own code style, my own environment always was too much work with doubtful gains.

Sometimes it **is** worth it to deviate from the trodden path. **Coding style** isn’t one of those areas.
