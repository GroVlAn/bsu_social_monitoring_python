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

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label='Организация',
        empty_label='Выбрать'
    )

    class Meta:
        model = GroupAnalyzedItems
        fields = [
            'ru_name',
            'level',
            'organization'
        ]
        widgets = {
            'ru_name': forms.TextInput(attrs={'class': 'group_analyzed_items__input'}),
            'level': forms.TextInput(attrs={'class': 'group_analyzed_items__input'}),
            'organization': forms.Select(attrs={'class': 'group_analyzed_items__input'})
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
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label='Организация',
        empty_label=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = AnalyzedItem
        fields = [
            'group',
            'name',
            'description',
            'parent',
            'organization'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'analyzed_items__input'}),
            'description': forms.Textarea(attrs={'class': 'analyzed_items__input'}),
            'group': forms.Select(attrs={'class': 'analyzed_items__select'}),
            'parent': forms.Select(attrs={'class': 'analyzed_items__select'}),
            'organization': forms.Select(attrs={'class': 'analyzed_items__select'})
        }
