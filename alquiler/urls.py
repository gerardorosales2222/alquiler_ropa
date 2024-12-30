from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login/',views.login, name='login'),
    path('logout/', views.exit, name='salir'),
    path('clientes/',views.clientes, name='clientes'),
    path('trajes/',views.trajes, name='trajes'),
    path('nuevo_traje/', views.nuevo_traje, name='nuevo_traje'),
    path('prendas/', views.prendas, name='prendas'),
    
    path('registrar_alquiler/', views.registrar_alquiler, name='registrar_alquiler'),
    path('guardar_alquiler/', views.guardar_alquiler, name='guardar_alquiler'),
    path('registrar_devolucion/<int:alquiler_id>/', views.registrar_devolucion, name='registrar_devolucion'),
    path('lista_alquileres/', views.lista_alquileres, name='lista_alquileres'),
]

