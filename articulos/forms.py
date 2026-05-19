from django import forms
from .models import Articulos
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

class ArticuloForm(forms.ModelForm):
    # LOS CAMPOS VAN AQUÍ (AFUERA DE META)
    nombre = forms.CharField(
        label="Nombre del artículo",
        validators=[
            MinLengthValidator(5, message="El nombre debe tener al menos 5 caracteres"),
            MaxLengthValidator(50, message="El nombre debe tener al menos 50 caracteres"),
        ],
        widget=forms.TextInput(attrs={'class': 'auth-input'})
    )
    
    numero_serie = forms.CharField(
        label="Número de Serie",
        required=True,
        validators=[
            MinLengthValidator(5, message="La serie debe tener al menos 5 caracteres."),
        ],
        widget=forms.TextInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Ej: ABC12345'
        })
    )

    class Meta:
        model = Articulos
        fields = ['nombre', 'descripcion', 'numero_serie', 'categoria', 'estado', 'precio_sugerido_venta', 'quilataje']
        # Los labels y widgets de Meta solo se aplican a los campos que NO definiste arriba
        labels = {
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'estado': 'Estado',
            'precio_sugerido_venta': 'Precio Sugerido de Venta ($)',
            'quilataje': 'Quilataje',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'precio_sugerido_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quilataje': forms.Select(attrs={'class': 'form-select'}),
        }


# Artículos
class FiltroArticuloForm(forms.Form):
    buscar_id = forms.IntegerField(
        required=False, label='Buscar',
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'placeholder': 'Buscar Id.'})
    )
    
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