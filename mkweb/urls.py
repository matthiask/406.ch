from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views import generic


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', generic.RedirectView.as_view(
        url='/blog/',
        )),
    url(r'^home/$', generic.TemplateView.as_view(
        template_name='home.html',
        )),
    url(r'^404/$', generic.TemplateView.as_view(
        template_name='404.html',
        )),

    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
