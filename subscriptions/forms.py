from django import forms
from .models import SellerSubscription, BuyerMembership

class SellerSubscriptionForm(forms.ModelForm):
    class Meta:
        model = SellerSubscription
        fields = ['plan', 'amount_paid', 'receipt_image', 'payment_reference']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_paid'].help_text = "Ensure you transfer the correct fee for your chosen plan."
        self.fields['payment_reference'].help_text="TransactionID in sms after payment"

class BuyerMembershipForm(forms.ModelForm):
    class Meta:
        model = BuyerMembership
        fields = ['amount_paid', 'receipt_image', 'payment_reference']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_paid'].initial = 20000.00
        self.fields['amount_paid'].widget.attrs['readonly'] = True
        self.fields['amount_paid'].help_text = "Standard Buyer Membership fee is 20,000 UGX."
        self.fields['payment_reference'].help_text="TransactionID in sms after payment"
