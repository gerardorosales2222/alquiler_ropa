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

class PrendaInline(admin.TabularInline):
    model = Alquiler.prenda.through
    extra = 1

class AlquilerAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'mostrar_prendas', 'fecha_alquiler', 'fecha_devolucion', 'precio_alquiler', 'estado', 'seña', 'usuario')
    exclude = ('usuario',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Solo asignar usuario si es un nuevo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Alquiler, AlquilerAdmin)