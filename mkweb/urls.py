from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views import generic


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mkweb.views.home', name='home'),
    # url(r'^mkweb/', include('mkweb.foo.urls')),

    url(r'^$', generic.TemplateView.as_view(
        template_name='home.html',
        )),
    url(r'^404/$', generic.TemplateView.as_view(
        template_name='404.html',
        )),

    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
