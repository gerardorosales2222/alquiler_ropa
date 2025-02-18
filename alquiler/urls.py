from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login/',views.login, name='login'),
    path('logout/', views.exit, name='salir'),
    path('clientes/',views.clientes, name='clientes'),
    path('trajes/',views.trajes, name='trajes'),
    path('asociar_prenda/', views.asociar_prenda, name='asociar_prenda'),
    path('nuevo_traje/', views.nuevo_traje, name='nuevo_traje'),
    path('trajes/listar_pantalones/<int:traje_id>/', views.listar_pantalones, name='listar_pantalones'),
    path('prendas/', views.prendas, name='prendas'),
    
    

    path('nueva_prenda/', views.add_prenda, name='nueva_prenda'),

]

## alquileres
urlpatterns += [

    path('registrar_alquiler/', views.registrar_alquiler, name='registrar_alquiler'),
    path('registrar_devolucion/<int:alquiler_id>/', views.registrar_devolucion, name='registrar_devolucion'),
    path('lista_alquileres_activos_devolucion/', views.lista_alquileres_activos_para_devolucion, name='lista_alquileres_activos_devolucion'),
    path('lista_alquileres/', views.lista_alquileres, name='lista_alquileres'),
    path('cancelar_reserva/<int:alquiler_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('lista_trajes_alquilados_reservados/', views.lista_trajes_alquilados_reservados, name='lista_trajes_alquilados_reservados'),


]
