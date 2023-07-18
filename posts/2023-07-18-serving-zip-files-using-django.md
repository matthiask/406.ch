Title: Serving ZIP files using Django
Date: 2023-07-18
Categories: Django, Programming

# Serving ZIP files using Django

I have generated ZIP files on the fly and served them using Django for a time.
Serving ZIP files worked well until it didn't and browsing StackOverflow etc.
didn't produce clear answers either. The development server worked fine, but
gunicorn/nginx didn't.

In the end, I had to change `content_type="application/zip"` to
`content_type="application/x-zip-compressed"`. I still don't know what changed
and I have only theories why that's necessary, but maybe it helps someone else.
Sometimes it's better to be dumber about it.
