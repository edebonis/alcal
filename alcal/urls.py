from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'alcal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', lambda x: HttpResponseRedirect('/admin')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
)
