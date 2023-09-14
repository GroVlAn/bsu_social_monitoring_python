from django import forms
from django.core.cache import cache

from apps.monitoring.models_db.team import *


class TeamForm(forms.ModelForm):
    def __init__(self, team=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if team is not None:
            self.fields['name'].initial = team.name
            self.fields['description'].initial = team.description

    def save(self, team=None, user=None, commit=True):

        if team is None:
            team = super().save(commit=False)
        else:
            team.name = self.cleaned_data.get('name')
            team.description = self.cleaned_data.get('description')
            team_key = f'{user.id}_{user.username}_team'
            cache.set(team_key, team)

        if commit:
            team.save()

        if user and team is not None:
            team.users.add(user)

        if commit:
            team.save()

        return team

    class Meta:
        model = Team
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'auth__input'}),
            'description': forms.Textarea(attrs={'class': 'auth__input'}),
        }
