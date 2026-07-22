from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'title', 'description', 'price', 'condition', 'location', 'image', 'is_promoted', 'phone_number', 'whatsapp_number']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user:
            # Temporarily attach the seller instance to run validation
            self.instance.seller = self.user
        
        # Call model clean() to run limits/subscriptions checks
        self.instance.clean()
        return cleaned_data
