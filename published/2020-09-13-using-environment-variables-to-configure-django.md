Title: Using environment variables to configure Django
Slug: using-environment-variables-to-configure-django
Date: 2020-09-13
Categories: Django, Programming

# Using environment variables to configure Django

My preferred way to read values from the environment uses the [ast](https://docs.python.org/3/library/ast.html) module to evaluate Python literals. This means that values such as `["*"]`, `None` and `True` aren't returned as strings but actually have the expected type already.

A basic implementation using `ast.literal_eval()` follows:

    import ast
    import os

    def env(key):
    	value = os.environ[key]
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value

Some deployment environments may not make it easy to add environment variables. I like placing a `.env` file into the project root containing additional key-value combinations. Here's a way to add those values to the environment:

    def read_speckenv():
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = [v.strip("'\" \t") for v in line.split("=", 1)]
                os.environ.setdefault(key, value)

Those two functions along with a few additional bells and whistles are available as **[`speckenv`](https://pypi.org/project/speckenv/)** from PyPI. The packaged version also supports defaults, warning messages, coercion and using another mapping instead of `os.environ`. [The implementation follows the basics outlined above.](https://github.com/matthiask/speckenv/blob/master/speckenv.py)

Of course it may be useful to bundle the conversion of [DSNs](https://en.wikipedia.org/wiki/Data_source_name) to the configuration format Django expects, however I mostly use individual libraries such as [dj-database-url](https://pypi.org/project/dj-database-url/) and [dj-email-url](https://pypi.org/project/dj-email-url/) for this.
