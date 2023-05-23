from django import forms


class FilterSearchItemsForm(forms.Form):
    date_from = forms.CharField(
        label='С',
        widget=forms.TextInput(),
        required=False
    )
    date_to = forms.CharField(
        label='До',
        widget=forms.TextInput(),
        required=False
    )

    class Meta:
        fields = [
            'date_from',
            'date_to'
        ]
        widget = {
            'date_form': forms.TextInput(attrs={'class': 'js_date_picker'}),
            'date_to': forms.TextInput(attrs={'class': 'js_date_picker'})
        }
