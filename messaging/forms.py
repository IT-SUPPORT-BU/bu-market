from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'maxlength': 600,
                'placeholder': 'Type a message (max 30 words)...'
            })
        }

    def clean_body(self):
        body = self.cleaned_data['body'].strip()
        word_count = len(body.split())
        if word_count > 30:
            raise forms.ValidationError(f"Message is {word_count} words — please keep it under 30 words.")
        if not body:
            raise forms.ValidationError("Message cannot be empty.")
        return body