from django import forms
from .models import ProductVariant, ImagePath
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactTable, UserAddress,Review
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django import forms

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address'
        }),
    )

class UpdateStockForm(forms.Form):
    variant = forms.ModelChoiceField(queryset=ProductVariant.objects.all(), widget=forms.HiddenInput())
    stocklevel = forms.IntegerField(label="New Stock Level", min_value=0)

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['variant'].queryset = product.productvariant.all()
            
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

class filterProducts(forms.Form):
    hatFilter = forms.BooleanField(label= "Hats",required=False)
    glassesFilter = forms.BooleanField(label= "Sunglasses", required=False)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email address'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Reoeat password'
        })



class ContactEnquiryForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe your issue', 'rows': 6}))
    
    class Meta:
        model = ContactTable
        fields = ['username','description','email']


class CheckoutForm(forms.ModelForm):
    
    class Meta:
        model = UserAddress
        fields = ['houseNumber', 'apartmentNumber', 'street', 'postcode', 'city']
        widgets = {
            'street': forms.TextInput(attrs={'placeholder': 'Street'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postcode'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        
        model = Review
        fields = ['title', 'description']
        widgets = {
            'rating': forms.HiddenInput(),  # This makes the rating field hidden in the HTML
            'productID' : forms.HiddenInput(),
            'userID': forms.HiddenInput()
        }

        def __init__(self, *args, **kwargs):
            kwargs.pop('user', None)  # Remove 'user' from kwargs to prevent error
            super().__init__(*args, **kwargs)  # Call the parent __init__ method

        def save(self, commit=True):
            review = super().save(commit=False)
            if self.user:
                review.created_by = self.user  # Assign user to created_by
            if commit:
                review.save()
            return review
