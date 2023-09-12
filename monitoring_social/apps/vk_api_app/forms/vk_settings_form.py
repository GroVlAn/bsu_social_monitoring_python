from django import forms

from apps.monitoring.models_db.team import Team
from apps.vk_api_app.models_db.vk_settings import VkSettings


class VkSettingsForm(forms.ModelForm):
    token = forms.CharField(
        label='Токен',
        widget=forms.TextInput(),
    )
    group_id = forms.CharField(
        label='Id группы вконтакте',
        widget=forms.NumberInput()
    )
    team = forms.ModelChoiceField(
        queryset=None,
        label='Команда',
        empty_label='Выбрать'
    )

    def __init__(self, request=None, vk_settings: VkSettings = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if vk_settings:
            self.fields['token'].initial = vk_settings.token
            self.fields['group_id'].initial = vk_settings.group_id
            self.fields['team'].initial = vk_settings.team
        if request is not None:
            self.fields['team'].queryset = Team.objects.filter(users=request.user)

    def save(self, vk_settings: VkSettings = None, commit=True):
        if not vk_settings:
            vk_settings = super().save(commit=False)
        else:
            vk_settings.token = self.cleaned_data['token']
            vk_settings.group_id = self.cleaned_data['group_id']
            vk_settings.team = self.cleaned_data['team']

        if commit:
            vk_settings.save()

        return vk_settings

    class Meta:
        model = VkSettings
        fields = [
            'token',
            'group_id',
            'team'
        ]
