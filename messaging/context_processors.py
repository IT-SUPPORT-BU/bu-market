from django.db.models import Q
from .models import Conversation, Message


def unread_message_counts(request):
    if not request.user.is_authenticated:
        return {}

    unread_count = Message.objects.filter(
        Q(conversation__buyer=request.user) | Q(conversation__seller=request.user),
        is_read=False
    ).exclude(sender=request.user).count()

    messages = Message.objects.filter(
        Q(conversation__buyer=request.user) | Q(conversation__seller=request.user)
    ).select_related('conversation__listing', 'conversation__buyer', 'conversation__seller', 'sender').order_by('-sent_at')

    previews = []
    seen_conversations = set()
    for msg in messages:
        conv = msg.conversation
        if conv.pk in seen_conversations:
            continue
        seen_conversations.add(conv.pk)
        other_party = conv.other_party(request.user)
        previews.append({
            'conversation_pk': conv.pk,
            'listing_title': conv.listing.title,
            'other_username': other_party.username,
            'sender_username': msg.sender.username,
            'snippet': msg.body[:45] + ('...' if len(msg.body) > 45 else ''),
            'unread': conv.unread_count_for(request.user),
        })
        if len(previews) >= 3:
            break

    return {
        'unread_message_count': unread_count,
        'message_previews': previews,
    }
