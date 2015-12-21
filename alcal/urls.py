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
    url(r'^ingresar', 'alcal.views.ingresar', name='ingresar'),
    url(r'^asistencia/', 'alcal.views.asistencia', name='asistencia'),
    url(r'^calificaciones/', 'alcal.views.calificaciones', name='calificaciones'),
    url(r'^observaciones/', 'alcal.views.observaciones', name='observaciones'),
    url(r'^ing_asistencia/', 'alcal.views.ing_asistencia', name='ing_asistencia'),
    url(r'^ing_asistencia_cur/', 'alcal.views.ing_asistencia_cur', name='ing_asistencia_cur'),
    url(r'^cons_asistencia/', 'alcal.views.cons_asistencia', name='cons_asistencia'),
    url(r'^cons_asistencia_cur/', 'alcal.views.cons_asistencia_cur', name='cons_asistencia_cur'),
    url(r'^ing_calificaciones/', 'alcal.views.ing_calificaciones', name='ing_calificaciones'),
    url(r'^ing_calificaciones_cur/', 'alcal.views.ing_calificaciones_cur', name='ing_calificaciones_cur'),
    url(r'^cons_calificaciones/', 'alcal.views.cons_calificaciones', name='cons_calificaciones'),
    url(r'^cons_calificaciones_cur/', 'alcal.views.cons_calificaciones_cur', name='cons_calificaciones_cur'),
    url(r'^ing_observaciones/', 'alcal.views.ing_observaciones', name='ing_observaciones'),
    url(r'^ing_observaciones_cur/', 'alcal.views.ing_observaciones_cur', name='ing_observaciones_cur'),
    url(r'^cons_observaciones/', 'alcal.views.cons_observaciones', name='cons_observaciones'),
    url(r'^cons_observaciones_cur/', 'alcal.views.cons_observaciones_cur', name='cons_observaciones_cur'),
)
