from django import forms
from .models import ContactMessage

from .models import ContactRequest, Service

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-white bg-dark-800 custom-border', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control text-white bg-dark-800 custom-border', 'required': True, 'pattern': r'\+?[0-9\s\-]{7,15}', 'placeholder': '+48 XXX XXX XXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-white bg-dark-800 custom-border', 'required': True}),
            'service': forms.Select(attrs={'class': 'form-select text-white bg-dark-800 custom-border', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-control text-white bg-dark-800 custom-border', 'rows': 4, 'style': 'resize: none;'}),
        }
