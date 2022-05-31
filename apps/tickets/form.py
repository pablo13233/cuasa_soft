from apps.tickets.models import Ticket
from apps.usuarios.models import User
from django import forms

class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assignee', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].queryset = User.objects.filter(is_active=True)
        self.fields['status'].queryset = Ticket.objects.filter(status='Abierto')
