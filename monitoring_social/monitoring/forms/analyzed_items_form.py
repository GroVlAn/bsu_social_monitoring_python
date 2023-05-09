from django import forms
from monitoring.models_db.analyzed_items import *


class GroupAnalyzedItemsForm(forms.ModelForm):
    ru_name = forms.CharField(
        label='Название',
        widget=forms.TextInput(),
        required=True
    )

    level = forms.IntegerField(
        label='Уровень',
        initial=None
    )

    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label='Команда',
        empty_label='Выбрать'
    )

    def __init__(self, request=None, group: GroupAnalyzedItems = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if group is not None:
            self.fields['ru_name'].initial = group.ru_name
            self.fields['level'].initial = group.level
            self.fields['team'].initial = group.team
        if request is not None:
            self.fields['team'].queryset = Team.objects.filter(users=request.user)
            self.fields['team'].label = 'Команда'
            self.fields['team'].empty_label = None

    def save(self, group=None, commit=True):
        if group is None:
            group = super().save(commit=False)
        else:
            group.ru_name = self.cleaned_data['ru_name']
            group.level = self.cleaned_data['level']
            group.team = self.cleaned_data['team']

        if commit:
            group.save()

        return group

    class Meta:
        model = GroupAnalyzedItems
        fields = [
            'ru_name',
            'level',
            'team'
        ]
        widgets = {
            'ru_name': forms.TextInput(attrs={'class': 'group_analyzed_items__input'}),
            'level': forms.TextInput(attrs={'class': 'group_analyzed_items__input'}),
            'team': forms.Select(attrs={'class': 'group_analyzed_items__input'})
        }


class AnalyzedItemsForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=GroupAnalyzedItems.objects.all(),
        label='Группа',
        empty_label=None,
    )
    parent = forms.ModelChoiceField(
        queryset=AnalyzedItem.objects.all(),
        label='Родитель',
        empty_label='Выберете',
        required=False,
        initial=None
    )

    def __init__(self, request, analyzed_item: AnalyzedItem = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if analyzed_item is not None:
            self.fields['group'].initial = analyzed_item.group
            self.fields['name'].initial = analyzed_item.name
            self.fields['description'].initial = analyzed_item.description
            self.fields['parent'].initial = analyzed_item.parent
            self.fields['team'].initial = analyzed_item.team
        self.fields['team'].queryset = Team.objects.filter(users=request.user)
        self.fields['team'].label = 'Команда'
        self.fields['team'].empty_label = None

    def save(self, analyzed_item: AnalyzedItem = None, commit=True):
        if analyzed_item is None:
            analyzed_item = super().save(commit=False)
        else:
            analyzed_item.group = self.cleaned_data['group']
            analyzed_item.name = self.cleaned_data['name']
            analyzed_item.description = self.cleaned_data['description']
            analyzed_item.parent = self.cleaned_data['parent']
            analyzed_item.team = self.cleaned_data['team']

        if commit:
            analyzed_item.save()

        return analyzed_item

    class Meta:
        model = AnalyzedItem
        fields = [
            'group',
            'name',
            'description',
            'parent',
            'team'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'analyzed_items__input'}),
            'description': forms.Textarea(attrs={'class': 'analyzed_items__input'}),
            'group': forms.Select(attrs={'class': 'analyzed_items__select'}),
            'parent': forms.Select(attrs={'class': 'analyzed_items__select'}),
            'team': forms.Select(attrs={'class': 'analyzed_items__select'})
        }
