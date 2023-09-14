from django import forms

from apps.monitoring.models_db.search_items import GroupSearchItems, SearchItem
from apps.monitoring.models_db.team import Team


class GroupSearchItemsForm(forms.ModelForm):
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

    def __init__(self, request=None, group: GroupSearchItems = None, *args, **kwargs):

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
        model = GroupSearchItems
        fields = [
            'ru_name',
            'level',
            'team'
        ]
        widgets = {
            'ru_name': forms.TextInput(attrs={'class': 'group_search_items__input'}),
            'level': forms.TextInput(attrs={'class': 'group_search_items__input'}),
            'team': forms.Select(attrs={'class': 'group_search_items__input'})
        }


class SearchItemsForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=GroupSearchItems.objects.all(),
        label='Группа',
        empty_label=None,
    )
    parent = forms.ModelChoiceField(
        queryset=SearchItem.objects.all(),
        label='Родитель',
        empty_label='Выберете',
        required=False,
        initial=None
    )

    def __init__(self, request, search_item: SearchItem = None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if search_item is not None:
            self.fields['group'].initial = search_item.group
            self.fields['name'].initial = search_item.name
            self.fields['description'].initial = search_item.description
            self.fields['parent'].initial = search_item.parent
            self.fields['team'].initial = search_item.team

        self.fields['team'].queryset = Team.objects.filter(users=request.user)
        self.fields['team'].label = 'Команда'
        self.fields['team'].empty_label = None

    def save(self, search_item: SearchItem = None, commit=True):

        if search_item is None:
            search_item = super().save(commit=False)
        else:
            search_item.group = self.cleaned_data['group']
            search_item.name = self.cleaned_data['name']
            search_item.description = self.cleaned_data['description']
            search_item.parent = self.cleaned_data['parent']
            search_item.team = self.cleaned_data['team']

        if commit:
            search_item.save()

        return search_item

    class Meta:
        model = SearchItem
        fields = [
            'group',
            'name',
            'description',
            'parent',
            'team'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'search_items__input'}),
            'description': forms.Textarea(attrs={'class': 'search_items__input'}),
            'group': forms.Select(attrs={'class': 'search_items__select'}),
            'parent': forms.Select(attrs={'class': 'search_items__select'}),
            'team': forms.Select(attrs={'class': 'search_items__select'})
        }
