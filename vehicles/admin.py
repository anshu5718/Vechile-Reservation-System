from django.contrib import admin, messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Vehicle

class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'owner',
        'registration_number', 
        'vehicle_type', 
        'is_active', 
        'kyc_approved'
    )
    list_editable = ('kyc_approved','is_active')
    list_filter = ('owner', 'is_active', 'kyc_approved', 'vehicle_type', 'cost_per_day' )
    search_fields = ('registration_number', 'owner__username', 'owner__email')


    # KYC approval/rejection notifications
    def save_model(self, request, obj, form, change):
        if change:
            old_kyc = form.initial.get("kyc_approved", False)

            # KYC approved
            if not old_kyc and obj.kyc_approved:
                if obj.owner.email:
                    send_mail(
                        subject=f'KYC Approved: {obj.vehicle_type} ({obj.registration_number})',
                        message=f'Hello {obj.owner.username}, your KYC for vehicle {obj.registration_number} has been approved!',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[obj.owner.email],
                        fail_silently=True,
                    )
                messages.success(request, f"KYC approval email sent to {obj.owner.username}")

            # KYC rejected
            elif old_kyc and not obj.kyc_approved:
                if obj.owner.email:
                    send_mail(
                        subject=f'KYC Rejected: {obj.vehicle_type} ({obj.registration_number})',
                        message=f'Hello {obj.owner.username}, your KYC for vehicle {obj.registration_number} has been rejected.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[obj.owner.email],
                        fail_silently=True,
                    )
                messages.warning(request, f"KYC rejection email sent to {obj.owner.username}")

        super().save_model(request, obj, form, change)

# Register Vehicle with this admin
admin.site.register(Vehicle, VehicleAdmin)
