Title: The final INTERNAL_IPS fix for development hosts
Slug: the-final-internal_ips-fix-for-development-hosts
Date: 2018-04-20
Categories: Django, Programming

# The final INTERNAL_IPS fix for development hosts

Django's [INTERNAL_IPS](https://docs.djangoproject.com/en/2.0/ref/settings/#internal-ips) setting is an ongoing source of frustration and confusion (not only, but also) for users of [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar), especially when using non-local addresses. This is very useful for testing a website using mobile devices if you do not have a very fast internet connection where it does not matter whether you connect to a host through the local network or via the internet, for example using [localtunnel](https://localtunnel.github.io/www/).

For some time we had a utility function which automatically added all detected network interface IPs to `INTERNAL_IPS`. However, this does not work when using virtualization software such as Docker or Vagrant with port forwarding, because the VM's (or container's) IP isn't what you want -- you want the host IP.

Once I took a step back I saw a different, but much simpler solution. `INTERNAL_IPS` can be replaced with an object which simply answers `True` to all `__contains__`-type questions:

    if DEBUG:
        # `debug` is only True in templates if the vistor IP is in INTERNAL_IPS.
        INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()
