from django import forms
from .models import *

class TrajeForm(forms.ModelForm):
    class Meta:
        model = Traje
        fields = ['nro_articulo']

class PantalonForm(forms.ModelForm):
    class Meta:
        model = Pantalon
        fields = ['color_pantalon', 'talle_pantalon']


class SacoForm(forms.ModelForm):
    class Meta:
        model = Saco
        fields = ['color_saco', 'talle_saco']


class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['cliente', 'prenda', 'traje', 'fecha_devolucion']


## REGISTRAR ALQUILER

class AlquilerForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label='Cliente',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    sacos = forms.ModelMultipleChoiceField(
        queryset=Prenda.objects.filter(categoria__nombre='Saco', disponible=True),  # Solo sacos disponibles
        label='Sacos',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    pantalones = forms.ModelMultipleChoiceField(
        queryset=Prenda.objects.filter(categoria__nombre='Pantalon', disponible=True),  # Solo pantalones disponibles
        label='Pantalones',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    prendas = forms.ModelMultipleChoiceField(
        queryset=Prenda.objects.exclude(categoria__nombre__in=['Saco', 'Pantalon']).filter(disponible=True),  # Otras prendas disponibles
        label='Otras Prendas',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    trajes = forms.ModelMultipleChoiceField(
        queryset=Traje.objects.filter(disponible=True),  # Solo trajes disponibles
        label='Trajes',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    fecha_alquiler = forms.DateField(
        label='Fecha de Alquiler',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    precio_alquiler = forms.DecimalField(
        label='Precio de Alquiler',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    estado = forms.ChoiceField(
        label='Estado',
        choices=[
            ('reservado', 'Reservado'),
            ('alquilado', 'Alquilado'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    seña = forms.DecimalField(
        label='Seña',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        trajes = cleaned_data.get('trajes')
        sacos = cleaned_data.get('sacos')
        pantalones = cleaned_data.get('pantalones')

        if trajes:
            for traje in trajes:
                sacos_del_traje = traje.prendas.filter(categoria__nombre='Saco')
                pantalones_del_traje = traje.prendas.filter(categoria__nombre='Pantalon')

                for saco in sacos_del_traje:
                  if not saco.disponible:
                    raise forms.ValidationError(f"El saco del traje {traje.nro_articulo} no está disponible.")

                for pantalon in pantalones_del_traje:
                  if not pantalon.disponible:
                    raise forms.ValidationError(f"El pantalón del traje {traje.nro_articulo} no está disponible.")
        
        if trajes and (sacos or pantalones):
            raise forms.ValidationError("No puede seleccionar trajes y sacos/pantalones sueltos al mismo tiempo.")

        return cleaned_data
