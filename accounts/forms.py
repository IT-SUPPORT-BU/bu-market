from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            (User.Role.BUYER, 'Buyer — I want to browse and purchase items'),
            (User.Role.SELLER, 'Seller — I want to list items for sale')
        ],
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'whatsapp_number', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.phone_number = self.cleaned_data.get('phone_number')
        user.whatsapp_number = self.cleaned_data.get('whatsapp_number')
        if commit:
            user.save()
        return user
