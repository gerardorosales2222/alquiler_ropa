from django.urls import path
from alquiler import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login/',views.colores, name='login'),
]