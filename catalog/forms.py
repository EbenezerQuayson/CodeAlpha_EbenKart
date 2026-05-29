from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-input'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'city', 'country', 'payment_method']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+233 55 123 4567', 'class': 'form-input'}),
            'address': forms.TextInput(attrs={'placeholder': '123 Fashion Ave', 'class': 'form-input'}),
            'city': forms.TextInput(attrs={'placeholder': 'Accra', 'class': 'form-input'}),
            'country': forms.TextInput(attrs={'placeholder': 'Ghana', 'class': 'form-input'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
