from django import forms
from clientes.models import Cliente
from articulos.models import Articulos

FORMA_PAGO_CHOICES = [
    ('Efectivo', 'Efectivo'),
    ('Transferencia', 'Transferencia'),
]


class CompraForm(forms.Form):
    id_cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label='Cliente que vende',
        widget=forms.Select(attrs={'class': 'auth-input'})
    )
    id_articulo = forms.ModelChoiceField(
        queryset=Articulos.objects.all(),
        label='Artículo',
        widget=forms.Select(attrs={'class': 'auth-input'})
    )
    precio_pagado = forms.DecimalField(
        max_digits=12, decimal_places=2,
        label='Precio pagado por la casa',
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'step': '0.01'})
    )
    precio_reventa = forms.DecimalField(
        max_digits=12, decimal_places=2,
        label='Precio de reventa sugerido',
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'step': '0.01'})
    )
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