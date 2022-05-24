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
    nombres = forms.CharField(
        label='Nombres',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nombres', 'class': 'form-control rounded', 'type':'text'}
        ),
    )
    apellidos = forms.CharField(
        label='Apellidos',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Apellidos', 'class': 'form-control rounded', 'type':'text'}
        ),
    )
    is_staff = forms.BooleanField(
        label='Es Administrador',
        required=False,
        widget=forms.CheckboxInput(
            attrs={'placeholder': 'Es Administrador', 'class': 'form-check-input', 'type':'checkbox', 'unchecked':'unchecked', 'role':'switch', 'id':'flexSwitchCheckDefault'}
        ),
    )
    is_active = forms.BooleanField(
        label='Está Activo',
        required=False,
        widget=forms.CheckboxInput(
            attrs={'placeholder': 'Está Activo', 'class': 'form-check-input', 'type':'checkbox', 'checked':'checked', 'role':'switch', 'id':'flexSwitchCheckChecked'}
        ),
    )
    class Meta:
        model = User
        fields = (
            'username',
            'nombres',
            'apellidos',
            'email',
            'is_staff',
            'is_active',
        )
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no coinciden')
