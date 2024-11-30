from django import forms
from .models import ProductVariant, ImagePath

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

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CreateVariantForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = ProductVariant
        fields = ['size', 'colour', 'price', 'stocklevel']


class EditVariantForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = ProductVariant
        fields = ['size', 'colour', 'price', 'stocklevel']