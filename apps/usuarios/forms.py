from .models import User
from django import forms
from django.contrib.auth.password_validation import validate_password

class RegistroForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña', 'class': 'form-control rounded', 'type':'password'}
            ),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirme la Contraseña', 'class': 'form-control rounded', 'type':'password'}
            ),
        validators=[validate_password],
    )
    username = forms.CharField(
        label='Nombre de Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nombre de Usuario', 'class': 'form-control rounded', 'type':'text'}
        ),
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        required=True,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control rounded', 'type':'email'}
        ),
    )
    first_name = forms.CharField(
        label='Nombres',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nombres', 'class': 'form-control rounded', 'type':'text'}
        ),
    )
    last_name = forms.CharField(
        label='Apellidos',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Apellidos', 'class': 'form-control rounded', 'type':'text'}
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