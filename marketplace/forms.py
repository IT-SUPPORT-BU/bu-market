from django import forms
from .models import Listing, Hostel, HostelImage, Community

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'community', 'title', 'description', 'price', 'condition', 'location', 'image', 'is_promoted', 'phone_number', 'whatsapp_number']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['community'].queryset = Community.objects.filter(is_active=True).order_by('order', 'name')
        self.fields['community'].empty_label = "Select Campus or Town Hub"

    def clean(self):
        cleaned_data = super().clean()
        if self.user:
            # Temporarily attach the seller instance to run validation
            self.instance.seller = self.user
        
        # Call model clean() to run limits/subscriptions checks
        self.instance.clean()
        return cleaned_data


class HostelForm(forms.ModelForm):
    image_1 = forms.ImageField(required=True)
    image_2 = forms.ImageField(required=False)
    image_3 = forms.ImageField(required=False)
    image_4 = forms.ImageField(required=False)

    class Meta:
        model = Hostel
        fields = ['name', 'community', 'location', 'price', 'description', 'phone_number', 'whatsapp_number']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['community'].queryset = Community.objects.filter(is_active=True).order_by('order', 'name')
        self.fields['community'].empty_label = "Select Campus or Town Hub"

    def clean(self):
        cleaned_data = super().clean()
        if self.user:
            self.instance.owner = self.user
        self.instance.clean()
        return cleaned_data
