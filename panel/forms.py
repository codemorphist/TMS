from django import forms


class ClientBuyForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    count = forms.IntegerField(initial=1, min_value=1, max_value=100)

    def __init__(self, *args, **kwargs):
        max_count = kwargs.pop('max_count', None)
        super().__init__(*args, **kwargs)
        if max_count is not None:
            self.fields['count'].widget.attrs['max'] = max_count