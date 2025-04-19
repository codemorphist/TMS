from django import forms


class AddProductForm(forms.Form):
    name = forms.CharField(label='Product Name')


