from django.contrib import admin
from .models import *

admin.site.site_header = 'Graciela Ferrer'
admin.site.index_title = 'Panel de control'
admin.site.site_title = 'Administración de Alquileres de Prendas'

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre','provincia')
    search_fields = ('id', 'nombre','provincia') 
    list_filter = ('id', 'nombre','provincia') 

@admin.register(Cliente)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('id', 'apellido','nombre','telefono')
    search_fields = ('apellido','nombre')
    ordering = ['apellido']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',) 

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion')
    search_fields = ('nombre',)

@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('nro_articulo','categoria','color','talle','descripcion', 'disponibilidad')
    search_fields = ('categoria__descripcion','talle','color__nombre','descripcion') 
    autocomplete_fields = ['categoria', 'color'] 
    
    def disponibilidad(self, obj):
        return "Sí" if obj.disponible else "NO disponible"
    disponibilidad.short_description = 'Disponible'

class PrendaInline(admin.TabularInline):
    model = Alquiler.prenda.through
    extra = 1


@admin.register(Pantalon)
class PantalonAdmin(admin.ModelAdmin):
    list_display = ('color_pantalon','talle_pantalon', 'traje')
    search_fields = ('color_pantalon','talle_pantalon','traje')
    autocomplete_fields = ['color_pantalon'] 
    exclude = ('disponible',)

@admin.register(Saco)
class SacoAdmin(admin.ModelAdmin):
    list_display = ('color_saco','talle_saco','traje')
    search_fields = ('color_saco','talle_saco','traje')
    autocomplete_fields = ['color_saco']
    exclude = ('disponible',)

@admin.register(Traje)
class TrajeAdmin(admin.ModelAdmin):
    list_display = ('nro_articulo', 'mostrar_pantalon', 'mostrar_saco')
    search_fields = ('nro_articulo',)
    list_filter = ('nro_articulo',)


class AlquilerAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'mostrar_prendas', 'mostrar_trajes','mostrar_pantalones','mostrar_sacos','fecha_alquiler', 'precio_alquiler', 'estado', 'seña', 'usuario')
    exclude = ('usuario',)
    autocomplete_fields = ['cliente','prenda']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
        
admin.site.register(Alquiler, AlquilerAdmin)