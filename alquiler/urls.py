from django.urls import path
from alquiler import views

urlpatterns = [
    path('',views.index),
]