from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from marketplace.models import Listing, Hostel
from dashboard.views import role_required
from accounts.models import User

@login_required
@role_required([User.Role.MODERATOR])
def approve_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.status = Listing.Status.ACTIVE
    listing.save()
    messages.success(request, f'Listing "{listing.title}" approved and is now active on the market.')
    return redirect('dashboard:moderator_dashboard')

@login_required
@role_required([User.Role.MODERATOR])
def reject_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.status = Listing.Status.REJECTED
    listing.save()
    messages.warning(request, f'Listing "{listing.title}" has been rejected.')
    return redirect('dashboard:moderator_dashboard')


@login_required
@role_required([User.Role.MODERATOR])
def approve_hostel(request, pk):
    hostel = get_object_or_404(Hostel, pk=pk)
    hostel.status = Hostel.Status.ACTIVE
    hostel.save()
    messages.success(request, f'Hostel "{hostel.name}" approved and is now visible on the market.')
    return redirect('dashboard:moderator_dashboard')

@login_required
@role_required([User.Role.MODERATOR])
def reject_hostel(request, pk):
    hostel = get_object_or_404(Hostel, pk=pk)
    hostel.status = Hostel.Status.REJECTED
    hostel.save()
    messages.warning(request, f'Hostel "{hostel.name}" has been rejected.')
    return redirect('dashboard:moderator_dashboard')
