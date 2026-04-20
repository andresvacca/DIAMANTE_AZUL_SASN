from django import forms
from .models import Contrato


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            'id_cuota',
            'fecha_contrato', 'tipo_contrato', 'estado_contrato'
        ]
        labels = {
            'id_cliente':      'Cliente',
            'id_articulo':     'Artículo',
            'id_empeno':       'Empeño',
            'id_cuota':        'Cuota (opcional)',
            'id_pago':         'Pago (opcional)',
            'id_factura':      'Factura (opcional)',
            'fecha_contrato':  'Fecha del Contrato',
            'tipo_contrato':   'Tipo de Contrato',
            'estado_contrato': 'Estado del Contrato',
        }
        widgets = {
            'id_cliente':      forms.Select(attrs={'class': 'auth-input'}),
            'id_articulo':     forms.Select(attrs={'class': 'auth-input'}),
            'id_empeno':       forms.Select(attrs={'class': 'auth-input', 'id': 'id_empeno', 'onchange': 'cargarDatosEmpeno()'}),
            'id_cuota':        forms.Select(attrs={'class': 'auth-input'}),
            'id_pago':         forms.Select(attrs={'class': 'auth-input'}),
            'id_factura':      forms.Select(attrs={'class': 'auth-input'}),
            'fecha_contrato':  forms.DateInput(attrs={'class': 'auth-input', 'type': 'date'}),
            'tipo_contrato':   forms.Select(attrs={'class': 'auth-input'}),
            'estado_contrato': forms.Select(attrs={'class': 'auth-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_cuota'].required = False