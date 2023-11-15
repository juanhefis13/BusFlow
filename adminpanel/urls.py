from django.contrib import admin
from django.urls import path, include
from aplicaciones.panel.views import Conductor, AgregarConductor,ModificarConductor,EliminarConductor
from aplicaciones.panel import views

from django.conf import settings
 
urlpatterns = [
    path('', views.bus_app_page, name='main'),
    path('admin/', admin.site.urls),
    path('Conductor/', Conductor.as_view(), name="index"),
    path('agregar/', AgregarConductor.as_view(), name='agregar_conductor'),
    path('modificar/<str:conductor_id>/', views.ModificarConductor.as_view(), name='modificar_conductor'),
    path('eliminar/<str:conductor_id>/', views.EliminarConductor.as_view(), name='eliminar_conductor'),
    
]
