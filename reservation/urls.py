from django.urls import path
from . import views 

app_name = 'reservation'

urlpatterns = [
    path('vehicle_reservation/<int:vehicle_id>/', views.vehicle_booking, name='vehicle_booking'),
    path('booking_status/<int:reservation_id>/', views.booking_status, name='booking_status'),
    path('reject_booking/<int:reservation_id>/', views.reject_booking, name='reject_booking'),
    path('payment/<int:reservation_id>/', views.payment, name='payment'),
    path('user_booking/', views.user_booking, name='user_booking'),
    path ('driver_booking/', views.driver_booking, name='driver_booking'),
    path('driver_booking/<int:reservation_id>/', views.driver_booking, name='driver_booking'),
]
