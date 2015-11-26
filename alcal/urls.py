from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from alcal import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'alcal.views.home', name='home'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^consultas', 'alcal.views.consultas', name='consultas'),
    url(r'^asistencia/', 'alcal.views.asistencia', name='asistencia'),
    url(r'^calificaciones/', 'alcal.views.calificaciones', name='calificaciones'),
    url(r'^observaciones/', 'alcal.views.observaciones', name='observaciones'),
    url(r'^ing_asistencia/', 'alcal.views.ing_asistencia', name='ing_asistencia'),

)
