from django import forms
from clientes.models import Cliente
from articulos.models import Articulos
from .models import Compra
from django.core.validators import MinValueValidator, MaxValueValidator

FORMA_PAGO_CHOICES = [
    ('Efectivo', 'Efectivo'),
    ('Transferencia', 'Transferencia'),
]


class CompraForm(forms.Form):
    # Definimos los campos que no están directamente en el modelo de Artículos
    # o que queremos personalizar con los nuevos límites de dígitos.
    
    id_cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label='Cliente que vende',
        widget=forms.Select(attrs={'class': 'auth-input'}),
        error_messages={'required': 'Debe seleccionar un cliente.'}
    )

    id_articulo = forms.ModelChoiceField(
        queryset=Articulos.objects.all(),
        label='Artículo',
        widget=forms.Select(attrs={'class': 'auth-input'}),
        error_messages={'required': 'Debe seleccionar un artículo.'}
    )

    precio_pagado = forms.DecimalField(
        max_digits=15,  # Protegemos contra el DataError de MySQL
        decimal_places=2,
        label='Precio pagado por la casa',
        validators=[MinValueValidator(0.01, message="El precio debe ser mayor a cero.")],
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'step': '0.01', 'placeholder': '0.00'})
    )

    precio_reventa = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        label='Precio de reventa sugerido',
        validators=[MinValueValidator(0.01, message="El precio de reventa debe ser mayor a cero.")],
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'step': '0.01', 'placeholder': '0.00'})
    )

    FORMA_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
    ]

    forma_pago = forms.ChoiceField(
        choices=FORMA_PAGO_CHOICES,
        label='Forma de pago',
        widget=forms.Select(attrs={'class': 'auth-input'})
    )

    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'auth-input', 'rows': 3}),
        required=False,
        label='Observaciones'
    )

    class Meta:
        # Como me dijiste que no hay modelo "Compra", usamos Articulos como base
        # o puedes usar forms.Form si no quieres ligarlo a un modelo directamente.
        model = Articulos 
        fields = ['nombre', 'categoria', 'quilataje']
        

class VentaForm(forms.Form):
    id_cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label='Cliente que compra'
    )
    valor_total = forms.DecimalField(
        max_digits=12, decimal_places=2,
        label='Valor de venta'
    )
    forma_pago = forms.ChoiceField(
        choices=FORMA_PAGO_CHOICES,
        label='Forma de pago'
    )
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Observaciones'
    )