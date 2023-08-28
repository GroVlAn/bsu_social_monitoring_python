from django import forms


class FilterSearchItemsForm(forms.Form):
    date_from = forms.CharField(
        label='С',
        widget=forms.TextInput(attrs={
            'class': 'js_date_picker',
            'placeholder': 'dd.mm.yyyy'
        }),
        required=False
    )
    date_to = forms.CharField(
        label='До',
        widget=forms.TextInput(attrs={
            'class': 'js_date_picker',
            'placeholder': 'dd.mm.yyyy'
        }),
        required=False
    )

    class Meta:
        fields = [
            'date_from',
            'date_to'
        ]
