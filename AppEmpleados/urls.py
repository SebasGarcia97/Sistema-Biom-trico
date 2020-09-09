from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [     
    path('reg_empleados/', views.reg_empleados, name='Empleado' ),
    path('elim_empleados/<int:id>/',views.elim_empleados, name='eliminar_empleado' ),
    path('informacion/', views.informacion, name="Informacion" ),      
    path('sistema/', views.sistema, name="Sistema" ), 
    #EDITAR EMPLEADO
    path('editar_empleado/<int:id>/',views.editarEmpleado, name = 'editar_empleado'),
    #VIDEO     
    path('video/', views.Video, name='Video'),   
    path('video_feed/', views.video_feed, name='video_feed'), 
    path('reconocer/', views.reconocer, name='reconocer'), 

]
