Title: User registration in the age of social media platforms
Slug: user-registration-age-social-media-platforms
Date: 2014-07-23
Categories: Django, Programming

**Note!** While I still think the ideas in this blog post are sound, the reference to django-email-registration is a bit outdated. I recommend <a href="https://django-authlib.readthedocs.io/" title="">django-authlib</a> these days instead.</p>

# User registration in the age of social media platforms

When we started using <a href="https://www.djangoproject.com">Django</a> at <a href="http://www.feinheit.ch/">Feinheit</a>, <a href="https://django-registration.readthedocs.org/">django-registration</a> was the app to go to when you had to implement registration and login functionality on a website.

With the advent of social media platforms things changed. Choosing a username and a password for each and every site was getting tiresome. More and more accounts are created by authenticating using Twitter, Facebook, Google, Github or whatever suits the needs of websites. Supporting email-based registration is still important of course, but can be implemented by a much smaller app.

Django supports <a href="https://docs.djangoproject.com/en/dev/topics/signing.html">cryptographic signing</a> now, which makes it much easier to provide some data to a user and check whether we get it back unmodified. We do not need to store emails and verification codes in the database if we only want to confirm email addresses for account creation. Instead, we simply craft a special link containing the email address and a cryptographic signature signed with Django’s <code>SECRET_KEY</code>.

That’s what <a href="https://github.com/matthiask/django-email-registration/">django-email-registration</a> does. It can either be used as an alternative step to social authentication, and also to confirm email addresses for already existing users.
