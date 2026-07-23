from django import forms
from django.contrib import admin
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Category, Listing


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


class RemovalReasonForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, label="Reason for removal")


@admin.action(description="Remove selected listings with a reason")
def remove_with_reason(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = RemovalReasonForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            for listing in queryset:
                listing.status = Listing.Status.REMOVED
                listing.removal_reason = reason
                listing.save()
                send_mail(
                    subject=f"Your listing '{listing.title}' was removed",
                    message=f"Your product '{listing.title}' was removed by an admin.\n\nReason: {reason}",
                    from_email=None,
                    recipient_list=[listing.seller.email],
                )
            return redirect(request.get_full_path())
    else:
        form = RemovalReasonForm()

    return render(request, 'admin/removal_reason_form.html', {
        'listings': queryset,
        'form': form,
    })


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'condition', 'status', 'is_promoted']
    list_filter = ['status', 'is_promoted', 'condition', 'category']
    search_fields = ['title', 'description', 'seller__username']
    prepopulated_fields = {'slug': ('title',)}
    actions = [remove_with_reason]