from django import forms
from monitoring.models_db.organization import *


class OrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, user=None, commit=True):
        organization = super().save(commit=False)
        if user:
            organization.users.add(user)
        if commit:
            organization.save()
        return organization

    class Meta:
        model = Organization
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'auth__input'}),
            'description': forms.Textarea(attrs={'class': 'auth__input'}),
        }
