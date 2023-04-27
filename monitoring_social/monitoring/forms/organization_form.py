from django import forms
from django.core.cache import cache

from monitoring.models_db.organization import *


class OrganizationForm(forms.ModelForm):
    def __init__(self, organization=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if organization is not None:
            self.fields['name'].initial = organization.name
            self.fields['description'].initial = organization.description

    def save(self, organization=None, user=None, commit=True):
        if organization is None:
            organization = super().save(commit=False)
        else:
            organization.name = self.cleaned_data.get('name')
            organization.description = self.cleaned_data.get('description')
            organization_key = f'{user.id}_{user.username}_organization'
            cache.set(organization_key, organization)

        print(organization)
        if commit:
            organization.save()
        if user and organization is not None:
            print(user)
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
