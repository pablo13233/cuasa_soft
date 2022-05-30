from .models import User
from django import forms
from django.contrib.auth.password_validation import validate_password

class RegistroForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña', 'class': 'form-control rounded', 'type':'password', 'id':'password1'}
            ),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirme la Contraseña', 'class': 'form-control rounded', 'type':'password', 'id':'password2'}
            ),
        validators=[validate_password],
    )
    username = forms.CharField(
        label='Nombre de Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nombre de Usuario', 'class': 'form-control rounded', 'type':'text', 'id': 'nombre_usuario'}
        ),
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        required=True,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control rounded', 'type':'email', 'id': 'correo'}
        ),
    )
    first_name = forms.CharField(
        label='Nombres',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nombres', 'class': 'form-control rounded', 'type':'text', 'id': 'nombres'}
        ),
    )
    last_name = forms.CharField(
        label='Apellidos',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Apellidos', 'class': 'form-control rounded', 'type':'text', 'id': 'apellidos'}
        ),
    )
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

class UpdateUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña', 
        required=False, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña', 'class': 'form-control rounded', 'type':'password', 'id':'password1'}
            ),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña', 
        required=False, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirme la Contraseña', 'class': 'form-control rounded', 'type':'password', 'id':'password2'}
            ),
        validators=[validate_password],
    )
    username = forms.CharField(
        label='Nombre de Usuario',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control rounded', 'type':'text', 'id': 'nombre_usuario', 'disabled':'true'}
        ),
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        required=False,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control rounded', 'type':'email', 'id': 'correo'}
        ),
    )
    first_name = forms.CharField(
        label='Nombres',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nombres', 'class': 'form-control rounded', 'type':'text', 'id': 'nombres'}
        ),
    )
    last_name = forms.CharField(
        label='Apellidos',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Apellidos', 'class': 'form-control rounded', 'type':'text', 'id': 'apellidos'}
        ),
    )
    is_active = forms.BooleanField(
        label='Estado',
        required=False,
        widget=forms.CheckboxInput(
            attrs={}
        ),
    )
    is_staff = forms.BooleanField(
        label='Es Administrador',
        required=False,
        widget=forms.CheckboxInput(
            attrs={'placeholder': 'Tipo de Usuario', 'class': 'form-control rounded', 'type':'checkbox', 'id': 'tipo_usuario'}
        ),
    )
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
        )

class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña', 'class': 'form-control rounded', 'type':'password', 'id':'password1'}
            ),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirme la Contraseña', 'class': 'form-control rounded', 'type':'password', 'id':'password2'}
            ),
        validators=[validate_password],
    )