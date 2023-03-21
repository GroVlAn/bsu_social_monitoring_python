from django import forms
from monitoring.models_db.AnalyzedItems import *


class GroupAnalyzedItemsForm(forms.ModelForm):
    class Meta:
        model = GroupAnalyzedItems
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'group_analyzed_items__input'})
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
