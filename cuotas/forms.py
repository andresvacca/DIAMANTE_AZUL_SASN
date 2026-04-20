from django import forms
from empenos.models import Cuota

class FiltroCuota(forms.Form):
    estado = forms.ChoiceField(
        required=False,
        label='ESTADO DE CUOTA', # Texto de arriba personalizado
        choices=[('', 'Todos los estados')] + Cuota.ESTADO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'input-auth',
            'style': 'margin-bottom: 0; height: 42px; background-color: var(--blanco); color: var(--azul-oscuro); border: 1px solid var(--gris-claro);'
        })
    )
    
    q = forms.CharField(
        required=False,
        label='BUSCAR POR CLIENTE', # Texto de arriba personalizado
        widget=forms.TextInput(attrs={
            'placeholder': 'Escriba el nombre...',
            'class': 'input-auth',
            'style': 'margin-bottom: 0; height: 42px; background-color: var(--blanco); color: var(--azul-oscuro); border: 1px solid var(--gris-claro);'
        })
    )