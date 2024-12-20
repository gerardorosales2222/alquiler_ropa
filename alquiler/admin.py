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
    list_display = ('nro_articulo','categoria','color','talle','descripcion')
    search_fields = ('categoria__descripcion','talle','color__nombre','descripcion') 
    list_filter = ('categoria','color','descripcion') 

class PrendaInline(admin.TabularInline):
    model = Alquiler.prenda.through
    extra = 1


@admin.register(Pantalon)
class PantalonAdmin(admin.ModelAdmin):
    list_display = ('color_pantalon','talle_pantalon', 'traje')
    search_fields = ('color_pantalon','talle_pantalon','traje')
    list_filter = ('color_pantalon','talle_pantalon')

@admin.register(Saco)
class SacoAdmin(admin.ModelAdmin):
    list_display = ('color_saco','talle_saco','traje')
    search_fields = ('color_saco','talle_saco','traje')
    list_filter = ('color_saco','talle_saco')

@admin.register(Traje)
class TrajeAdmin(admin.ModelAdmin):
    list_display = ('nro_articulo', 'mostrar_pantalon', 'mostrar_saco')
    search_fields = ('nro_articulo',)
    list_filter = ('nro_articulo',)

class AlquilerAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'mostrar_prendas', 'mostrar_trajes','mostrar_pantalones','mostrar_sacos','fecha_alquiler', 'precio_alquiler', 'estado', 'seña', 'usuario')
    exclude = ('usuario',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Solo asignar usuario si es un nuevo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
        
admin.site.register(Alquiler, AlquilerAdmin)