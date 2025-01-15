Title: Weeknotes (2025 week 03)
Categories: Django, Programming, Weeknotes

## Claude AI helped me for the first time

[django-imagefield](https://github.com/matthiask/django-imagefield) prefers
processing thumbnails, cropped images etc. directly when saving the model and
not later on demand; it's faster and also you'll know it immediately when an
image couldn't be processed for some reason instead of only later when people
actually try browsing your site.

A consequence is that if you change formats you have to remember that you have
to reprocess the images. The Django app comes with a management command
`./manage.py process_imagefields` to help with this. I have added parallel
processing based on `concurrent.futures` to it some time ago so that the
command completes faster when it is being run on a system with several cores.

A work colleague is using macOS (many are, in fact), and he always got
multiprocessing Python crashes. This is a well known issue and I remember
reading about it a few years ago. I checked the docs and saw that the
[`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html)
page doesn't mention macOS, but
[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)
does. So, I hoped that a simple rewrite of the management command using
`multiprocessing` might fix it.

Because I was in a rush and really didn't want to do it I turned to an AI
assistant for doing this boring work. To my surprise it immediately produced a
version which I could easily fix by hand to produce a working version. Of
course, the initial response was totally broken, removed code it wasn't
supposed to, and even the syntax was invalid. I didn't expect more though, but
what was surprising was that it actually felt like I had to do less work at
this time.

The assistant also helped adding a `--no-parallel` flag to the management
command. The output was even more broken than the output of the change
mentioned above, but again, I could easily fix it to achieve what I wanted.

The fact that I know the code and [git](https://git-scm.com/) well certainly
helped, the assistant would really have helped without that knowledge.

In the end, switching to `multiprocessing` didn't help, but adding the
`--no-parallel` flag allowed them to run the processing themselves by not
spawning any additional threads or processes.

The energy use and the stealing of copyrighted material done by the AI
companies is still really bad. It does feel somewhat OK to use an AI assistant
in an area where I'm proficient as well and where I probably also supplied
training material (without being asked if I wanted this) though. It's making me
slightly faster, and doesn't allow me to do things I really couldn't otherwise.

## Releases

- [FeinCMS 24.12.3](https://pypi.org/project/FeinCMS/): I have added a TinyMCE
  7 integration to FeinCMS.
- [django-imagefield 0.21.1](https://pypi.org/project/django-imagefield/): See
  above.
