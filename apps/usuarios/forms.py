from .models import User
from django import forms


class RegistroForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña'}
            )
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirme la Contraseña'}
            )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'nombres',
            'apellidos',
            'email',
            'staff',
            'superuser',
            'activo',
        )
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.errors('password2', 'Las contraseñas no coinciden')
