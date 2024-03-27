Title: The Django admin is a CMS
Date: 2024-03-27
Categories: Django, Programming
Draft: remove-this-to-publish

A recurring theme in Django land is the idea that the [Django administration
interface](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/) isn't a
CMS (Content Management System). One of the latest instances of that is the post
[Why is the Django Admin
“Ugly”?](https://www.coderedcorp.com/blog/why-is-the-django-admin-ugly/) post
and the [discussion on
Mastodon](https://hachyderm.io/@paulox@fosstodon.org/111298440425647176) around
it.

I think that this is a misguided and needlessly limits the discourse around
what the admin's current functionality is and what it already does for users.

[A web content management system](https://en.wikipedia.org/wiki/Web_content_management_system) is about website authoring for users who do not need to be web
programming experts in their own rights. [Django was created at the Lawrence
Journal-World newspaper](https://en.wikipedia.org/wiki/Django_(web_framework)).
The admin itself was created to allow quickly spinning up new websites, where
the admin interface was used by content managers to fill in the content while
programmers finalized the rest of the website. So obviously the admin interface
was a system used to manage content[^words] from the beginning.

[^words]: Sorry-not-sorry for my choice of words.

Sure, the [Django admin site
documentation](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/)
states (emphasis added):

> One of the most powerful parts of Django is the automatic admin interface. It reads metadata from your models to provide a quick, model-centric interface where trusted users can manage content on your site. The admin’s recommended use is limited to an organization’s internal management tool. **It’s not intended for building your entire front end around.**

In other words, the Django documentation also points out that the admin is
powerful and that it allows trusted users to manage content[^words].

Yes, it will be very painful if you try to do everything on top of the Django
admin site. The warnings against using the Django admin for more than it was
designed to are necessary and I totally support them. As soon as you're getting
into workflows, into complex permission scenarios (sad noises) or similar
things the admin definitely isn't for you. But, the admin nicely solves 90% of
the problems with 10% of the effort. And it's very good at that.

And sure, if you try building your own frontend on top of the Django admin
you're in for a bumpy ride, but that much should be obvious.

Many third party apps for Django actually target the Django admin interface
itself, and not one of the (excellent!) Django-based CMS such as
[Wagtail](https://wagtail.org/). This means that by building on the Django
admin instead of one of the CMS you're a part of a larger community, and
because of that you potentially benefit much more from the general Django
packages ecosystem. Also, you'll be able to upgrade to new Django versions
quicker because it's much easier to update more focussed third party apps for
new Django versions than bigger systems. It's the price they pay for the
additional functionality.

I'm not trying to say that the Django admin is a better CMS than other
Django-based CMS, or any other CMS. I'm saying it's a trade off and you should
be mindful of the downsides of choosing a larger system. And I'm saying that
the people who tell you that you shouldn't be using the Django admin interface
are wrong in the first approximation.

The fact that it's so easy to spin up an additional site and with minimal
effort and still be able to work with clean database schemas and all the great
tools Django (and Python) offers is important for those of us who are working
on many different projects with limited financial resources, because the
website often is for example just a small part of a campaign.
