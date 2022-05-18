from .models import User
from django import forms

class RegistroForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = (
            'username',
            'nombres',
            'apellidos',
            'email'
        )