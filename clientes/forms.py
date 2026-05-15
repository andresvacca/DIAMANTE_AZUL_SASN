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
        help_text='Si se ingresa, se creará un usuario con acceso al sistema.'
    )
    
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'auth-input', 
            'placeholder': 'Ingrese el nombre completo'
        }),
        label='Nombre Completo',
        validators=[
            RegexValidator(
                regex = r'^[^0-9]+$',
                message ='El nombre solo debe tener letras'
            ),
            MinLengthValidator(3 ,message= "Minimo 3 Caracteres"),
            MaxLengthValidator(100, message= "Maximo 100 Caracteres"),
            ],
    )
    
    documento_id = forms.CharField(
        label='Número de documento',
        validators=[
          RegexValidator(
              regex=r'^\d+$',
              message= "El Documento solo debe tener numeros"
           ),
            MinLengthValidator(4, message="El teléfono debe tener minumo 4 dígitos."),
            MaxLengthValidator(15, message="El teléfono no puede exceder los 15 dígitos."),
        ],
        widget=forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Cédula o documento'})
    )

    class Meta:
        model = Cliente
        fields = ['telefono', 'direccion', 'departamento_expedicion', 'lugar_expedicion']
        labels = {
            
           # 'nombre':                 'Nombre Completo',
            'telefono':               'Teléfono',
            'direccion':              'Dirección',
            'departamento_expedicion':'Departamento de Expedición',
            'lugar_expedicion':       'Municipio de Expedición',
        }
        widgets = {
            
            #'nombre':                  forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Nombre completo'}),
            'telefono':                forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Ej: 3001234567'}),
            'direccion':               forms.Textarea(attrs={'class': 'auth-input', 'rows': 3}),
            'departamento_expedicion': forms.HiddenInput(),
            'lugar_expedicion':        forms.HiddenInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def save(self, commit=True):
        cliente = super().save(commit=False)
        email    = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

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
    q = forms.CharField(required=False, label='Buscar',
                        widget=forms.TextInput(attrs={'placeholder': 'Nombre o Documento... '}))