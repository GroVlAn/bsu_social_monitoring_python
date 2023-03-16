from django import forms
from monitoring.models_db.Organization import *


class OrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Organization
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'auth__input'}),
            'fio': forms.TextInput(attrs={'class': 'auth__input'}),
            'password': forms.PasswordInput(attrs={'class': 'auth__input'})
        }
