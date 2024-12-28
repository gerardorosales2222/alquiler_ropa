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
]