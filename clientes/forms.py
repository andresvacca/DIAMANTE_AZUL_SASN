from django import forms
from django.contrib.auth.hashers import make_password
from .models import Cliente
from usuarios.models import Usuario, Rol


class ClienteForm(forms.ModelForm):
    email = forms.EmailField(
        label='Correo electrónico',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'auth-input', 'placeholder': 'correo@ejemplo.com'})
    )
    password = forms.CharField(
        label='Contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'auth-input', 'placeholder': 'Dejar vacío si no tendrá acceso'}),
        help_text='Si se ingresa, se creará un usuario con acceso al sistema.'
    )

    class Meta:
        model = Cliente
        fields = ['documento_id', 'nombre', 'telefono', 'direccion', 'departamento_expedicion', 'lugar_expedicion']
        labels = {
            'documento_id':           'Número de Documento',
            'nombre':                 'Nombre Completo',
            'telefono':               'Teléfono',
            'direccion':              'Dirección',
            'departamento_expedicion':'Departamento de Expedición',
            'lugar_expedicion':       'Municipio de Expedición',
        }
        widgets = {
            'documento_id':            forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Ej: 1234567890'}),
            'nombre':                  forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Nombre completo'}),
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