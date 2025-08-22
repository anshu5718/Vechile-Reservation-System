from django.contrib import admin
from .models import User_profile, OTP

admin.site.register(User_profile)

# Register your models here.

class OTP_Time(admin.ModelAdmin):  
    list_display = ('otp', 'created_at') 

admin.site.register(OTP, OTP_Time)