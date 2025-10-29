from django.shortcuts import render, redirect, get_object_or_404
from vehicles.models import Vehicle
from user_acc.models import User_profile
from .forms import ReservationForm
from .models import Reservation
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def vehicle_booking(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    # Check if the user already has a pending or approved reservation for this vehicle
    existing_reservation = Reservation.objects.filter(
        user=request.user,
        vehicle=vehicle,
        status__in=['pending', 'approved']
    ).first()

    if existing_reservation:
        messages.error(request, "You already have a reservation for this vehicle.")
        return redirect('viewer_homepage')

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.vehicle = vehicle
            reservation.status = 'pending'
            reservation.save()
            send_mail(
                subject='Reservation Request',
                message=(
                    f'New reservation request for {vehicle.vehicle_type} '
                    f'from {reservation.start_date} to {reservation.end_date}.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[vehicle.owner.email],
            )
            messages.success(request, "Reservation requested successfully!")
            return redirect('viewer_homepage')
    else:
        form = ReservationForm()

    return render(request, 'reservation/vehicle_booking.html', {
        'vehicle': vehicle,
        'form': form,
    })


@login_required
def booking_status(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    vehicle = reservation.vehicle

    # Ensure only the driver who owns the vehicle can access
    if vehicle.owner != request.user:
        messages.error(request, "You are not allowed to manage this reservation.")
        return redirect('vehicles:driver_homepage')

    if request.method == "POST":
        action = request.POST.get("action")
        if action in ["approved", "completed", "available", "pending"]:
            reservation.status = action
            reservation.save()


           
            if action == "approved":
                subject = 'Reservation Approved'
                body = (
                    f'Your reservation of {vehicle.vehicle_type} '
                    f'from {reservation.start_date} to {reservation.end_date} has been approved.\n\n'
                    f'Please pay the amount to complete the booking.'
                )

                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[reservation.user.email],
                )

                # Attach QR code if it exists
                if vehicle.qr_image and vehicle.qr_image.path:
                    email.attach_file(vehicle.qr_image.path)

                email.send()
            elif action == "completed":
                subject = 'Reservation Completed'
                body = (
                    f'Your reservation of {vehicle.vehicle_type} '
                    f'from {reservation.start_date} to {reservation.end_date} has been marked as completed.\n\n'
                    f'Thank you for using our service!'
                )
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reservation.user.email],
                )
            messages.success(request, f"Reservation status updated to {action}.")
            return redirect('vehicles:driver_homepage')  # redirect back to driver homepage
        
        

    return render(request, "reservation/booking_status.html", {
        "reservation": reservation,
        "vehicle": vehicle
    })

@login_required
def reject_booking(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    user = reservation.user
    if request.method == "POST":
        reservation.delete()
        send_mail(
            subject='Reservation Rejected',
            message=(
                f'Your reservation of {reservation.vehicle.vehicle_type} '
                f'from {reservation.start_date} to {reservation.end_date} has been rejected.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.user.email],
        )
        messages.success(request, "Reservation has been rejected.")
        return redirect('reservation:user_booking')
    return render(request, 'reservation/reject_booking.html', 
                  {'reservation': reservation,
                     'user': user})
                                                            

@login_required
def payment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.user != request.user:
        messages.error(request, "You are not authorized to view this payment page.")
        return redirect('viewer_homepage')
    if request.method == 'POST':
        payment_proof = request.FILES.get('payment_proof')
        if payment_proof:
            reservation.status = 'Paid'
            reservation.payment_proof = payment_proof
            reservation.save()
            messages.success(request, "Payment proof uploaded successfully. Awaiting approval.")
            send_mail(
                subject='Payment is completed',
                message=(
                    f'Payment is done for your reservation of {reservation.vehicle.vehicle_type} '
                    f'from {reservation.start_date} to {reservation.end_date} has been submitted.'
                    f'Please change the status to completed after verification.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reservation.vehicle.owner.email],
            )
            return redirect('viewer_homepage')
        else:
            reservation.status ='Unpaid'
            messages.error(request, "Please upload a valid payment proof.")
    return render(request, 'reservation/payment.html', {'reservation': reservation})


def user_booking(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation/user_booking.html', {'reservations': reservations})



@login_required
def driver_booking(request, reservation_id=None):
    reservations = Reservation.objects.filter(vehicle__owner=request.user)

    if request.method == 'POST' and reservation_id:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        action = request.POST.get('action')
        if action in ['available', 'pending', 'approved']:
            reservation.status = action
            reservation.save()
            messages.success(request, f"Reservation {action} successfully.")
        return redirect('reservation:driver_booking')

    return render(request, 'reservation/driver_booking.html', {'reservations': reservations})
