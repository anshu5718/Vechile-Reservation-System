from django.urls import path
from . import views

app_name = 'vehicles'
urlpatterns = [
    path('register_vehicle/', views.register_vehicle, name='register_vehicle'),
    path('driver_homepage/', views.driver_homepage, name='driver_homepage'),
]
