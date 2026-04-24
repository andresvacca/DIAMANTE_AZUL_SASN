from django import forms
from .models import Empeno, Pago
from contratos.models import Contrato
from articulos.models import Articulos
from decimal import Decimal

class EmpenoForm(forms.ModelForm):
    # --- CAMPOS CON VALIDACIÓN DE NEGATIVOS Y ESTILO ---
    monto_prestado = forms.DecimalField(
        min_value=0,
        label="Monto Prestado ($)",
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'step': '1000', 'min': '0'})
    )

    tasa_interes = forms.DecimalField(
        min_value=0,
        label="Tasa de Interés (%)",
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'step': '0.1', 'min': '0'})
    )

    monto_entregado = forms.DecimalField(
        min_value=0,
        label="Monto Entregado ($)",
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'step': '1000', 'min': '0'})
    )

    # --- CAMPO BLOQUEADO (SOLO LECTURA) ---
    tipo_contrato = forms.ChoiceField(
        choices=Contrato.TIPO_CHOICES,
        label="Tipo de Contrato",
        widget=forms.Select(attrs={'class': 'auth-input', 'disabled': 'disabled'})
    )

    class Meta:
        model = Empeno
        # Aquí listamos todos los campos que queremos en el formulario
        fields = [
            'id_cliente',
            'id_articulo',
            'monto_prestado',
            'tasa_interes',
            'fecha_vencimiento',
            'monto_entregado',
            'estado',
            'tipo_contrato'
        ]

        # Solo ponemos en 'widgets' los que NO definimos arriba
        widgets = {
            'id_cliente': forms.Select(attrs={'class': 'auth-input'}),
            'id_articulo': forms.Select(attrs={'class': 'auth-input'}),
            'estado': forms.Select(attrs={'class': 'auth-input'}),
            'fecha_vencimiento': forms.DateInput(
                attrs={'class': 'auth-input', 'type': 'date'},
                format='%Y-%m-%d'
            ),
        }
    # ! Funcion para Automatizar los tipos de contratos en los formularios de crear y editar empeno
    def clean(self):
        super().clean()
        articu = self.cleaned_data.get('id_articulo')
        monto = self.cleaned_data.get('monto_prestado')
        if articu and monto:
            if articu and str(articu.categoria) == "Oro":
                limite = articu.precio_sugerido_venta * Decimal('0.45')
                if monto > limite:
                    self.cleaned_data['tipo_contrato'] = "Oro Maximo"
                else:
                    self.cleaned_data['tipo_contrato'] = "Contrato sobre Oro"
            else:
                limite = articu.precio_sugerido_venta * Decimal('0.4')
                if monto > limite:
                    self.cleaned_data['tipo_contrato'] = "Plazo Maximo"
                else:
                    self.cleaned_data['tipo_contrato'] = "Normal"
                    
        return self.cleaned_data   
                
                

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Hacemos que el contrato no sea obligatorio (porque está disabled)
        self.fields['tipo_contrato'].required = True

        # 2. Tu lógica de formato de fecha para la edición
        if self.instance and self.instance.fecha_vencimiento:
            self.initial['fecha_vencimiento'] = self.instance.fecha_vencimiento.strftime('%Y-%m-%d')


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto', 'metodo_pago']
        labels = {
            'monto':       'Monto a Pagar ($)',
            'metodo_pago': 'Método de Pago',
        }
        widgets = {
            'monto':       forms.NumberInput(attrs={'class': 'auth-input', 'step': '0.01'}),
            'metodo_pago': forms.Select(attrs={'class': 'auth-input'}),
        }

class FiltroEmpeno(forms.Form):
    q = forms.CharField(required=False, label='Buscar', 
                        widget=forms.TextInput(attrs={'placehorder': 'Nombre, Valor o Estado...'}))
    
    estado = forms.ChoiceField(
        required=False, label='Estado',
        choices=[("", 'Todos')] + Empeno.ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'auth-input'})
    )


from django import forms
from .models import Contrato


class AbonoForm(forms.Form):
    # Definimos los campos con los widgets que ya diseñamos
    abonoCap = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        label="Monto a Abonar",
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'step': '1000'})
    )

    tipo_contrato = forms.ChoiceField(
        choices=Contrato.TIPO_CHOICES,
        required=True,
        label="Nuevo Tipo de Contrato",
        widget=forms.Select(attrs={'class': 'auth-input'})
    )

    # El famoso __init__ para recibir el saldo actual
    def __init__(self, *args, **kwargs):
        # Extraemos el saldo_actual antes de que Django procese el formulario
        self.saldo_actual = kwargs.pop('saldo_actual', None)
        super(AbonoForm, self).__init__(*args, **kwargs)

    # La validación para que no abonen más de lo que deben
    def clean_abonoCap(self):
        monto_abono = self.cleaned_data.get('abonoCap')

        # Si tenemos un saldo_actual y el abono es mayor, lanzamos error
        if self.saldo_actual is not None and monto_abono > self.saldo_actual:
            raise forms.ValidationError(
                f"El abono no puede ser mayor al saldo actual del empeño (${self.saldo_actual})"
            )

        return monto_abono