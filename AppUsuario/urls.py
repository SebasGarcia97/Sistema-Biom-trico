from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.inicio, name="Inicio" ),   
    path('registro/',views.registro, name="Registro"),
    path('salir/', views.salir, name="Salir"), 
    path('sistema/', views.sistema, name="Sistema" ), 
    path('horario/', views.horario, name="Horario" ),

    path('info_admin/', views.info_admin, name="info_admin" ),
     path('elim_admin/<int:id>/',views.elim_admin, name='eliminar_admin' ),
]
