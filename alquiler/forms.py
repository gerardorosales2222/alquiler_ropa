from django import forms
from .models import Alquiler, Prenda, Traje, Pantalon, Saco

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
        fields = ['cliente', 'prenda', 'saco', 'pantalon', 'traje']