from django.db import models
from django import forms
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.contrib import admin


class Localidad(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    provincia = models.CharField(max_length=20, null=False, verbose_name='Provincia')
    def __str__(self):
        return f'{self.nombre}'
    class Meta:
        db_table = 'localidad'
        verbose_name = 'localidad'
        verbose_name_plural = 'localidades'


class Cliente(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, null=False, verbose_name='Apellido')
    telefono = models.CharField(max_length=12, blank=True, verbose_name='Teléfono',)
    direccion = models.CharField(max_length=50, blank=True, verbose_name='Dirección',)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE, default=1, related_name='Localidad')
    dni = models.CharField(max_length=8, unique=True, verbose_name='DNI',null=True, blank=True)
    GENERO_CHOICES = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otro'),
    ]
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='F')
    observacion = models.CharField(max_length=400, blank=True, verbose_name='Observación')

    def __str__(self):
        return f'{self.apellido}, {self.nombre}'

    class Meta:
        db_table = 'cliente'
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

class Color(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'color'
        verbose_name = 'color'
        verbose_name_plural = 'colores'

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'categoria'
        verbose_name = 'categiria'
        verbose_name_plural = 'categorias'

class Prenda(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE, default=1)
    descripcion = models.TextField(max_length=60, null=True, blank=True)
    busto = models.IntegerField(null=True, blank=True)
    cintura = models.IntegerField(null=True, blank=True)
    cadera = models.IntegerField(null=True, blank=True)
    largo = models.IntegerField(null=True, blank=True, verbose_name='Largo(cm)',)
    talle = models.CharField(max_length=20, null=True, blank=True)
    relacionadas = models.ManyToManyField('self', blank=True, verbose_name='Relacionadas',)

    def __str__(self):
        return f'nro_artículo: {self.id}, {self.categoria}, {self.color}, {self.talle}'

    def nro_articulo(self):
        return self.id

    nro_articulo.short_description = 'Número de Artículo'

    class Meta:
        db_table = 'prenda'
        verbose_name = 'prenda'
        verbose_name_plural = 'prendas'

class Pantalon(models.Model):
    color_pantalon = models.ForeignKey('Color', on_delete=models.CASCADE, default=1)
    talle_pantalon = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.id},{self.color_pantalon}, {self.talle_pantalon}'    
    
    class Meta:
        db_table = 'pantalon'
        verbose_name = 'pantalon'
        verbose_name_plural = 'pantalones'


class Saco(models.Model):
    color_saco = models.ForeignKey('Color', on_delete=models.CASCADE, default=1)
    talle_saco = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.id},{self.color_saco}, {self.talle_saco}'

    class Meta:
        db_table = 'saco'
        verbose_name = 'saco'
        verbose_name_plural = 'sacos'
    
class Traje(models.Model):
    nro_articulo = models.CharField(max_length=20, unique=True)
    pantalon = models.OneToOneField(Pantalon, on_delete=models.CASCADE)
    saco = models.OneToOneField(Saco, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'traje'
        verbose_name = 'traje'
        verbose_name_plural = 'trajes'

class Alquiler(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    prenda = models.ManyToManyField(Prenda)
    traje = models.ManyToManyField(Traje)
    fecha_alquiler = models.DateField()
    precio_alquiler = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('reservado', 'Reservado'),
        ('alquilado', 'Alquilado'),
        ('limpieza', 'Limpieza'),
    ], default='alquilado')
    seña = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def mostrar_prendas(self):
        return ", ".join([p.descripcion for p in self.prenda.all()])
    
    mostrar_prendas.short_description = 'Prendas'

    def __str__(self):
        return f'{self.prenda}, {self.cliente.nombre}, {self.cliente.apellido}, {self.fecha_devolucion}'

    class Meta:
        db_table = 'alquiler'
        verbose_name = 'alquiler'
        verbose_name_plural = 'alquileres'