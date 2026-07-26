from django.conf import settings
from django.db import models
from marketplace.models import Listing


class Conversation(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='conversations')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_as_buyer')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_as_seller')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('listing', 'buyer', 'seller')

    def __str__(self):
        return f"{self.buyer} <-> {self.seller} on {self.listing.title}"

    def other_party(self, user):
        return self.seller if user == self.buyer else self.buyer

    def unread_count_for(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    @property
    def last_sender(self):
        latest_message = self.messages.order_by('-sent_at').first()
        return latest_message.sender if latest_message else None


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at:%Y-%m-%d %H:%M:%S}"