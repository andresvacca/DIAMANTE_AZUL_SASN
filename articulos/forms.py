from django import forms
from .models import Articulos

class ArticuloForm(forms.ModelForm):
    """
    Form para registrar y editar artículos.
    Los campos con choices (categoria, estado, quilataje) se renderizan
    automáticamente como <select> con las opciones del modelo.
    """

    class Meta:
        model = Articulos
        fields = ['nombre', 'descripcion', 'numero_serie', 'categoria', 'estado', 'precio_sugerido_venta', 'quilataje']
        labels = {
            'nombre':                'Nombre del Artículo',
            'descripcion':           'Descripción',
            'numero_serie':          'Número de Serie',
            'categoria':             'Categoría',
            'estado':                'Estado',
            'precio_sugerido_venta': 'Precio Sugerido de Venta ($)',
            'quilataje':             'Quilataje',
        }
        widgets = {
            'nombre':                forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion':           forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'numero_serie':          forms.TextInput(attrs={'class': 'form-control'}),
            'categoria':             forms.Select(attrs={'class': 'form-select'}),   # Select porque tiene choices
            'estado':                forms.Select(attrs={'class': 'form-select'}),   # Select porque tiene choices
            'precio_sugerido_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quilataje':             forms.Select(attrs={'class': 'form-select'}),   # Select porque tiene choices
        }


# Artículos
class FiltroArticuloForm(forms.Form):
    q = forms.CharField(
        required=False, label='Buscar',
        widget=forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Buscar por nombre...'})
    )
    estado = forms.ChoiceField(
        required=False, label='Estado',
        choices=[('', 'Todos')] + Articulos.ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'auth-input'})
    )
    categoria = forms.ChoiceField(
        required=False, label='Categoría',
        choices=[('', 'Todas')] + Articulos.CATEGORIA_CHOICES,
        widget=forms.Select(attrs={'class': 'auth-input'})
    )