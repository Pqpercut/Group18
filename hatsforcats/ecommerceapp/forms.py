from django import forms
from .models import ProductVariant

class UpdateStockForm(forms.Form):
    variant = forms.ModelChoiceField(queryset=ProductVariant.objects.all(), widget=forms.HiddenInput())
    stocklevel = forms.IntegerField(label="New Stock Level", min_value=0)

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['variant'].queryset = product.productvariant.all()


class CreateVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['size', 'colour', 'price', 'stocklevel']

class VariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['size', 'colour', 'price', 'stocklevel']
