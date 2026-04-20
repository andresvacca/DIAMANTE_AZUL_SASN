from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol
from clientes.models import Cliente


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'auth-input'}),
        required=False,
        help_text='Dejar en blanco para no cambiar la contraseña.'
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'id_rol']
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo Electrónico',
            'id_rol': 'Rol',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'auth-input'}),
            'email': forms.EmailInput(attrs={'class': 'auth-input'}),
            'id_rol': forms.Select(attrs={'class': 'auth-input'}),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            usuario.password_hash = make_password(password)
        if commit:
            usuario.save()
        return usuario


class RegistroForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre completo',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Tu nombre completo'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'auth-input', 'placeholder': 'correo@ejemplo.com'})
    )
    documento_id = forms.CharField(
        label='Número de documento',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Cédula o documento'})
    )
    telefono = forms.CharField(
        label='Teléfono',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Opcional'})
    )
    direccion = forms.CharField(
        label='Dirección',
        required=False,
        widget=forms.TextInput(attrs={'class': 'auth-input', 'placeholder': 'Opcional'})
    )
    departamento_expedicion = forms.CharField(
        label='Departamento de Expedición',
        max_length=100,
        required=False,
        widget=forms.HiddenInput()
    )
    lugar_expedicion = forms.CharField(
        label='Municipio de Expedición',
        max_length=100,
        required=False,
        widget=forms.HiddenInput()
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'auth-input', 'placeholder': 'Mínimo 6 caracteres'}),
        min_length=6
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'auth-input', 'placeholder': 'Repite la contraseña'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def clean_documento_id(self):
        documento_id = self.cleaned_data.get('documento_id')
        if Cliente.objects.filter(documento_id=documento_id).exists():
            raise forms.ValidationError('Este documento ya está registrado.')
        return documento_id

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned

    def save(self):
        try:
            rol_cliente = Rol.objects.get(pk=Rol.ROL_CLIENTE)
        except Rol.DoesNotExist:
            rol_cliente, _ = Rol.objects.get_or_create(
                pk=Rol.ROL_CLIENTE,
                defaults={'nombre': 'Cliente'}
            )
        usuario = Usuario.objects.create(
            nombre=self.cleaned_data['nombre'],
            email=self.cleaned_data['email'],
            password_hash=make_password(self.cleaned_data['password']),
            id_rol=rol_cliente,
        )
        Cliente.objects.create(
            nombre=self.cleaned_data['nombre'],
            documento_id=self.cleaned_data['documento_id'],
            telefono=self.cleaned_data.get('telefono', ''),
            direccion=self.cleaned_data.get('direccion', ''),
            departamento_expedicion=self.cleaned_data.get('departamento_expedicion', ''),
            lugar_expedicion=self.cleaned_data.get('lugar_expedicion', ''),
            id_usuario=usuario,
        )
        return usuario


class FiltroUsuarios(forms.Form):
    q = forms.CharField(required=False, label='Buscar',
                        widget=forms.TextInput(attrs={'placeholder': 'Nombre o Email... '}))

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'auth-input', 'placeholder': 'correo@ejemplo.com'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'auth-input', 'placeholder': 'Tu contraseña'})
    )