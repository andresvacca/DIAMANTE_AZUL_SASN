from django import forms
from .models import Factura, DetalleFactura


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['id_cliente', 'id_usuario', 'monto_pagado', 'metodo_pago']
        labels = {
            'id_cliente':   'Cliente',
            'id_usuario':   'Vendedor',
            'monto_pagado': 'Monto Pagado ($)',
            'metodo_pago':  'Método de Pago',
        }
        widgets = {
            'id_cliente':   forms.Select(attrs={'class': 'auth-input'}),
            'id_usuario':   forms.Select(attrs={'class': 'auth-input'}),
            'monto_pagado': forms.NumberInput(attrs={
                'class': 'auth-input', 'step': '0.01', 'min': '0', 'placeholder': '0.00'
            }),
            'metodo_pago':  forms.Select(attrs={'class': 'auth-input'}),
        }


class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['id_articulo', 'precio_venta']
        labels = {
            'id_articulo':  'Artículo',
            'precio_venta': 'Precio de Venta ($)',
        }
        widgets = {
            'id_articulo':  forms.Select(attrs={'class': 'auth-input'}),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'auth-input', 'step': '0.01', 'min': '0', 'placeholder': '0.00'
            }),
        }


class FiltroFactura(forms.Form):
    q = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de cliente o # Factura...'})
    )