from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from dashboard.views import role_required
from accounts.models import User
from .models import SellerSubscription, SubscriptionPlan
from .forms import SellerSubscriptionForm


@login_required
@role_required([User.Role.SELLER])
def apply_seller(request):
    # Check if they already have a pending application
    pending_app = SellerSubscription.objects.filter(
        seller=request.user,
        status=SellerSubscription.Status.PENDING
    ).first()
    if pending_app:
        messages.info(request, "You already have a pending subscription application.")
        return redirect('dashboard:seller_dashboard')

    if request.method == 'POST':
        form = SellerSubscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.seller = request.user
            sub.status = SellerSubscription.Status.PENDING
            sub.save()
            messages.success(
                request,
                "Your subscription application has been submitted successfully and is pending approval."
            )
            return redirect('dashboard:seller_dashboard')
    else:
        form = SellerSubscriptionForm()

    return render(request, 'subscriptions/apply_seller.html', {
        'form': form,
        'plans': SubscriptionPlan.objects.all()
    })


@login_required
@role_required([User.Role.ACCOUNTANT])
def approve_seller_subscription(request, pk):
    sub = get_object_or_404(SellerSubscription, pk=pk)
    sub.status = SellerSubscription.Status.APPROVED
    sub.approved_by = request.user
    sub.approved_at = timezone.now()
    sub.expires_at = timezone.now() + timedelta(days=30)
    sub.save()
    messages.success(request, f"Approved subscription for seller {sub.seller.username}.")
    return redirect('dashboard:accountant_dashboard')


@login_required
@role_required([User.Role.ACCOUNTANT])
def reject_seller_subscription(request, pk):
    sub = get_object_or_404(SellerSubscription, pk=pk)
    sub.status = SellerSubscription.Status.REJECTED
    sub.approved_by = request.user
    sub.approved_at = timezone.now()
    sub.save()
    messages.warning(request, f"Rejected subscription for seller {sub.seller.username}.")
    return redirect('dashboard:accountant_dashboard')
