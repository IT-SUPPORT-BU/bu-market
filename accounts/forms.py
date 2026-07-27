from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Registration form for sellers only.
    Buyers do not need to register — they can browse freely.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'whatsapp_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        # All registrations are for sellers — buyers browse anonymously
        user.role = User.Role.SELLER
        user.phone_number = self.cleaned_data.get('phone_number')
        user.whatsapp_number = self.cleaned_data.get('whatsapp_number')
        if commit:
            user.save()
        return user
