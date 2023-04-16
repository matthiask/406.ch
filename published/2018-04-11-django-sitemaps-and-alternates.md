Title: Django, Sitemaps and alternates
Slug: django-sitemaps-and-alternates
Date: 2018-04-11
Categories: Django, Programming

# Django, Sitemaps and alternates

Django's own [sitemaps](https://docs.djangoproject.com/en/2.0/ref/contrib/sitemaps/) module is great for quickly generating [sitemaps](https://support.google.com/webmasters/answer/183668?hl=en), but it unfortunately does not support more than the bare minimum of attributes. Also, it uses the template engine to create XML and this makes me sad.

[We](https://feinheit.ch/) had to add a `sitemap.xml` file to a customers' website. The site supports several languages and runs on several domains, so we had to carefully specify [alternate language pages](https://support.google.com/webmasters/answer/2620865?hl=en) and [canonical URLs](https://support.google.com/webmasters/answer/139066?hl=en) so that the website would not be punished for duplicate content.

Therefore, a year ago I set out to build a sitemaps app for Django which supports Django's sitemaps, but also allows adding entries with additional attributes. The result of this work was [django-sitemaps](https://github.com/matthiask/django-sitemaps).

    from django_sitemaps import Sitemap

    def sitemap(request):
    	sitemap = Sitemap(build_absolute_uri=request.build_absolute_uri)
        sitemap.add_django_sitemap(SomeSitemap, request=request)
        sitemap.add(
      	   url,
           changefreq='weekly',
           priority=0.5,
           lastmod=datetime.now(),
           alternates={
               'en': '...',
               'en-ch': '...',
               'en-gb': '...',
               'de': '...',
               ...
           },
       )
       return sitemap.response(pretty_print=True)

Today, I also added support for generating the most simple `robots.txt` files possible: All user agents, and only `Sitemap: <absolute url>` entries. The recommended usage is now (still using `url()` instead of `path()` because I'm old and rusty):

    from django_sitemaps import robots_txt
    from app.views import sitemap

    urlpatterns = [
        url(r'^sitemap\.xml$', sitemap),
        url(r'^robots\.txt$', robots_txt(timeout=86400)),
        ...
    ]
