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
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya existe')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo electrónico ya existe')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
