from django import forms
from django.contrib.auth.hashers import make_password
from .models import Cliente
from usuarios.models import Usuario, Rol
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

class ClienteForm(forms.ModelForm): 
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'auth-input', 'placeholder': 'correo@ejemplo.com'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'auth-input', 'placeholder': 'Dejar vacío si no tendrá acceso'}),
        help_text='Si se ingresa, se creará un usuario con acceso al sistema.',
        required=False # 👈 IMPORTANTE: Falso por defecto, lo controlamos en __init__
    )
    
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Ingrese el nombre completo'}),
        label='Nombre Completo',
        validators=[
            RegexValidator(regex=r'^[^0-9]+$', message='El nombre solo debe tener letras'),
            MinLengthValidator(3, message="Mínimo 3 Caracteres"),
            MaxLengthValidator(100, message="Máximo 100 Caracteres"),
        ],
    )
    
    documento_id = forms.CharField(
        label='Número de documento',
        validators=[
            RegexValidator(regex=r'^\d+$', message="El Documento solo debe tener números"),
            MinLengthValidator(4, message="El documento debe tener mínimo 4 dígitos."),
            MaxLengthValidator(15, message="El documento no puede exceder los 15 dígitos."),
        ],
        widget=forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Cédula o documento'})
    )
    
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        
        # 🎨 1. Estilos automáticos
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'auth-input')

        # 🔄 2. Control total de estados
        if self.instance and self.instance.pk:
            self.fields['nombre'].widget.attrs['readonly'] = True
            self.fields['nombre'].widget.attrs['class'] = 'auth-input bg-light'
            self.fields['documento_id'].widget.attrs['readonly'] = True
            self.fields['documento_id'].widget.attrs['class'] = 'auth-input bg-light'
            
            # Quitar required de contraseña en HTML
            self.fields['password'].required = False
            self.fields['password'].widget.attrs.pop('required', None)
            self.fields['password'].label = "Nueva Contraseña (Vacío para mantener)"
        else:
            self.fields['password'].required = True

    class Meta:
        model = Cliente
        # 🚨 SOLUCIÓN: Agregados nombre y documento_id que faltaban aquí
        fields = ['documento_id', 'nombre', 'telefono', 'direccion', 'departamento_expedicion', 'lugar_expedicion']
        labels = {
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'departamento_expedicion': 'Departamento de Expedición',
            'lugar_expedicion': 'Municipio de Expedición',
        }
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Ej: 3001234567'}),
            'direccion': forms.Textarea(attrs={'class': 'auth-input', 'rows': 3}),
            'departamento_expedicion': forms.HiddenInput(),
            'lugar_expedicion': forms.HiddenInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 🚨 SOLUCIÓN CORREO REPETIDO: Si estamos editando, ignoramos al dueño actual
        if self.instance and self.instance.pk and self.instance.id_usuario:
            if Usuario.objects.filter(email=email).exclude(pk=self.instance.id_usuario.pk).exists():
                raise forms.ValidationError('Este correo ya está registrado por otro usuario.')
        else:
            if email and Usuario.objects.filter(email=email).exists():
                raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def save(self, commit=True):
        cliente = super().save(commit=False)
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        # 🚨 SOLUCIÓN INTELIGENTE: Distinguir entre Crear y Editar Usuario
        if self.instance and self.instance.pk and cliente.id_usuario:
            # Modo Editar
            usuario = cliente.id_usuario
            usuario.nombre = self.cleaned_data['nombre']
            usuario.email = email
            if password:
                usuario.password_hash = make_password(password)
            usuario.save()
        else:
            # Modo Crear
            if email and password:
                rol_cliente = Rol.objects.get(pk=Rol.ROL_CLIENTE)
                usuario = Usuario.objects.create(
                    nombre=self.cleaned_data['nombre'],
                    email=email,
                    password_hash=make_password(password),
                    id_rol=rol_cliente,
                )
                cliente.id_usuario = usuario

        if commit:
            cliente.save()
        return cliente

class FiltroCliente(forms.Form):
    buscar_id = forms.IntegerField(
        required=False, label='Buscar',
        widget=forms.NumberInput(attrs={'class': 'auth-input', 'placeholder': 'Buscar Id.'})
    )
    q = forms.CharField(
        required=False, 
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'auth-input', # O la clase CSS que uses para tus buscadores
            'placeholder': 'Buscar por nombre, documento, teléfono...'
        })
    )