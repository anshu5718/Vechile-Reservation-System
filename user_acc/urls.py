from django.urls import path
from . import views

urlpatterns = [
    path('', views.first_view, name='first_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('viewer_homepage/', views.viewer_homepage, name='viewer_homepage'),
    path('logout/', views.logout_view, name='logout_view'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),  # Placeholder for forgot password view
    path('otp_confirmation/', views.otp_confirmation_view, name='otp_confirmation'),  # Placeholder for OTP confirmation view
    path('set_new_password/<int:user_id>/',
          views.set_new_password_view, name='set_new_password'),  # Placeholder for setting new password view
    path('booking_cancel/<int:reservation_id>/', views.booking_cancel, name='booking_cancel'),  # New path for booking cancellation
    
]
