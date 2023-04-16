Title: Offline messages for Django
Slug: offline-messages-for-django
Date: 2018-04-18
Categories: Django, Programming

# Offline messages for Django

`django.contrib.messages` is awesome. Its API surface is small, it's fast and it does what it does really well.

However, it sometimes happens that you would want to send messages to users outside the request-response cycle, for example from a background process or even from a `post_save` signal handler.

Adding a full-blown notifications-and-messages-system is of course possible. Sending a one-off message to the user would be sufficient though, but there is no way to do this with Django's messages framework.

There are a few packages around solving this particular problem. Almost all of them solve this by saving undelivered messages in the database. My solution, [django-user-messages](https://django-user-messages.readthedocs.io/) follows the same approach, but contrary to many others it does not reimplement the message storage nor replace any other functionality of `django.contrib.messages`. It only adds a few additional utilities for adding messages (e.g. `user_messages.api.info(...)` instead of `messages.info(...)`) and a context processor which concatenates Django's messages with those provided by django-user-messages.

Instead of passing the request to `messages.info(...)` you would pass a user instance, or even only a user ID to `api.info(...)`.

Easy enough, and works well. Despite the 0.5 version number the package has been stable and essentially unchanged since July 2017 (except for the addition of Python 2 support). So I wont say to get it while it's hot, because it's not -- instead, it is boring, stable and reliable, the way I like my [low maintenance software](https://406.ch/writing/low-maintenance-software/).

- [django-user-messages on Github](https://github.com/matthiask/django-user-messages/)
- [Documentation on readthedocs.io](https://django-user-messages.readthedocs.io/)
