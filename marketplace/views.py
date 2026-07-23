from django.shortcuts import render

#from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages as django_messages
from .models import Listing
from messaging.models import Conversation


@login_required
def mark_as_sold(request, slug):
    listing = get_object_or_404(Listing, slug=slug)

    if request.user != listing.seller:
        django_messages.error(request, "You can only mark your own listings as sold.")
        return redirect('core:listing_detail', slug=listing.slug)

    if request.method == 'POST':
        listing.status = Listing.Status.SOLD
        listing.sold_at = timezone.now()
        listing.save(update_fields=['status', 'sold_at'])

        Conversation.objects.filter(listing=listing).delete()

        django_messages.success(request, f"'{listing.title}' marked as sold.")
        return redirect('core:listing_detail', slug=listing.slug)

    return redirect('core:listing_detail', slug=listing.slug)
