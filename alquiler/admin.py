from django.contrib import admin
from .models import *

admin.site.site_header = 'Graciela Ferrer'
admin.site.index_title = 'Panel de control'
admin.site.site_title = 'Administración de Alquileres de Prendas'

@admin.register(Localidad)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre','provincia')
    search_fields = ('id', 'nombre','provincia') 
    list_filter = ('id', 'nombre','provincia') 

@admin.register(Cliente)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('dni', 'apellido','nombre')
    search_fields = ('dni', 'apellido','nombre') 
    list_filter = ('dni', 'apellido','nombre') 

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',) 
    list_filter = ('nombre',) 

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion')
    search_fields = ('nombre',) 
    list_filter = ('nombre',) 

@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('categoria','color','descripcion')
    search_fields = ('categoria','color','descripcion') 
    list_filter = ('categoria','color','descripcion') 

@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    list_display = ('fecha_alquiler','estado')
    search_fields = ('fecha_alquiler',) 
    list_filter = ('fecha_alquiler',)