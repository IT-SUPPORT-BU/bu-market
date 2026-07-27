from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.shortcuts import render, redirect, get_object_or_404
from marketplace.models import Listing
from .models import Conversation, Message
from .forms import MessageForm

MAX_MESSAGES_PER_CONVERSATION = 10  # adjust as needed — e.g. 5 exchanges each way


@login_required
def start_conversation(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.seller:
        return redirect('marketplace:listing_detail', pk=listing.pk)

    conversation, created = Conversation.objects.get_or_create(
        listing=listing,
        buyer=request.user,
        seller=listing.seller,
    )
    return redirect('messaging:conversation_detail', pk=conversation.pk)


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in [conversation.buyer, conversation.seller]:
        return redirect('core:home')

    message_count = conversation.messages.count()
    limit_reached = message_count >= MAX_MESSAGES_PER_CONVERSATION
    is_seller_view = request.user == conversation.seller

    if is_seller_view:
        target_whatsapp_url = conversation.buyer.whatsapp_url
        target_whatsapp_number = conversation.buyer.whatsapp_number
        whatsapp_label = f"Buyer WhatsApp"
    else:
        target_whatsapp_url = conversation.listing.whatsapp_url
        target_whatsapp_number = conversation.listing.whatsapp_number
        whatsapp_label = "Seller WhatsApp"

    whatsapp_url = target_whatsapp_url or conversation.listing.whatsapp_url
    whatsapp_number = target_whatsapp_number or conversation.listing.whatsapp_number

    if request.method == 'POST':
        if limit_reached:
            django_messages.error(request, "This conversation has reached its message limit.")
            return redirect('messaging:conversation_detail', pk=conversation.pk)

        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.save()
            return redirect('messaging:conversation_detail', pk=conversation.pk)
    else:
        form = MessageForm()

    # Mark incoming messages read when the recipient opens the conversation
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    messages_list = conversation.messages.select_related('sender')
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages_list': messages_list,
        'form': form,
        'limit_reached': limit_reached,
        'message_count': message_count,
        'max_messages': MAX_MESSAGES_PER_CONVERSATION,
        'whatsapp_url': whatsapp_url,
        'whatsapp_number': whatsapp_number,
        'whatsapp_label': whatsapp_label,
    })


@login_required
def inbox(request):
    conversations = (Conversation.objects.filter(buyer=request.user) | Conversation.objects.filter(seller=request.user)).distinct().select_related('listing', 'buyer', 'seller')
    conversation_items = []
    for conversation in conversations:
        conversation_items.append({
            'conversation': conversation,
            'unread': conversation.messages.filter(is_read=False).exclude(sender=request.user).count(),
            'last_sender_name': conversation.last_sender.username if conversation.last_sender else None,
        })

    return render(request, 'messaging/inbox.html', {'conversation_items': conversation_items})