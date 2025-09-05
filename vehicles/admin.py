from django.contrib import admin, messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Vehicle

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'registration_number', 'vehicle_type', 'is_active', 'kyc_approved')
    list_filter = ('is_active', 'kyc_approved', 'vehicle_type')
    list_editable = ('kyc_approved',)

    def save_model(self, request, obj, form, change):
        if change:  # Only on updates
            old_obj = Vehicle.objects.get(pk=obj.pk)

            # Notify if KYC changed from False → True (approved)
            if not old_obj.kyc_approved and obj.kyc_approved:
                send_mail(
                    subject='KYC Approved',
                    message=f'Hello {obj.owner.username}, your KYC for vehicle {obj.registration_number} has been approved!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.owner.email],
                    fail_silently=True,
                )
                messages.add_message(request, messages.SUCCESS,
                                     f"KYC approval email sent to {obj.owner.username}")
            elif old_obj.kyc_approved and not obj.kyc_approved:
                send_mail(
                    subject='KYC Rejected',
                    message=f'Hello {obj.owner.username}, your KYC for vehicle {obj.registration_number} has been rejected!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.owner.email],
                    fail_silently=True,
                )

        super().save_model(request, obj, form, change)

admin.site.register(Vehicle, VehicleAdmin)
