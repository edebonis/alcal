from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path

from alcal import views

urlpatterns = [  
    path('', views.home, name='home'),  
    path('grappelli/', include('grappelli.urls')),  
    path('admin/', admin.site.urls),  
    path('chaining/', include('smart_selects.urls')),  
    path('consultas/', views.consultas, name='consultas'),  
    path('ingresar/', views.ingresar, name='ingresar'),  
    path('asistencia/', views.asistencia, name='asistencia'),  
    path('calificaciones/', views.calificaciones, name='calificaciones'),  
    path('observaciones/', views.observaciones, name='observaciones'),  
    path('ing_asistencia/', views.ing_asistencia, name='ing_asistencia'),  
    path('ing_asistencia_cur/', views.ing_asistencia_cur, name='ing_asistencia_cur'),  
    path('cons_asistencia/', views.cons_asistencia, name='cons_asistencia'),  
    path('cons_asistencia_cur/', views.cons_asistencia_cur, name='cons_asistencia_cur'),  
    path('ing_calificaciones/', views.ing_calificaciones, name='ing_calificaciones'),  
    path('ing_calificaciones_cur/', views.ing_calificaciones_cur, name='ing_calificaciones_cur'),  
    path('cons_calificaciones/', views.cons_calificaciones, name='cons_calificaciones'),  
    path('cons_calificaciones_cur/', views.cons_calificaciones_cur, name='cons_calificaciones_cur'),  
    path('ing_observaciones/', views.ing_observaciones, name='ing_observaciones'),  
    path('ing_observaciones_cur/', views.ing_observaciones_cur, name='ing_observaciones_cur'),  
    path('cons_observaciones/', views.cons_observaciones, name='cons_observaciones'),  
    path('cons_observaciones_cur/', views.cons_observaciones_cur, name='cons_observaciones_cur'),  
]