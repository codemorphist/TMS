from django import forms


class OrderForm(forms.Form):
    product = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(initial=1, min_value=1)

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)

        if product:
            self.fields['product'].initial = product.id
            self.fields['quantity'].max_value = product.stock
            self.fields['quantity'].widget.attrs['max'] = product.stock
