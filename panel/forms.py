from django import forms


class CatalogProductBuyForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    count = forms.IntegerField(initial=1, min_value=1, max_value=100)

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['count'].max_value = product.available_count
            self.fields['count'].widget.attrs['max'] = product.available_count
            self.fields['product_id'].initial = product.id
