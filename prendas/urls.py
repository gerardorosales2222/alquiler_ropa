from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('alquiler.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
